"""
title: Jurisprudência TCU Servfaz
description: Pesquisa acórdãos, jurisprudência selecionada e súmulas na Pesquisa de Jurisprudência do TCU para fundamentar impugnações e recursos.
author: Servfaz
version: 0.1.0
"""
# Import manual em Workspace > Tools; Function Calling = Native no modelo (ver ../INSTALACAO.md).
# Usa a API REST pública por trás de pesquisa.apps.tcu.gov.br. O firewall do TCU barra User-Agent genérico
# (ex.: o padrão do curl), respondendo HTTP 200 com HTML de bloqueio: por isso o UA próprio e honesto nas Valves,
# e HTML no lugar de JSON é tratado como falha técnica, nunca como "nenhum resultado".
import asyncio
import html
import json
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from pydantic import BaseModel, Field

PORTAL = 'https://pesquisa.apps.tcu.gov.br'
AVISO = ('_Resultado da Pesquisa de Jurisprudência do TCU. É candidato, não prova: abra o inteiro teor, '
         'confira deliberação, lei aplicada e contexto antes de citar._')
NENHUM = 'Nenhum resultado na Pesquisa do TCU para esta consulta. Tente frases mais curtas, entre aspas, ou outro termo.'
FALHA = ('A consulta ao TCU falhou (erro técnico: {motivo}). Não foi possível pesquisar agora; informe isso ao '
         'usuário e não conclua que não há jurisprudência sobre o tema.')
COLEGIADOS = ('Plenário', 'Primeira Câmara', 'Segunda Câmara')


class FalhaTCU(Exception):
    """Erro técnico na consulta (HTTP, rede, timeout ou bloqueio do firewall)."""


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


class Tools:
    class Valves(BaseModel):
        base_url: str = Field(default=f'{PORTAL}/rest/publico', description='API REST da Pesquisa do TCU')
        user_agent: str = Field(default='servfaz-tcu-tool/0.1 (+contato Servfaz)',
                                description='Identificação honesta do cliente; o firewall do TCU barra UA genérico')
        timeout_s: float = Field(default=20.0, description='Tempo máximo de cada consulta, em segundos')
        max_resultados: int = Field(default=10, description='Itens por página nas buscas')
        max_chars_texto: int = Field(default=12000, description='Limite de cada seção do inteiro teor')

    def __init__(self):
        self.valves = self.Valves()

    # ---- cliente HTTP -------------------------------------------------------------------------------------

    def _get_sync(self, base: str, endpoint: str, params: dict) -> dict:
        url = f"{self.valves.base_url.rstrip('/')}/base/{base}/{endpoint}?{urllib.parse.urlencode(params)}"
        pedido = urllib.request.Request(url, headers={'User-Agent': self.valves.user_agent,
                                                      'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(pedido, timeout=self.valves.timeout_s) as resposta:
                corpo = resposta.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            raise FalhaTCU(f'HTTP {e.code}') from e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise FalhaTCU(f'rede ou tempo esgotado: {getattr(e, "reason", e)}') from e
        try:
            dados = json.loads(corpo)
        except ValueError as e:
            bloqueio = 'rejeitada' in corpo.lower() or corpo.lstrip().startswith('<')
            raise FalhaTCU('acesso bloqueado pelo firewall do TCU' if bloqueio else 'resposta inválida') from e
        if not isinstance(dados, dict) or not isinstance(dados.get('documentos'), list):
            raise FalhaTCU('resposta em formato inesperado')
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
        except FalhaTCU as e:
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
        except FalhaTCU as e:
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
        except FalhaTCU as e:
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
        except FalhaTCU as e:
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
