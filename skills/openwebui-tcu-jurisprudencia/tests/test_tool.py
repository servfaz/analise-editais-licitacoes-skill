import asyncio
import importlib.util
import io
import json
import unittest
import urllib.error
import urllib.parse
from pathlib import Path
from unittest import mock

PACOTE = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('tcu_jurisprudencia', PACOTE / 'tools' / 'tcu_jurisprudencia.py')
tcu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tcu)
# A nova tentativa espera 1 s entre chamadas; nos testes, sem espera.
mock.patch.object(tcu.time, 'sleep', lambda *_: None).start()

# Respostas no formato da API conferido em 2026-10-30, com dados fictícios (sem nomes reais).
ACORDAO_RESUMIDO = {
    'KEY': 'ACORDAO-COMPLETO-1', 'NUMACORDAO': '1505', 'ANOACORDAO': '2026', 'COLEGIADO': 'Plenário',
    'DATASESSAO': '10/06/2026', 'SUMARIO': 'AUDITORIA. <em>RETENÇÃO</em> DE PAGAMENTO.',
    'FRAGMENTO1': '...vedada a <em>retenção</em> de pagamento...',
}
ACORDAO_COMPLETO = {
    **ACORDAO_RESUMIDO, 'SITUACAO': 'OFICIALIZADO', 'TIPOPROCESSO': 'RELATÓRIO DE AUDITORIA (RA)',
    'RELATOR': 'RELATOR FICTICIO', 'ASSUNTO': 'Auditoria de conformidade.',
    'ACORDAO': '<p>9.1. determinar ao órgão que&nbsp;se abstenha de reter pagamentos;</p>',
    'VOTO': '<p>Em exame, auditoria.[footnoteRef:3] Ante o exposto...</p>',
    'RELATORIO': '<p>' + 'x' * 10000 + '</p>',
    'ADVOGADO': 'Fulano de Tal (OAB/XX 000)', 'INTERESSADOS': 'Beltrano', 'QUORUM': 'Ministros presentes: Sicrano',
    'URLARQUIVOPDF': 'https://contas.tcu.gov.br/sagas/exemplo.pdf',
}


def resposta(corpo):
    corpo = corpo if isinstance(corpo, str) else json.dumps(corpo)
    r = io.BytesIO(corpo.encode('utf-8'))
    r.__enter__ = lambda *a: r
    r.__exit__ = lambda *a: False
    return mock.MagicMock(**{'__enter__.return_value': r})


def pagina(docs, total=None):
    return {'quantidadeEncontrada': len(docs) if total is None else total, 'inicio': 0, 'documentos': docs}


def rodar(coro):
    return asyncio.run(coro)


