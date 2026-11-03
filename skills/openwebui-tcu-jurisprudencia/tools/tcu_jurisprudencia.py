"""
title: Fontes oficiais Servfaz
description: Pesquisa acórdãos, jurisprudência selecionada e súmulas do TCU e traz o texto vigente da Lei 14.133/2021 para fundamentar impugnações e recursos.
author: Servfaz
version: 0.2.0
"""
# Import manual em Workspace > Tools; Function Calling = Native no modelo (ver ../INSTALACAO.md).
# Usa a API REST pública por trás de pesquisa.apps.tcu.gov.br. O firewall do TCU barra User-Agent genérico
# (ex.: o padrão do curl), respondendo HTTP 200 com HTML de bloqueio: por isso o UA próprio e honesto nas Valves,
# e HTML no lugar de JSON é tratado como falha técnica, nunca como "nenhum resultado".
# O texto da Lei 14.133 vem da API do normas.leg.br (Congresso Nacional): a lei inteira em JSON-LD, um nó por
# dispositivo, com o histórico de versões de cada um; a tool escolhe a versão vigente e guarda a lei em cache.
import asyncio
import html
import json
import math
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

from pydantic import BaseModel, Field

PORTAL = 'https://pesquisa.apps.tcu.gov.br'
AVISO = ('_Resultado da Pesquisa de Jurisprudência do TCU. É candidato, não prova: abra o inteiro teor com '
         'obter_acordao_tcu e confira deliberação, lei aplicada e contexto antes de citar. Verifique na lista '
         'enunciados em sentido contrário. Só transcreva entre aspas o que veio do texto aberto._')
NENHUM = 'Nenhum resultado na Pesquisa do TCU para esta consulta. Tente frases mais curtas, entre aspas, ou outro termo.'
FALHA = ('A consulta ao TCU falhou (erro técnico: {motivo}). Não foi possível pesquisar agora. Informe isso ao '
         'usuário, não conclua que não há jurisprudência sobre o tema e não transcreva texto de súmula ou acórdão '
         'de memória: marque o precedente como "a conferir".')
COLEGIADOS = ('Plenário', 'Primeira Câmara', 'Segunda Câmara')


class FalhaConsulta(Exception):
    """Erro técnico na consulta (HTTP, rede, timeout, bloqueio do firewall ou resposta fora do formato)."""


def limpar(texto) -> str:
    """HTML do TCU em texto corrido: sem tags, entidades nem marcas de rodapé."""
    if not texto:
        return ''
    if isinstance(texto, list):
        texto = ' '.join(str(t) for t in texto)
    texto = re.sub(r'<br\s*/?>|</p>', '\n', str(texto), flags=re.I)
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = html.unescape(texto)
    texto = re.sub(r'\[footnoteRef:\d+\]', '', texto)
    texto = re.sub(r'[ \t\xa0]+', ' ', texto)
    return re.sub(r'\n\s*\n+', '\n\n', texto).strip()


def cortar(texto: str, limite: int) -> str:
    return texto if len(texto) <= limite else texto[:limite].rstrip() + f' […] (cortado em {limite} caracteres)'


def normalizar_colegiado(colegiado: Optional[str]) -> Optional[str]:
    """A API exige o nome exato, com acento: aceita "plenario", "1ª Câmara", "segunda camara" etc."""
    if not colegiado:
        return None
    chave = unicodedata.normalize('NFKD', colegiado).encode('ascii', 'ignore').decode().lower().strip()
    if chave.startswith('plen'):
        return 'Plenário'
    if chave.startswith(('primeira', '1')):
        return 'Primeira Câmara'
    if chave.startswith(('segunda', '2')):
        return 'Segunda Câmara'
    return colegiado.strip()


def link_acordao(numero: str, ano: str, colegiado: str) -> str:
    """Link do portal, no formato que a própria Pesquisa usa (filtro e ordenação codificados duas vezes)."""
    duplo = lambda s: urllib.parse.quote(urllib.parse.quote(s, safe=''), safe='')
    filtro = f'NUMACORDAO:{numero} ANOACORDAO:{ano} COLEGIADO:"{colegiado}"'
    return f'{PORTAL}/documento/acordao-completo/*/{duplo(filtro)}/{duplo("DTRELEVANCIA desc, NUMACORDAOINT desc")}/0'


def identificacao(doc: dict) -> str:
    return f"Acórdão {doc.get('NUMACORDAO', '?')}/{doc.get('ANOACORDAO', '?')}-{doc.get('COLEGIADO', '?')}"


# ---- Lei 14.133 (normas.leg.br) -----------------------------------------------------------------------------

NORMAS = 'https://normas.leg.br'
# Só a Lei 14.133 vem com texto estruturado no normas.leg.br (conferido em 2026-11-03); LC 123, CLT, Leis 8.666,
# 9.784 e 13.303 voltam só com metadados. Acrescente aqui quando a API passar a estruturar outra lei.
LEIS = {'14133': ('urn:lex:br:federal:lei:2021-04-01;14133', 'Lei 14.133/2021')}
AVISO_LEI = ('_Texto montado a partir do registro do Congresso Nacional no normas.leg.br, sem valor oficial (o '
             'oficial é o publicado no DOU). Transcreva só o que está acima e leia o dispositivo inteiro, com '
             'todos os incisos, antes de concluir._')
