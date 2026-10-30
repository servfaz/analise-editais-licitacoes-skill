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
        self.assertNotEqual(texto, tcu.NENHUM)

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


if __name__ == '__main__':
    unittest.main()