class BuscarAcordaos(unittest.TestCase):
    def setUp(self):
        self.tools = tcu.Tools()
        self.tools.valves.max_resultados = 2

    def chamar(self, corpo, **kwargs):
        with mock.patch.object(tcu.urllib.request, 'urlopen', return_value=resposta(corpo)) as urlopen:
            texto = rodar(self.tools.buscar_acordaos_tcu(**kwargs))
        pedido = urlopen.call_args[0][0]
        return texto, pedido

    def test_formata_resultado_com_link_e_sem_html(self):
        texto, _ = self.chamar(pagina([ACORDAO_RESUMIDO], total=5), consulta='"retenção de pagamento"')
        self.assertIn('**Acórdão 1505/2026-Plenário** — sessão de 10/06/2026', texto)
        self.assertIn('RETENÇÃO DE PAGAMENTO', texto)
        self.assertNotIn('<em>', texto)
        self.assertIn('/documento/acordao-completo/*/NUMACORDAO%253A1505', texto)
        self.assertIn('pagina=1', texto)
        self.assertIn(tcu.AVISO, texto)
        self.assertIn('sentido contrário', texto)

    def test_monta_filtros_paginacao_e_user_agent(self):
        _, pedido = self.chamar(pagina([ACORDAO_RESUMIDO]), consulta='"x"', ano_minimo=2021,
                                colegiado='plenario', pagina=3)
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(pedido.full_url).query)
        self.assertEqual(params['filtro'], ['ANOACORDAO:[2021 TO *] COLEGIADO:"Plenário"'])
        self.assertEqual(params['inicio'], ['6'])
        self.assertEqual(params['quantidade'], ['2'])
        self.assertIn('/base/acordao-completo/documentosResumidos', pedido.full_url)
        self.assertEqual(pedido.get_header('User-agent'), self.tools.valves.user_agent)

    def test_sem_resultado_e_diferente_de_falha(self):
        texto, _ = self.chamar(pagina([]), consulta='"inexistente"')
        self.assertEqual(texto, tcu.NENHUM)

    def test_html_de_bloqueio_vira_falha_tecnica(self):
        texto, _ = self.chamar('<html><body>Requisição rejeitada</body></html>', consulta='x')
        self.assertIn('falhou', texto)
        self.assertIn('firewall', texto)
        self.assertIn('de memória', texto)
        self.assertNotEqual(texto, tcu.NENHUM)

    def test_nova_tentativa_quando_o_tcu_nao_responde(self):
        corpo = resposta(pagina([ACORDAO_RESUMIDO]))
        with mock.patch.object(tcu.urllib.request, 'urlopen', side_effect=[TimeoutError('timed out'), corpo]) as u:
            texto = rodar(self.tools.buscar_acordaos_tcu(consulta='x'))
        self.assertEqual(u.call_count, 2)
        self.assertIn('Acórdão 1505/2026-Plenário', texto)

    def test_desiste_depois_das_tentativas(self):
        with mock.patch.object(tcu.urllib.request, 'urlopen', side_effect=TimeoutError('timed out')) as u:
            texto = rodar(self.tools.buscar_acordaos_tcu(consulta='x'))
        self.assertEqual(u.call_count, 3)
        self.assertIn('após 3 tentativa(s)', texto)

    def test_erro_http_do_cliente_nao_repete(self):
        erro = urllib.error.HTTPError('u', 404, 'não encontrado', {}, None)
        with mock.patch.object(tcu.urllib.request, 'urlopen', side_effect=erro) as u:
            texto = rodar(self.tools.buscar_acordaos_tcu(consulta='x'))
        self.assertEqual(u.call_count, 1)
        self.assertIn('HTTP 404', texto)

    def test_falha_e_vazio_trazem_o_plano_b_com_os_niveis(self):
        falha, _ = self.chamar('<html>Requisição rejeitada</html>', consulta='x')
        vazio, _ = self.chamar(pagina([]), consulta='x')
        for texto in (falha, vazio):
            self.assertIn('site:tcu.gov.br', texto)
            self.assertIn('A = o próprio acórdão em pesquisa.apps.tcu.gov.br', texto)
            self.assertIn('nunca de memória, nem de outro tribunal', texto)
            self.assertIn('O trecho do resultado de busca não é fonte aberta', texto)
            self.assertIn('na resposta, não mostre as letras', texto)
            self.assertIn('urn:lex:br:tribunal.contas.uniao', texto)
            self.assertIn('nunca vai entre aspas nem como ementa', texto)
            self.assertIn('confiança em palavras (alta, média ou baixa)', texto)
            self.assertIn('licitacoesecontratos.tcu.gov.br', texto.split('B = ')[1].split('C = ')[0])
            self.assertIn('a conferir', texto)

    def test_erro_http_vira_falha_tecnica(self):
        erro = urllib.error.HTTPError('u', 503, 'indisponível', {}, None)
        with mock.patch.object(tcu.urllib.request, 'urlopen', side_effect=erro):
            texto = rodar(self.tools.buscar_acordaos_tcu(consulta='x'))
        self.assertIn('HTTP 503', texto)