FALHA_LEI = ('A consulta ao texto da lei falhou (erro técnico: {motivo}). Não transcreva o dispositivo de memória: '
             'cite-o sem aspas e marque "a conferir".')
ROMANOS = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100}
STOPWORDS = {'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos', 'para', 'por', 'pela', 'pelo', 'que',
             'com', 'sem', 'aos', 'uma', 'umas', 'uns', 'ser', 'sua', 'seu', 'lei', 'art', 'artigo'}
_CACHE_LEIS: dict = {}  # urn -> (instante, Lei); vive enquanto o módulo estiver carregado no Open WebUI


@dataclass
class Dispositivo:
    chave: str  # identificador sem o prefixo da lei nem o sufixo da lei de origem, ex.: art121_par3_inc2
    rotulo: str
    texto: str
    nota: str
    link: str
    filhos: list = field(default_factory=list)
    vigente: bool = True
    suprimido: bool = False


def _data_br(data: str) -> str:
    partes = (data or '').split('-')
    return '/'.join(reversed(partes)) if len(partes) == 3 else (data or '?')


def versao_vigente(versoes: list) -> tuple:
    """A versão vigente é a mais recente sem a marca NotInForce: a API marca só as versões que saíram de vigor."""
    if not versoes:
        return {}, True
    em_vigor = [v for v in versoes if v.get('legislationLegalForce') != 'NotInForce']
    candidatas = em_vigor or versoes
    return max(candidatas, key=lambda v: v.get('legislationDate') or ''), bool(em_vigor)


def nota_da_versao(versao: dict, versoes: list) -> str:
    tipo = str(versao.get('legislationType') or '')
    if not tipo or tipo == 'Original_Version':
        return ''
    data = _data_br(versao.get('legislationDate'))
    origem = versao.get('legislationConsolidates')
    origem = limpar(origem.get('name')) if isinstance(origem, dict) and origem.get('name') else ''
    por = f' por {origem}' if origem else ''
    if 'Rejected_Veto' in tipo:
        return f'(veto derrubado; em vigor desde {data})'
    # Supressão de aplicabilidade afasta o dispositivo só na hipótese da norma de origem (ex.: art. 55 e a
    # MP 1.221/2024, calamidade): o texto continua em vigor, então é nota, nunca supressão.
    if 'Applicability_Suppression' in tipo:
        return f'(aplicação afastada em hipótese específica{por}, em {data}; o texto segue em vigor: confira o alcance)'
    if 'Suppression' in tipo:
        return f'(suprimido{por}, em {data})'
    if 'Court_Decision' in tipo:
        decisao = next((limpar(v['@reverse']['legislationCourtDecision'].get('name'))
                        for v in versoes if isinstance(v.get('@reverse'), dict)
                        and isinstance(v['@reverse'].get('legislationCourtDecision'), dict)), '')
        return f"(decisão judicial{' - ' + decisao if decisao else ''}, em {data}: confira a interpretação dada)"
    if 'Vetoed_Text_Change' in tipo:
        return f'(alteração de {data} vetada; redação mantida)'
    if 'Text_Restoration' in tipo:
        return f'(redação restabelecida em {data})'
    if 'Insertion' in tipo:
        return f'(incluído{por} em {data})'
    if 'Text_Indirect_Change' in tipo:
        return f'(alterado indiretamente{por} em {data})'
    if 'Text_Change' in tipo or 'Renumbering' in tipo:
        return f'(redação dada{por} em {data})'
    return f'(versão de {data})'


def texto_dispositivo(texto) -> str:
    """Tira a aspa de fechamento que sobra do texto da lei alteradora (ex.: art. 90, § 8º termina em ".'")."""
    texto = limpar(texto)
    for aspa in ("'", '”'):
        if texto.endswith(aspa) and texto.count(aspa) % 2 == 1:
            texto = texto[:-1].rstrip()
    return texto


def normalizar_busca(texto: str) -> str:
    """Minúsculas, sem acentos e sem pontuação: "Retenção" e "retencao" batem."""
    texto = unicodedata.normalize('NFKD', texto or '').encode('ascii', 'ignore').decode().lower()
    return ' '.join(re.sub(r'[^a-z0-9 ]+', ' ', texto).split())


def _raiz(palavra: str) -> str:
    """Radical por prefixo (palavra sem as 3 últimas letras, mínimo de 5): "impugnação" bate com "impugnar",
    "trabalhistas" com "trabalhista"; palavras curtas ficam inteiras para "conta" não bater com "contrato"."""
    return palavra if len(palavra) <= 5 else palavra[:max(5, len(palavra) - 3)]


def _trecho(texto: str, termos: list, tamanho: int = 260) -> str:
    normalizado = normalizar_busca(texto)
    pos = min((normalizado.find(t) for t in termos if t and normalizado.find(t) >= 0), default=0)
    inicio = max(0, pos - 60)
    trecho = texto[inicio:inicio + tamanho].strip()
    return ('…' if inicio else '') + trecho + ('…' if inicio + tamanho < len(texto) else '')