class ObterAcordao(unittest.TestCase):
    def setUp(self):
        self.tools = tcu.Tools()
        self.tools.valves.max_chars_texto = 3000

    def chamar(self, corpo, **kwargs):
        with mock.patch.object(tcu.urllib.request, 'urlopen', return_value=resposta(corpo)) as urlopen:
            texto = rodar(self.tools.obter_acordao_tcu(**kwargs))
        return texto, urlopen.call_args[0][0]

    def test_inteiro_teor_limpo_sem_dados_pessoais(self):
        texto, pedido = self.chamar(pagina([ACORDAO_COMPLETO]), numero='1505', ano='2026', colegiado='plenário')
        self.assertIn('# Acórdão 1505/2026-Plenário', texto)
        self.assertIn('9.1. determinar ao órgão que se abstenha', texto)
        self.assertNotIn('footnoteRef', texto)
        self.assertIn('cortado em 1000 caracteres', texto)
        for pessoal in ('Fulano', 'Beltrano', 'Sicrano'):
            self.assertNotIn(pessoal, texto)
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(pedido.full_url).query)
        self.assertEqual(params['filtro'], ['NUMACORDAO:1505 ANOACORDAO:2026 COLEGIADO:"Plenário"'])
        self.assertIn('/base/acordao-completo/documento?', pedido.full_url)

    def test_nao_encontrado(self):
        texto, _ = self.chamar(pagina([]), numero='1', ano='1900', colegiado='Plenário')
        self.assertIn('não encontrado', texto)

    def test_pede_colegiado_quando_ha_mais_de_um(self):
        texto, _ = self.chamar(pagina([ACORDAO_COMPLETO], total=2), numero='1505', ano='2026', colegiado='')
        self.assertIn('Informe o colegiado', texto)


ENUNCIADO = {
    'KEY': 'JURISPRUDENCIA-SELECIONADA-1', 'NUMACORDAO': '1505', 'ANOACORDAO': '2026', 'COLEGIADO': 'Plenário',
    'AREA': 'Contrato Administrativo', 'TEMA': 'Execução de contrato', 'SUBTEMA': 'Regularidade fiscal',
    'ENUNCIADO': 'É vedada a <em>retenção</em> de pagamento por irregularidade fiscal.',
    'DATASESSAOFORMATADA': '10/06/2026', 'AUTORTESE': 'RELATOR FICTICIO',
}
SUMULA = {
    'KEY': 'SUMULA-1', 'NUMERO': '<em>254</em>', 'VIGENTE': 'true', 'NUMAPROVACAO': '625', 'ANOAPROVACAO': '2010',
    'COLEGIADO': 'Plenário', 'CABECALHO': 'O IRPJ e a CSLL não se consubstanciam em despesa indireta.',
    'EXCERTO': '<p><b>Fundamento legal:</b></p><p>- Lei 9.430/1996.</p>',
}


class BuscarJurisprudenciaSelecionada(unittest.TestCase):
    def test_enunciado_com_acordao_de_origem(self):
        tools = tcu.Tools()
        with mock.patch.object(tcu.urllib.request, 'urlopen', return_value=resposta(pagina([ENUNCIADO]))) as u:
            texto = rodar(tools.buscar_jurisprudencia_selecionada(tema='"retenção de pagamento"'))
        self.assertIn('**É vedada a retenção de pagamento por irregularidade fiscal.**', texto)
        self.assertIn('Origem: Acórdão 1505/2026-Plenário, sessão de 10/06/2026', texto)
        self.assertIn('Contrato Administrativo > Execução de contrato > Regularidade fiscal', texto)
        self.assertIn('/base/jurisprudencia-selecionada/documentosResumidos', u.call_args[0][0].full_url)

    def test_vazio(self):
        with mock.patch.object(tcu.urllib.request, 'urlopen', return_value=resposta(pagina([]))):
            texto = rodar(tcu.Tools().buscar_jurisprudencia_selecionada(tema='x'))
        self.assertEqual(texto, tcu.NENHUM)


class BuscarSumulas(unittest.TestCase):
    def chamar(self, termo, corpo):
        with mock.patch.object(tcu.urllib.request, 'urlopen', return_value=resposta(corpo)) as u:
            texto = rodar(tcu.Tools().buscar_sumulas_tcu(termo=termo))
        return texto, urllib.parse.parse_qs(urllib.parse.urlsplit(u.call_args[0][0].full_url).query)

    def test_por_numero_usa_filtro(self):
        texto, params = self.chamar('Súmula 254', pagina([SUMULA]))
        self.assertEqual(params['filtro'], ['NUMERO:254'])
        self.assertIn('### Súmula TCU 254 (vigente)', texto)
        self.assertIn('Aprovada pelo Acórdão 625/2010-Plenário', texto)
        self.assertIn('Lei 9.430/1996', texto)

    def test_por_assunto_usa_termo(self):
        _, params = self.chamar('parcelamento do objeto', pagina([{**SUMULA, 'VIGENTE': 'false'}]))
        self.assertEqual(params['termo'], ['parcelamento do objeto'])
        self.assertNotIn('filtro', params)

    def test_sumula_nao_vigente_sinalizada(self):
        texto, _ = self.chamar('254', pagina([{**SUMULA, 'VIGENTE': 'false'}]))
        self.assertIn('NÃO vigente', texto)


class Auxiliares(unittest.TestCase):
    def test_link_no_formato_do_portal(self):
        esperado = ('https://pesquisa.apps.tcu.gov.br/documento/acordao-completo/*/NUMACORDAO%253A2924%2520'
                    'ANOACORDAO%253A2026%2520COLEGIADO%253A%2522Plen%25C3%25A1rio%2522/'
                    'DTRELEVANCIA%2520desc%252C%2520NUMACORDAOINT%2520desc/0')
        self.assertEqual(tcu.link_acordao('2924', '2026', 'Plenário'), esperado)

    def test_normaliza_colegiado(self):
        self.assertEqual(tcu.normalizar_colegiado('PLENARIO'), 'Plenário')
        self.assertEqual(tcu.normalizar_colegiado('1ª Câmara'), 'Primeira Câmara')
        self.assertEqual(tcu.normalizar_colegiado('segunda camara'), 'Segunda Câmara')
        self.assertIsNone(tcu.normalizar_colegiado(''))


# Lei fictícia no formato do normas.leg.br conferido em 2026-11-03: um nó por dispositivo, versões em workExample.
URN = 'urn:lex:br:federal:lei:2021-04-01;14133'


def versao(texto=None, nome=None, tipo='Original_Version', data='2021-04-01', fora=False, origem=None, **extra):
    v = {'legislationType': tipo, 'legislationDate': data, **extra}
    if texto is not None:
        v['text'] = texto
    if nome:
        v['name'] = nome
    if fora:
        v['legislationLegalForce'] = 'NotInForce'
    if origem:
        v['legislationConsolidates'] = {'name': origem}
    return v


def no(chave, versoes, filhos=(), sufixo=''):
    d = {'legislationIdentifier': f'{URN}!{chave}{sufixo}', '@id': f'https://normas.leg.br/?urn={URN}!{chave}',
         'workExample': versoes if isinstance(versoes, list) else versoes}
    if filhos:
        d['hasPart'] = list(filhos)
    return d