def _lista(valor) -> list:
    return valor if isinstance(valor, list) else [valor] if isinstance(valor, dict) else []


def montar_dispositivo(no: dict) -> Dispositivo:
    ident = no.get('legislationIdentifier') or ''
    chave = ident.split('!', 1)[1].split(',', 1)[0] if '!' in ident else ''
    versoes = _lista(no.get('workExample'))
    versao, vigente = versao_vigente(versoes)
    tipo = str(versao.get('legislationType') or '')
    rotulo = limpar(versao.get('name')) or next((limpar(v.get('name')) for v in reversed(versoes) if v.get('name')), '')
    texto = texto_dispositivo(versao.get('text'))
    if rotulo and texto.startswith(rotulo.rstrip('.') + ' '):  # a fonte repete o rótulo no texto (art. 121, § 4º)
        texto = texto[len(rotulo.rstrip('.')):].lstrip(' .')
    filhos = escolher_por_posicao([montar_dispositivo(f) for f in _lista(no.get('hasPart'))])
    return Dispositivo(chave=chave, rotulo=rotulo, texto=texto,
                       nota=nota_da_versao(versao, versoes) if vigente else '(sem versão em vigor)',
                       link=no.get('@id') or '', filhos=filhos, vigente=vigente,
                       suprimido='Suppression' in tipo and 'Applicability' not in tipo)


def escolher_por_posicao(filhos: list) -> list:
    """A mesma posição pode ter dois nós (ex.: art. 75, XVII inserido por MP depois suprimida e de novo por lei):
    fica o vigente e não suprimido, na ordem em que a posição aparece."""
    por_chave: dict = {}
    for d in filhos:
        atual = por_chave.get(d.chave)
        if atual is None or ((atual.suprimido or not atual.vigente) and d.vigente and not d.suprimido):
            por_chave[d.chave] = d
    return list(por_chave.values())