LEI_FICTICIA = {
    'dateModified': '2026-07-20',
    'hasPart': {'legislationIdentifier': f'{URN}!', 'hasPart': [
        no('tit1', versao('DISPOSIÇÕES DE TESTE', 'TÍTULO I'), [
            no('tit1_cap1', versao('DO PAGAMENTO', 'CAPÍTULO I'), [
                no('art1', versao(nome='Art. 1º'), [
                    no('art1_cpt', versao('A Administração poderá, entre outras medidas:'), [
                        no('art1_cpt_inc1', versao('exigir garantia;', 'I –')),
                        no('art1_cpt_inc2', versao('condicionar o pagamento à quitação;', 'II –')),
                    ]),
                    no('art1_par1', [versao('(VETADO).', '§ 1º', fora=True),
                                     versao('Texto restaurado pelo Congresso.', '§ 1º', 'Rejected_Veto_Version',
                                            '2021-06-11')]),
                    no('art1_par2', versao('Regra alterada.', '§ 2º', 'Text_Change_Version', '2023-07-20',
                                           origem='Lei nº 14.628 de 20/07/2023')),
                    no('art1_par3', [versao('Regra original em vigor.', '§ 3º'),
                                     versao('Regra da MP que perdeu a validade.', '§ 3º', 'Text_Change_Version',
                                            '2023-03-22', fora=True, origem='Medida Provisória nº 1.166')]),
                ]),
                no('art2', versao(nome='Art. 2º'), [
                    no('art2_cpt', versao('Os prazos mínimos são de:'), [no('art2_cpt_inc1', versao('8 dias;', 'I –'))]),
                ]) | {'workExample': [versao(nome='Art. 2º', fora=True),
                                      versao(tipo='Applicability_Suppression_Version', data='2024-05-17',
                                             origem='Medida Provisória nº 1.221 de 17/05/2024')]},
                no('art3', versao(nome='Art. 3º'), [
                    no('art3_cpt', versao('É dispensável a licitação:'), [
                        no('art3_cpt_inc1', [versao('hipótese da MP.', 'I –', 'Insertion_Version', '2023-03-22',
                                                    fora=True), versao('(Suprimido)', 'I –', 'Suppression_Version',
                                                                       '2023-08-02')], sufixo=',mpv-1166-2023-03-22'),
                        no('art3_cpt_inc1', versao('hipótese da lei.', 'I –', 'Insertion_Version', '2023-07-20',
                                                   origem='Lei nº 14.628 de 20/07/2023'), sufixo=',lei-14628-2023-07-20'),
                    ]),
                    no('art3_par1u', versao("Parágrafo com aspa da lei alteradora.'", 'Parágrafo único.')),
                ]),
                no('art3-1', versao(nome='Art. 3º-A', tipo='Insertion_Version', data='2023-12-22',
                                    origem='Lei nº 14.770 de 22/12/2023'), [
                    no('art3-1_cpt', versao('Regime simplificado:', tipo='Insertion_Version', data='2023-12-22',
                                            origem='Lei nº 14.770 de 22/12/2023'), [
                        no('art3-1_cpt_inc1', versao('plano de trabalho;', 'I –', 'Insertion_Version', '2023-12-22',
                                                     origem='Lei nº 14.770 de 22/12/2023')),
                    ]),
                ], sufixo=',lei-14770-2023-12-22'),
            ]),
        ]),
    ]},
}


class ObterDispositivoLei(unittest.TestCase):
    def setUp(self):
        tcu._CACHE_LEIS.clear()
        self.tools = tcu.Tools()

    def chamar(self, *args, corpo=LEI_FICTICIA, **kwargs):
        with mock.patch.object(tcu.urllib.request, 'urlopen', return_value=resposta(corpo)) as urlopen:
            texto = rodar(self.tools.obter_dispositivo_lei(*args, **kwargs))
        return texto, urlopen

    def test_artigo_inteiro_com_caput_na_linha_do_rotulo_e_todos_os_incisos(self):
        texto, urlopen = self.chamar('14133', '1')
        self.assertIn('## Lei 14.133/2021, art. 1º', texto)
        self.assertIn('Localização: TÍTULO I - DISPOSIÇÕES DE TESTE > CAPÍTULO I - DO PAGAMENTO', texto)
        self.assertIn('Art. 1º A Administração poderá, entre outras medidas:\nI – exigir garantia;\n'
                      'II – condicionar o pagamento à quitação;', texto)
        self.assertIn('registro de 20/07/2026', texto)
        self.assertIn(tcu.AVISO_LEI, texto)
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(urlopen.call_args[0][0].full_url).query)
        self.assertEqual(params['urn'], [URN])
        self.assertEqual(params['tipo_documento'], ['maior-detalhe'])

    def test_veto_derrubado_usa_versao_sem_notinforce(self):
        texto, _ = self.chamar('Lei 14.133/2021', '1', paragrafo='1')
        self.assertIn('§ 1º Texto restaurado pelo Congresso. (veto derrubado; em vigor desde 11/06/2021)', texto)
        self.assertNotIn('VETADO', texto)
        self.assertIn('Art. 1º A Administração poderá, entre outras medidas:\n[…]', texto)

    def test_redacao_alterada_anota_a_lei_de_origem(self):
        texto, _ = self.chamar('14133', '1', paragrafo='2')
        self.assertIn('(redação dada por Lei nº 14.628 de 20/07/2023 em 20/07/2023)', texto)

    def test_versao_mais_recente_fora_de_vigor_nao_vale(self):
        texto, _ = self.chamar('14133', '1', paragrafo='3')
        self.assertIn('§ 3º Regra original em vigor.', texto)
        self.assertNotIn('perdeu a validade', texto)

    def test_supressao_de_aplicabilidade_nao_suprime_o_artigo(self):
        texto, _ = self.chamar('14133', '2')
        self.assertIn('Art. 2º Os prazos mínimos são de: (aplicação afastada em hipótese específica por Medida '
                      'Provisória nº 1.221 de 17/05/2024', texto)
        self.assertIn('I – 8 dias;', texto)
        self.assertNotIn('suprimido', texto.lower().replace('supressão', ''))

    def test_mesma_posicao_fica_com_o_no_vigente_nao_suprimido(self):
        texto, _ = self.chamar('14133', '3', inciso='I')
        self.assertIn('I – hipótese da lei. (incluído por Lei nº 14.628', texto)
        self.assertNotIn('Suprimido', texto)
        self.assertIn('## Lei 14.133/2021, art. 3º, inciso I', texto)

    def test_rotulo_repetido_no_texto_nao_duplica(self):
        d = tcu.montar_dispositivo(no('art1_par4', versao('§ 4º Os valores depositados são impenhoráveis.', '§ 4º')))
        self.assertEqual(d.texto, 'Os valores depositados são impenhoráveis.')

    def test_paragrafo_unico_e_aspa_da_lei_alteradora(self):
        texto, _ = self.chamar('14133', '3', paragrafo='único')
        self.assertIn('Parágrafo único. Parágrafo com aspa da lei alteradora.\n', texto)
        self.assertIn('art. 3º, parágrafo único', texto)

    def test_artigo_com_letra_e_nota_de_inclusao_sem_repetir_nos_filhos(self):
        texto, _ = self.chamar('14133', '3-A')
        self.assertIn('Art. 3º-A Regime simplificado: (incluído por Lei nº 14.770 de 22/12/2023 em 22/12/2023)', texto)
        self.assertEqual(texto.count('incluído por Lei nº 14.770'), 1)
        self.assertEqual(self.chamar('14133', '3A')[0], texto)

    def test_inciso_em_arabico_ou_romano(self):
        self.assertEqual(self.chamar('14133', '1', inciso='2')[0], self.chamar('14133', '1', inciso='II')[0])

    def test_nao_encontrado_lei_fora_da_tabela_e_entrada_invalida(self):
        self.assertIn('não encontrado', self.chamar('14133', '99')[0])
        self.assertIn('não encontrado', self.chamar('14133', '1', paragrafo='9')[0])
        fora, urlopen = self.chamar('8666', '1')
        self.assertIn('só tem o texto estruturado de: Lei 14.133/2021', fora)
        urlopen.assert_not_called()
        self.assertIn('Dispositivo inválido', self.chamar('14133', 'cento e vinte')[0])

    def test_cache_baixa_a_lei_uma_vez(self):
        with mock.patch.object(tcu.urllib.request, 'urlopen', return_value=resposta(LEI_FICTICIA)) as urlopen:
            rodar(self.tools.obter_dispositivo_lei('14133', '1'))
            rodar(self.tools.obter_dispositivo_lei('14133', '2'))
        self.assertEqual(urlopen.call_count, 1)

    def test_cache_vencido_baixa_de_novo(self):
        self.tools.valves.cache_horas = 0
        with mock.patch.object(tcu.urllib.request, 'urlopen', side_effect=lambda *a, **k: resposta(LEI_FICTICIA)) as u:
            rodar(self.tools.obter_dispositivo_lei('14133', '1'))
            rodar(self.tools.obter_dispositivo_lei('14133', '1'))
        self.assertEqual(u.call_count, 2)

    def test_texto_longo_e_cortado_com_orientacao(self):
        self.tools.valves.max_chars_texto = 60
        texto, _ = self.chamar('14133', '1')
        self.assertIn('cortado em 60 caracteres', texto)
        self.assertIn('Peça um parágrafo ou inciso específico', texto)

    def test_falhas_viram_a_conferir_sem_transcricao(self):
        html_bloqueio, _ = self.chamar('14133', '1', corpo='<html>bloqueado</html>')
        self.assertIn('falhou', html_bloqueio)
        self.assertIn('a conferir', html_bloqueio)
        sem_arvore, _ = self.chamar('14133', '1', corpo={'name': 'Lei nº 14.133'})
        self.assertIn('texto estruturado', sem_arvore)
        with mock.patch.object(tcu.urllib.request, 'urlopen', side_effect=urllib.error.URLError('sem rede')):
            rede = rodar(self.tools.obter_dispositivo_lei('14133', '1'))
        self.assertIn('de memória', rede)

    def test_normalizacoes(self):
        self.assertEqual(tcu.normalizar_lei('Lei nº 14.133, de 1º de abril de 2021'), '14133')
        self.assertEqual(tcu.normalizar_lei(URN), '14133')
        self.assertIsNone(tcu.normalizar_lei('LC 123'))
        self.assertEqual(tcu.chave_dispositivo('Art. 121', '§ 3º', 'IV'), 'art121_par3_inc4')
        self.assertEqual(tcu.chave_dispositivo('75', inciso='XVII'), 'art75_cpt_inc17')
        self.assertEqual(tcu.chave_dispositivo('184-A'), 'art184-1')
        self.assertEqual(tcu.chave_dispositivo('1', '2', 'III', 'b'), 'art1_par2_inc3_ali2')
        self.assertEqual(tcu.chave_dispositivo('174', '3º-A'), 'art174_par3-1')
        self.assertEqual(tcu.chave_dispositivo('1', inciso='IV-A'), 'art1_cpt_inc4-1')