class Lei:
    def __init__(self, raiz: Dispositivo, urn: str, nome: str, data_registro: str):
        self.urn, self.nome, self.data_registro = urn, nome, data_registro
        self.artigos: dict = {}  # chave do artigo -> (Dispositivo, caminho na estrutura)
        self.trechos: list = []  # (citação, texto normalizado, texto original) de cada dispositivo com texto
        self._indexar(raiz, [])

    def _indexar(self, d: Dispositivo, caminho: list):
        if re.fullmatch(r'art\d+(-\d+)?', d.chave):
            if d.chave not in self.artigos:
                self.artigos[d.chave] = (d, caminho)
                self._indexar_trechos(d, d)
            return
        if re.match(r'(prt|liv|tit|cap|sec|sub)\d', d.chave):
            caminho = caminho + [' - '.join(x for x in (d.rotulo, d.texto) if x)]
        for f in d.filhos:
            self._indexar(f, caminho)

    def _indexar_trechos(self, artigo: Dispositivo, d: Dispositivo):
        if d.texto and not d.suprimido:
            self.trechos.append((rotulo_citacao('', artigo, d), normalizar_busca(d.texto), d.texto))
        for f in d.filhos:
            self._indexar_trechos(artigo, f)

    def buscar(self, termos: str, limite: int) -> tuple:
        """Dispositivos que contêm as frases entre aspas e mais palavras da consulta, em ordem de aderência."""
        frases = [normalizar_busca(f) for f in re.findall(r'"([^"]+)"', termos or '')]
        frases = [f for f in frases if f]
        soltas = [p for p in normalizar_busca(re.sub(r'"[^"]*"', ' ', termos or '')).split()
                  if p not in STOPWORDS and len(p) > 2]
        if not frases and not soltas:
            return [], 0
        consulta = ' '.join(soltas)
        tokens_por_trecho = [set(normalizado.split()) for _, normalizado, _ in self.trechos]
        # Termo raro pesa mais (como "impugnar" diante de "prazo" e "edital", que aparecem em toda a lei).
        peso = {}
        for p in soltas:
            presentes = sum(1 for tokens in tokens_por_trecho if any(t.startswith(_raiz(p)) for t in tokens))
            peso[p] = math.log((len(self.trechos) + 1) / (presentes + 1)) + 1
        achados = []
        for ordem, ((citacao, normalizado, original), tokens) in enumerate(zip(self.trechos, tokens_por_trecho)):
            if any(f not in normalizado for f in frases):
                continue
            # Palavra exata vale um pouco mais que o radical ("impugnar" para "impugnação"); as palavras na mesma
            # sequência da consulta ganham bônus.
            casadas = {p: (2 if p in tokens else 1.5) for p in soltas
                       if p in tokens or any(t.startswith(_raiz(p)) for t in tokens)}
            if soltas and len(casadas) < max(1, -(-len(soltas) // 2)):
                continue
            pontos = (10 * len(frases) + sum(peso[p] * v for p, v in casadas.items())
                      + (5 if len(soltas) > 1 and consulta in normalizado else 0))
            achados.append((-pontos, ordem, citacao, original))
        achados.sort()
        return [(c, o) for _, _, c, o in achados[:limite]], len(achados)

    @classmethod
    def de_json(cls, dados: dict, urn: str, nome: str) -> 'Lei':
        if not isinstance(dados, dict) or not dados.get('hasPart'):
            raise FalhaConsulta('a API não trouxe o texto estruturado da lei')
        raiz = Dispositivo(chave='', rotulo='', texto='', nota='', link='',
                           filhos=escolher_por_posicao([montar_dispositivo(f) for f in _lista(dados['hasPart'])]))
        return cls(raiz, urn, nome, _data_br(dados.get('dateModified')))


def normalizar_lei(lei: str) -> Optional[str]:
    """'14133', 'Lei 14.133', 'Lei nº 14.133/2021' ou a URN completa -> '14133', se a lei estiver na tabela."""
    valor = str(lei or '')
    if ';' in valor:
        valor = valor.rsplit(';', 1)[1]
    m = re.search(r'\d[\d.]*', valor)
    digitos = m.group(0).replace('.', '') if m else ''
    return digitos if digitos in LEIS else None


def _romano(valor: str) -> Optional[int]:
    valor = valor.lower()
    if not valor or any(c not in ROMANOS for c in valor):
        return None
    total = 0
    for i, c in enumerate(valor):
        n = ROMANOS[c]
        total += -n if i + 1 < len(valor) and ROMANOS[valor[i + 1]] > n else n
    return total


def _para_romano(n: int) -> str:
    saida = ''
    for valor, simbolo in ((100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'),
                           (4, 'IV'), (1, 'I')):
        while n >= valor:
            saida, n = saida + simbolo, n - valor
    return saida


def _numero(valor) -> Optional[str]:
    """'3', '§ 3º', 'II' -> '3' / '2'; com letra ('3º-A', 'IV-A') -> '3-1' / '4-1', como a API numera."""
    valor = re.sub(r'(?i)\b(inciso|inc|par[aá]grafo)\b|[\s.º°§ª]', '', str(valor or ''))
    m = re.fullmatch(r'([0-9]+|[ivxlcIVXLC]+)-?([a-zA-Z])?', valor)
    if not m:
        return None
    n = int(m.group(1)) if m.group(1).isdigit() else _romano(m.group(1))
    if not n:
        return None
    return f'{n}' + (f'-{ord(m.group(2).lower()) - 96}' if m.group(2) else '')


def _com_letra(numero: str, formato) -> str:
    """'3-1' -> formato(3) + '-A': rótulo de dispositivo inserido com letra."""
    base, _, letra = numero.partition('-')
    return formato(int(base)) + (f'-{chr(64 + int(letra))}' if letra.isdigit() else '')


def chave_artigo(artigo) -> Optional[str]:
    """'121' -> art121; '184-A' ou '184A' -> art184-1 (a API numera a letra)."""
    valor = re.sub(r'(?i)^\s*art(igo)?\.?\s*', '', str(artigo or '')).lower().replace('º', '').replace('°', '')
    m = re.fullmatch(r'\s*(\d+)\s*-?\s*([a-z])?\s*\.?\s*', valor)
    if not m:
        return None
    return f'art{int(m.group(1))}' + (f'-{ord(m.group(2)) - 96}' if m.group(2) else '')


def chave_dispositivo(artigo, paragrafo=None, inciso=None, alinea=None) -> Optional[str]:
    chave = chave_artigo(artigo)
    if not chave:
        return None
    if paragrafo not in (None, ''):
        if re.search(r'(?i)[uú]nico|^\s*u\s*$', str(paragrafo)):
            chave += '_par1u'
        else:
            n = _numero(paragrafo)
            if not n:
                return None
            chave += f'_par{n}'
    if inciso not in (None, ''):
        n = _numero(inciso)
        if not n:
            return None
        chave += ('' if '_par' in chave else '_cpt') + f'_inc{n}'
    if alinea not in (None, ''):
        letra = re.sub(r'[^a-z]', '', str(alinea).lower())
        if len(letra) != 1:
            return None
        chave += f'_ali{ord(letra) - 96}'
    return chave


def localizar(d: Dispositivo, chave: str) -> Optional[Dispositivo]:
    if d.chave == chave:
        return d
    for f in d.filhos:
        achado = localizar(f, chave)
        if achado:
            return achado
    return None


def renderizar(d: Dispositivo, nota_herdada: str = '') -> list:
    """Linhas no formato do texto oficial; o caput sai na mesma linha do rótulo do artigo. A nota que o pai já
    mostrou (ex.: artigo inteiro incluído por uma lei) não se repete em cada filho."""
    caput = next((f for f in d.filhos if f.chave.endswith('_cpt')), None)
    notas = []
    for nota in (d.nota, caput.nota if caput else ''):
        if nota and nota != nota_herdada and nota not in notas:
            notas.append(nota)
    linhas = [' '.join(p for p in [d.rotulo, caput.texto if caput else d.texto] + notas if p)]
    herdada = notas[-1] if notas else nota_herdada
    for f in (caput.filhos if caput else []) + [f for f in d.filhos if f is not caput]:
        linhas += renderizar(f, herdada)
    return [l for l in linhas if l]


def rotulo_citacao(nome_lei: str, artigo: Dispositivo, alvo: Dispositivo) -> str:
    partes = [nome_lei, re.sub(r'\.$', '', artigo.rotulo).replace('Art.', 'art.')]
    # O caput não entra na citação: "art. 121, inciso II" já é o inciso do caput.
    for trecho in alvo.chave.split('_')[1:]:
        if trecho == 'par1u':
            partes.append('parágrafo único')
        elif re.fullmatch(r'par\d+(-\d+)?', trecho):
            partes.append('§ ' + _com_letra(trecho[3:], lambda n: f'{n}º' if n < 10 else str(n)))
        elif re.fullmatch(r'inc\d+(-\d+)?', trecho):
            partes.append('inciso ' + _com_letra(trecho[3:], _para_romano))
        elif re.fullmatch(r'ali\d+', trecho):
            partes.append(f'alínea "{chr(96 + int(trecho[3:]))}"')
    return ', '.join(p for p in partes if p)


class Tools:
    class Valves(BaseModel):
        base_url: str = Field(default=f'{PORTAL}/rest/publico', description='API REST da Pesquisa do TCU')
        user_agent: str = Field(default='servfaz-fontes-oficiais/0.2 (+contato Servfaz)',
                                description='Identificação honesta do cliente; o firewall do TCU barra UA genérico')
        timeout_s: float = Field(default=20.0, description='Tempo máximo de cada consulta, em segundos')
        max_resultados: int = Field(default=10, description='Itens por página nas buscas')
        max_chars_texto: int = Field(default=12000, description='Limite de cada seção do inteiro teor')
        normas_url: str = Field(default=f'{NORMAS}/api/public', description='API do normas.leg.br (texto da lei)')
        cache_horas: float = Field(default=6.0, description='Por quanto tempo a lei baixada fica em cache')

    def __init__(self):
        self.valves = self.Valves()

    # ---- cliente HTTP -------------------------------------------------------------------------------------

    def _baixar_json(self, url: str):
        pedido = urllib.request.Request(url, headers={'User-Agent': self.valves.user_agent,
                                                      'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(pedido, timeout=self.valves.timeout_s) as resposta:
                corpo = resposta.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            raise FalhaConsulta(f'HTTP {e.code}') from e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise FalhaConsulta(f'rede ou tempo esgotado: {getattr(e, "reason", e)}') from e
        try:
            dados = json.loads(corpo)
        except ValueError as e:
            bloqueio = 'rejeitada' in corpo.lower() or corpo.lstrip().startswith('<')
            raise FalhaConsulta('acesso bloqueado (resposta em HTML)' if bloqueio else 'resposta inválida') from e
        return dados

    def _get_sync(self, base: str, endpoint: str, params: dict) -> dict:
        url = f"{self.valves.base_url.rstrip('/')}/base/{base}/{endpoint}?{urllib.parse.urlencode(params)}"
        try:
            dados = self._baixar_json(url)
        except FalhaConsulta as e:
            if 'HTML' in str(e):
                raise FalhaConsulta('acesso bloqueado pelo firewall do TCU') from e
            raise
        if not isinstance(dados, dict) or not isinstance(dados.get('documentos'), list):
            raise FalhaConsulta('resposta em formato inesperado')
        return dados

    async def _consultar(self, base: str, endpoint: str, termo: str, filtro: str = '', quantidade: int = 1,
                         inicio: int = 0, __event_emitter__=None) -> dict:
        await self._status(__event_emitter__, 'Consultando a Pesquisa do TCU…', False)
        params = {'termo': termo or '*', 'filtro': filtro, 'ordenacao': 'DTRELEVANCIA desc',
                  'quantidade': quantidade, 'inicio': inicio}
        try:
            return await asyncio.to_thread(self._get_sync, base, endpoint, params)
        finally:
            await self._status(__event_emitter__, 'Consulta ao TCU concluída', True)

    async def _carregar_lei(self, chave_lei: str, __event_emitter__=None) -> Lei:
        urn, nome = LEIS[chave_lei]
        guardada = _CACHE_LEIS.get(urn)
        if guardada and time.monotonic() - guardada[0] < self.valves.cache_horas * 3600:
            return guardada[1]
        await self._status(__event_emitter__, f'Consultando o texto da {nome} (normas.leg.br)…', False)
        url = (f"{self.valves.normas_url.rstrip('/')}/normas?"
               f"{urllib.parse.urlencode({'urn': urn, 'tipo_documento': 'maior-detalhe'})}")
        try:
            dados = await asyncio.to_thread(self._baixar_json, url)
            lei = Lei.de_json(dados, urn, nome)
        finally:
            await self._status(__event_emitter__, 'Consulta à lei concluída', True)
        _CACHE_LEIS[urn] = (time.monotonic(), lei)
        return lei

    @staticmethod
    async def _status(emitter, texto: str, fim: bool):
        if emitter:
            await emitter({'type': 'status', 'data': {'description': texto, 'done': fim}})

    def _rodape_paginacao(self, dados: dict, pagina: int, mostrados: int) -> str:
        total = dados.get('quantidadeEncontrada') or 0
        inicio = pagina * self.valves.max_resultados
        linha = f'Mostrando {inicio + 1}–{inicio + mostrados} de {total} resultado(s).'
        if inicio + mostrados < total:
            linha += f' Para ver mais, repita a busca com pagina={pagina + 1}.'
        return linha

    # ---- tools --------------------------------------------------------------------------------------------

    async def buscar_jurisprudencia_selecionada(self, tema: str, pagina: int = 0, __event_emitter__=None) -> str:
        """
        Busca enunciados da Jurisprudência Selecionada do TCU (teses curadas, cada uma com o acórdão de origem).
        Use como primeiro passo para fundamentar um vício de edital, contrato ou julgamento.
        Use frases curtas entre aspas (ex.: "retenção de pagamento" "regularidade fiscal").
        Depois, abra o acórdão de origem com obter_acordao_tcu antes de citar.
        :param tema: termos jurídicos do vício, de preferência frases entre aspas.
        :param pagina: página de resultados, começando em 0.
        """
        pagina = max(int(pagina or 0), 0)
        try:
            dados = await self._consultar('jurisprudencia-selecionada', 'documentosResumidos', tema, '',
                                          self.valves.max_resultados, pagina * self.valves.max_resultados,
                                          __event_emitter__)
        except FalhaConsulta as e:
            return FALHA.format(motivo=e)
        docs = dados['documentos']
        if not docs:
            return NENHUM
        linhas = [f'## Jurisprudência Selecionada do TCU — {tema}', '']
        for i, doc in enumerate(docs, start=pagina * self.valves.max_resultados + 1):
            classificacao = ' > '.join(limpar(doc.get(c)) for c in ('AREA', 'TEMA', 'SUBTEMA') if limpar(doc.get(c)))
            linhas.append(f'{i}. **{limpar(doc.get("ENUNCIADO"))}**')
            linhas.append(f"   - Origem: {identificacao(doc)}, sessão de {doc.get('DATASESSAOFORMATADA', '?')}"
                          f" · [abrir acórdão]({link_acordao(doc.get('NUMACORDAO'), doc.get('ANOACORDAO'), doc.get('COLEGIADO'))})")
            if classificacao:
                linhas.append(f'   - Classificação: {classificacao}')
        linhas += ['', self._rodape_paginacao(dados, pagina, len(docs)),
                   'O enunciado é resumo do TCU: leia a deliberação e o voto do acórdão de origem antes de citar.',
                   '', AVISO]
        return '\n'.join(linhas)

    async def buscar_sumulas_tcu(self, termo: str, __event_emitter__=None) -> str:
        """
        Busca súmulas do TCU por número (ex.: "254") ou por assunto (ex.: "parcelamento do objeto").
        Traz o enunciado, se está vigente e o fundamento legal com os precedentes.
        :param termo: número da súmula ou termos do assunto.
        """
        termo = (termo or '').strip()
        numero = re.fullmatch(r'(?:s[uú]mula\s*)?(\d{1,4})', termo, flags=re.I)
        try:
            if numero:
                dados = await self._consultar('sumula', 'documento', '*', f'NUMERO:{numero.group(1)}', 1, 0,
                                              __event_emitter__)
            else:
                dados = await self._consultar('sumula', 'documento', termo, '', min(self.valves.max_resultados, 5),
                                              0, __event_emitter__)
        except FalhaConsulta as e:
            return FALHA.format(motivo=e)
        docs = dados['documentos']
        if not docs:
            return NENHUM
        linhas = [f'## Súmulas do TCU — {termo}', '']
        for doc in docs:
            vigente = 'vigente' if str(doc.get('VIGENTE', '')).lower() == 'true' else 'NÃO vigente'
            linhas.append(f"### Súmula TCU {limpar(doc.get('NUMERO'))} ({vigente})")
            linhas.append(limpar(doc.get('CABECALHO')) or limpar(doc.get('ENUNCIADO')))
            aprovacao = f"Aprovada pelo Acórdão {doc.get('NUMAPROVACAO', '?')}/{doc.get('ANOAPROVACAO', '?')}-{doc.get('COLEGIADO', '?')}"
            linhas.append(f'- {aprovacao}')
            excerto = limpar(doc.get('EXCERTO'))
            if excerto:
                linhas.append(f'- Fundamento e precedentes: {cortar(excerto, 1500)}')
            linhas.append('')
        if (dados.get('quantidadeEncontrada') or 0) > len(docs):
            linhas.append(f"Mostrando {len(docs)} de {dados['quantidadeEncontrada']}; refine o termo para ver outras.")
        linhas += ['', AVISO]
        return '\n'.join(linhas)

    async def buscar_acordaos_tcu(self, consulta: str, ano_minimo: Optional[int] = None,
                                  colegiado: Optional[str] = None, pagina: int = 0,
                                  __event_emitter__=None) -> str:
        """
        Busca acórdãos do TCU por texto. Use quando a jurisprudência selecionada e as súmulas não bastarem
        ou para achar precedentes recentes. Prefira frases exatas entre aspas, unidas por espaço
        (ex.: "atestado de capacidade técnica" "tempo mínimo"); palavras soltas trazem resultado ruidoso.
        Resultados vêm dos mais recentes para os mais antigos. Não inclua dados do cliente na consulta.
        :param consulta: termos jurídicos, de preferência frases entre aspas.
        :param ano_minimo: só acórdãos deste ano em diante (ex.: 2021, para a Lei 14.133).
        :param colegiado: "Plenário", "Primeira Câmara" ou "Segunda Câmara".
        :param pagina: página de resultados, começando em 0.
        """
        filtros = []
        if ano_minimo:
            filtros.append(f'ANOACORDAO:[{int(ano_minimo)} TO *]')
        if colegiado:
            filtros.append(f'COLEGIADO:"{normalizar_colegiado(colegiado)}"')
        pagina = max(int(pagina or 0), 0)
        try:
            dados = await self._consultar('acordao-completo', 'documentosResumidos', consulta, ' '.join(filtros),
                                          self.valves.max_resultados, pagina * self.valves.max_resultados,
                                          __event_emitter__)
        except FalhaConsulta as e:
            return FALHA.format(motivo=e)
        docs = dados['documentos']
        if not docs:
            return NENHUM
        linhas = [f'## Acórdãos do TCU — {consulta}', '']
        for i, doc in enumerate(docs, start=pagina * self.valves.max_resultados + 1):
            ident = identificacao(doc)
            linhas.append(f"{i}. **{ident}** — sessão de {doc.get('DATASESSAO', '?')}")
            sumario = limpar(doc.get('SUMARIO'))
            if sumario:
                linhas.append(f'   - Sumário: {cortar(sumario, 600)}')
            trecho = limpar(doc.get('FRAGMENTO1'))
            if trecho:
                linhas.append(f'   - Trecho encontrado: {cortar(trecho, 400)}')
            linhas.append(f"   - [Abrir no portal]({link_acordao(doc.get('NUMACORDAO'), doc.get('ANOACORDAO'), doc.get('COLEGIADO'))})")
        linhas += ['', self._rodape_paginacao(dados, pagina, len(docs)),
                   'Para ler o inteiro teor, use obter_acordao_tcu com número, ano e colegiado.', '', AVISO]
        return '\n'.join(linhas)

    async def obter_acordao_tcu(self, numero: str, ano: str, colegiado: str, __event_emitter__=None) -> str:
        """
        Abre o inteiro teor de um acórdão do TCU (sumário, deliberação e voto; relatório resumido).
        Use antes de citar qualquer acórdão em impugnação, esclarecimento ou recurso.
        :param numero: número do acórdão, ex.: "2924".
        :param ano: ano do acórdão, ex.: "2026".
        :param colegiado: "Plenário", "Primeira Câmara" ou "Segunda Câmara".
        """
        colegiado = normalizar_colegiado(colegiado) or ''
        filtro = f'NUMACORDAO:{str(numero).strip()} ANOACORDAO:{str(ano).strip()}'
        if colegiado:
            filtro += f' COLEGIADO:"{colegiado}"'
        try:
            dados = await self._consultar('acordao-completo', 'documento', '*', filtro, 1, 0, __event_emitter__)
        except FalhaConsulta as e:
            return FALHA.format(motivo=e)
        docs = dados['documentos']
        if not docs:
            return f'Acórdão {numero}/{ano}-{colegiado or "?"} não encontrado na Pesquisa do TCU. Confira número, ano e colegiado.'
        if (dados.get('quantidadeEncontrada') or 0) > 1 and not colegiado:
            return (f'Há mais de um Acórdão {numero}/{ano} (um por colegiado). Informe o colegiado: '
                    + ', '.join(COLEGIADOS) + '.')
        doc = docs[0]
        limite = self.valves.max_chars_texto
        # Campos com nomes de partes, advogados e quórum ficam de fora (LGPD); o relator entra como autoria.
        partes = [f"# {identificacao(doc)}", '',
                  f"- Sessão: {doc.get('DATASESSAO', '?')} · Situação: {doc.get('SITUACAO', '?')}",
                  f"- Tipo de processo: {limpar(doc.get('TIPOPROCESSO')) or '?'} · Relator: {limpar(doc.get('RELATOR')) or '?'}",
                  f"- Assunto: {cortar(limpar(doc.get('ASSUNTO')), 800) or '?'}",
                  f"- [Abrir no portal]({link_acordao(doc.get('NUMACORDAO'), doc.get('ANOACORDAO'), doc.get('COLEGIADO'))})"]
        if doc.get('URLARQUIVOPDF'):
            partes.append(f"- [PDF oficial]({doc['URLARQUIVOPDF']})")
        for titulo, campo, maximo in (('Sumário', 'SUMARIO', limite), ('Acórdão (deliberação)', 'ACORDAO', limite),
                                      ('Voto', 'VOTO', limite), ('Relatório (trecho)', 'RELATORIO', limite // 3)):
            texto = limpar(doc.get(campo))
            if texto:
                partes += ['', f'## {titulo}', cortar(texto, maximo)]
        partes += ['', AVISO]
        return '\n'.join(partes)

    async def obter_dispositivo_lei(self, lei: str, artigo: str, paragrafo: Optional[str] = None,
                                    inciso: Optional[str] = None, alinea: Optional[str] = None,
                                    __event_emitter__=None) -> str:
        """
        Traz o texto vigente de um artigo (ou parágrafo, inciso, alínea) da Lei 14.133/2021, para transcrever
        a lei na peça. Use sempre antes de citar ou transcrever um dispositivo: não cite lei de memória.
        Sem parágrafo, devolve o artigo inteiro; leia todos os incisos antes de concluir.
        :param lei: "14133" (por enquanto só a Lei 14.133/2021 está disponível).
        :param artigo: número do artigo, ex.: "121" ou "184-A".
        :param paragrafo: número do parágrafo (ex.: "3") ou "único".
        :param inciso: inciso em romanos ou arábicos (ex.: "II" ou "2").
        :param alinea: letra da alínea (ex.: "a").
        """
        chave_lei = normalizar_lei(lei)
        if not chave_lei:
            disponiveis = ', '.join(nome for _, nome in LEIS.values())
            return (f'A consulta de legislação só tem o texto estruturado de: {disponiveis}. Para "{lei}", cite '
                    'sem aspas e marque "a conferir".')
        chave = chave_dispositivo(artigo, paragrafo, inciso, alinea)
        if not chave:
            return 'Dispositivo inválido: informe o artigo em números (ex.: "121" ou "184-A") e, se quiser, parágrafo, inciso e alínea.'
        try:
            texto_lei = await self._carregar_lei(chave_lei, __event_emitter__)
        except FalhaConsulta as e:
            return FALHA_LEI.format(motivo=e)
        artigo_d, caminho = texto_lei.artigos.get(chave.split('_', 1)[0], (None, []))
        alvo = localizar(artigo_d, chave) if artigo_d else None
        if not alvo:
            return (f'Dispositivo não encontrado na {texto_lei.nome}: artigo {artigo}'
                    + (f', parágrafo {paragrafo}' if paragrafo else '') + (f', inciso {inciso}' if inciso else '')
                    + (f', alínea {alinea}' if alinea else '') + '. Confira a numeração; não cite de memória.')
        linhas = renderizar(alvo)
        if alvo is not artigo_d:
            caput = next((f for f in artigo_d.filhos if f.chave.endswith('_cpt')), None)
            contexto = ' '.join(p for p in (artigo_d.rotulo, caput.texto if caput else '') if p)
            linhas = [contexto, '[…]'] + linhas
        corpo = '\n'.join(linhas)
        if len(corpo) > self.valves.max_chars_texto:
            corpo = (cortar(corpo, self.valves.max_chars_texto)
                     + '\nPeça um parágrafo ou inciso específico para ler o restante.')
        partes = [f'## {rotulo_citacao(texto_lei.nome, artigo_d, alvo)}']
        if caminho:
            partes.append(f"Localização: {' > '.join(caminho)}")
        partes += [f'Fonte: normas.leg.br (Congresso Nacional), registro de {texto_lei.data_registro} · '
                   f'[abrir]({alvo.link or artigo_d.link})', '', corpo, '', AVISO_LEI]
        return '\n'.join(partes)

    async def buscar_na_lei(self, lei: str, termos: str, __event_emitter__=None) -> str:
        """
        Procura no texto vigente da Lei 14.133/2021 os dispositivos sobre um assunto, quando não se sabe o número
        do artigo (ex.: "conta vinculada", "retenção pagamento obrigações trabalhistas"). Depois, abra o artigo
        encontrado com obter_dispositivo_lei antes de citar: o resultado aqui é só um trecho.
        :param lei: "14133" (por enquanto só a Lei 14.133/2021 está disponível).
        :param termos: palavras do assunto; frases exatas entre aspas (ex.: "dedicação exclusiva").
        """
        chave_lei = normalizar_lei(lei)
        if not chave_lei:
            disponiveis = ', '.join(nome for _, nome in LEIS.values())
            return (f'A consulta de legislação só tem o texto estruturado de: {disponiveis}. Para "{lei}", cite '
                    'sem aspas e marque "a conferir".')
        try:
            texto_lei = await self._carregar_lei(chave_lei, __event_emitter__)
        except FalhaConsulta as e:
            return FALHA_LEI.format(motivo=e)
        achados, total = texto_lei.buscar(termos, self.valves.max_resultados)
        if not achados:
            return (f'Nenhum dispositivo da {texto_lei.nome} contém esses termos. Tente sinônimos ou menos palavras; '
                    'não conclua que a lei não trata do assunto só por esta busca.')
        destaque = [normalizar_busca(f) for f in re.findall(r'"([^"]+)"', termos)] + \
                   [_raiz(p) for p in normalizar_busca(termos.replace('"', ' ')).split() if p not in STOPWORDS]
        destaque.sort(key=len, reverse=True)
        linhas = [f'## {texto_lei.nome}: dispositivos sobre "{termos}"', '']
        for i, (citacao, original) in enumerate(achados, start=1):
            linhas.append(f'{i}. **{citacao}**: {_trecho(original, destaque)}')
        linhas += ['', f'Mostrando {len(achados)} de {total} dispositivo(s), dos mais aderentes aos menos.',
                   'Abra o artigo com obter_dispositivo_lei antes de citar e leia todos os incisos.', '', AVISO_LEI]
        return '\n'.join(linhas)