class BuscarNaLei(unittest.TestCase):
    def setUp(self):
        tcu._CACHE_LEIS.clear()
        self.tools = tcu.Tools()

    def buscar(self, termos, corpo=LEI_FICTICIA, lei='14133'):
        with mock.patch.object(tcu.urllib.request, 'urlopen', return_value=resposta(corpo)) as urlopen:
            texto = rodar(self.tools.buscar_na_lei(lei, termos))
        return texto, urlopen

    def itens(self, texto):
        return [l for l in texto.splitlines() if l[:1].isdigit()]

    def test_acha_inciso_sem_acento_e_com_citacao_pronta(self):
        texto, _ = self.buscar('condicionar pagamento quitacao')
        self.assertEqual(self.itens(texto)[0],
                         '1. **art. 1º, inciso II**: condicionar o pagamento à quitação;')
        self.assertIn('Abra o artigo com obter_dispositivo_lei antes de citar', texto)
        self.assertIn(tcu.AVISO_LEI, texto)

    def test_frase_entre_aspas_e_obrigatoria(self):
        texto, _ = self.buscar('"entre outras medidas"')
        self.assertEqual(len(self.itens(texto)), 1)
        self.assertIn('**art. 1º**:', texto)
        self.assertIn('Nenhum dispositivo', self.buscar('"medidas entre outras"')[0])

    def test_radical_casa_variacoes_e_palavra_curta_nao_vira_prefixo_amplo(self):
        self.assertIn('art. 1º, § 2º', self.buscar('regras alteradas')[0])
        self.assertIn('art. 2º, inciso I', self.buscar('dia')[0])
        corpo = {'dateModified': '2026-07-20', 'hasPart': [
            no('art1', versao(nome='Art. 1º'), [no('art1_cpt', versao('O contrato será assinado.'))])]}
        self.assertIn('Nenhum dispositivo', self.buscar('conta', corpo=corpo)[0])

    def test_frase_entre_aspas_com_palavra_que_nao_aparece(self):
        texto, _ = self.buscar('"entre outras medidas" pagamento')
        self.assertIn('**art. 1º**', texto)

    def test_termo_raro_pesa_mais_que_termo_comum(self):
        # Como na lei real: "prazo" e "edital" aparecem em muitos dispositivos, "impugnar" em poucos.
        comuns = [no(f'art{i}', versao(nome=f'Art. {i}'), [no(f'art{i}_cpt', versao(f'O edital fixará o prazo {i}.'))])
                  for i in range(1, 11)]
        raro = no('art11', versao(nome='Art. 11'), [no('art11_cpt', versao('Qualquer pessoa pode impugnar o edital.'))])
        outros = [no(f'art{i}', versao(nome=f'Art. {i}'), [no(f'art{i}_cpt', versao(f'Regra geral número {i}.'))])
                  for i in range(12, 40)]
        texto, _ = self.buscar('prazo impugnação edital', corpo={'dateModified': '2026-07-20',
                                                                'hasPart': comuns + [raro] + outros})
        self.assertIn('**art. 11**', self.itens(texto)[0])

    def test_dispositivo_suprimido_fica_fora(self):
        texto, _ = self.buscar('hipótese')
        self.assertIn('hipótese da lei', texto)
        self.assertNotIn('Suprimido', texto)
        self.assertNotIn('hipótese da MP', texto)
        tcu._CACHE_LEIS.clear()
        corpo = {'dateModified': '2026-07-20', 'hasPart': [no('art1', versao(nome='Art. 1º'), [
            no('art1_cpt', versao('Regras de transição:'), [
                no('art1_cpt_inc1', versao('transição para órgãos;', 'I –')),
                no('art1_cpt_inc2', [versao('transição da MP;', 'II –', 'Insertion_Version', '2023-03-31', fora=True),
                                     versao('(Suprimido)', 'II –', 'Suppression_Version', '2023-08-02')]),
            ])])]}
        texto, _ = self.buscar('suprimido transição', corpo=corpo)
        self.assertNotIn('inciso II', texto)

    def test_sem_resultado_lei_fora_e_falha_tem_mensagens_distintas(self):
        vazio, _ = self.buscar('palavrainexistente')
        self.assertIn('não conclua que a lei não trata do assunto', vazio)
        fora, urlopen = self.buscar('garantia', lei='LC 123')
        self.assertIn('a conferir', fora)
        urlopen.assert_not_called()
        tcu._CACHE_LEIS.clear()
        falha, _ = self.buscar('garantia', corpo='<html>bloqueado</html>')
        self.assertIn('falhou', falha)

    def test_busca_reaproveita_a_lei_em_cache(self):
        with mock.patch.object(tcu.urllib.request, 'urlopen', return_value=resposta(LEI_FICTICIA)) as urlopen:
            rodar(self.tools.obter_dispositivo_lei('14133', '1'))
            rodar(self.tools.buscar_na_lei('14133', 'garantia'))
        self.assertEqual(urlopen.call_count, 1)

    def test_limite_de_resultados(self):
        self.tools.valves.max_resultados = 1
        texto, _ = self.buscar('de para o')  # só palavras sem conteúdo
        self.assertIn('Nenhum dispositivo', texto)
        texto, _ = self.buscar('garantia pagamento')
        self.assertEqual(len(self.itens(texto)), 1)
        self.assertIn('Mostrando 1 de 2', texto)


if __name__ == '__main__':
    unittest.main()
