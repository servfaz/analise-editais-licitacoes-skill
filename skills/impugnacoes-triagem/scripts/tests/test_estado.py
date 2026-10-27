import io
import json
import os
import subprocess
import sys
import tempfile
import unicodedata
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import estado
from triagem import comum, fases, persistencia
from triagem.formatos import ACCEPT_EXAMPLE

TZ = timezone(timedelta(hours=-3))
ORGAO = 'Secretaria Municipal de Saúde de Exemplópolis'
# Dados fictícios. IMP-100 e IMP-20 conferem a ordem numérica (a ordem de texto poria IMP-100 antes).
ITEMS = [
    {'id': 'ESC-02', 'classe': 'esclarecimento', 'titulo': 'Jornada do posto diurno'},
    {'id': 'IMP-100', 'classe': 'impugnacao', 'titulo': 'Capital social mínimo acima do limite'},
    {'id': 'ESC-01', 'classe': 'esclarecimento', 'titulo': 'Data-base da repactuação'},
    {'id': 'IMP-20', 'classe': 'impugnacao', 'titulo': 'Atestado com quantitativo excessivo'},
]
DEADLINE = {'abertura': '2026-10-30', 'data_limite': '2026-10-27', 'alertas': []}
ACCEPT = 'aceito a edição do estado: corrigi o título à mão'
REST = {'incluir': 'incluo', 'descartar': 'descarto', 'avaliar_depois': 'deixo para depois'}


def run(*args, stdin=''):
    out, err = io.StringIO(), io.StringIO()
    # bytes simulam a entrada padrão real (com .buffer), para testar o que não é UTF-8.
    stream = io.TextIOWrapper(io.BytesIO(stdin), encoding='utf-8') if isinstance(stdin, bytes) else io.StringIO(stdin)
    with redirect_stdout(out), redirect_stderr(err), mock.patch('sys.stdin', stream):
        code = estado.main([str(a) for a in args])
    return code, out.getvalue(), err.getvalue()


class EstadoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.root = self.base / 'triagens'
        self.manifest = self.base / 'MANIFEST.json'
        self.manifest.write_text(json.dumps({'estudo_sha256': 'a' * 64}), encoding='utf-8')
        self.assets = self.base / 'assets'
        self.assets.mkdir()
        self.clock = datetime(2026, 10, 19, 9, 30, 15, tzinfo=TZ)
        # O estudo e os modelos da peça são caminhos fixos (sem opção na linha de comando): os testes os trocam aqui.
        for patcher in (mock.patch.object(comum, 'now', lambda: self.clock),
                        mock.patch.object(fases, 'MANIFEST', self.manifest),
                        mock.patch.object(fases, 'ASSETS', self.assets)):
            patcher.start()
            self.addCleanup(patcher.stop)

    def tearDown(self):
        self.tmp.cleanup()

    def start(self, *extra):
        return run('iniciar', '--raiz', self.root, '--orgao', ORGAO, '--modalidade', 'PE', '--numero', '90001',
                   '--ano', '2026', *extra)

    def init(self):
        code, out, err = self.start()
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.folder = Path(result['pasta'])
        return result

    def call(self, command, *args, stdin=''):
        return run(command, '--pasta', self.folder, *args, stdin=stdin)

    def ok(self, command, *args, stdin=''):
        code, out, err = self.call(command, *args, stdin=stdin)
        self.assertEqual(code, 0, err)
        return json.loads(out)

    def refused(self, command, *args, contains, stdin=''):
        code, out, err = self.call(command, *args, stdin=stdin)
        self.assertEqual(code, 1, out)
        self.assertIn(contains, err)

    def status(self):
        return self.ok('status')

    def gate(self, faltas=''):
        missing = comum.split_list(faltas)
        present = ','.join(code for code in comum.DOC_CODES if code not in missing)
        return self.ok('documentos', '--presentes', present, '--faltas', faltas)

    def items_file(self, items):
        path = self.base / 'itens.json'
        path.write_text(json.dumps(items, ensure_ascii=False), encoding='utf-8')
        return path

    def add_items(self, items=ITEMS):
        return self.ok('itens', '--arquivo', self.items_file(items))

    def to_selection(self, items=ITEMS):
        self.init()
        self.gate()
        return self.add_items(items)

    def include(self, ids):
        return self.ok('decidir', '--evidencia', f'incluo {ids}')

    def decide_rest(self, decision):
        return self.ok('decidir', '--evidencia', f'{REST[decision]} os demais')

    def draft(self, item_id):
        return self.folder / 'minutas' / f'{item_id}.md'

    def write_draft(self, item_id, text='Fatos, fundamentação e pedido.\n'):
        self.draft(item_id).write_text(text, encoding='utf-8')

    def open_and_register(self, item_id, text='Fatos, fundamentação e pedido.\n'):
        opened = self.ok('minuta', '--acao', 'abrir')
        self.assertEqual(opened['minuta_em_revisao']['id'], item_id)
        self.write_draft(item_id, text)
        return self.ok('minuta', '--id', item_id, '--acao', 'registrar')

    def approve(self, item_id):
        self.open_and_register(item_id)
        return self.ok('minuta', '--evidencia', f'aprovo {item_id}')

    def validate(self):
        code, out, _ = self.call('validar')
        return code, json.loads(out)['violacoes']

    def edit_state(self, change):
        path = self.folder / 'estado.json'
        state = json.loads(path.read_text(encoding='utf-8'))
        change(state)
        path.write_text(json.dumps(state, ensure_ascii=False), encoding='utf-8')

    def test_slug_strips_accents_and_accepts_nfd(self):
        expected = 'secretaria-municipal-de-saude-de-exemplopolis-pe-90-001-2026'
        code, out, _ = run('slug', '--orgao', ORGAO, '--modalidade', 'PE', '--numero', '90.001', '--ano', '2026')
        self.assertEqual((code, out.strip()), (0, expected))
        decomposed = unicodedata.normalize('NFD', ORGAO)
        self.assertNotEqual(decomposed, ORGAO)
        code, out, _ = run('slug', '--orgao', decomposed, '--modalidade', 'PE', '--numero', '90.001', '--ano', '2026')
        self.assertEqual(out.strip(), expected)
        code, _, err = run('slug', '--orgao', ORGAO, '--modalidade', 'PE', '--numero', '1', '--ano', '26')
        self.assertEqual(code, 1)
        self.assertIn('ano inválido', err)

    def test_iniciar_creates_folder_and_refuses_existing(self):
        result = self.init()
        self.assertEqual(self.folder.name, 'secretaria-municipal-de-saude-de-exemplopolis-pe-90001-2026')
        for name in ('estado.json', 'registro.md', 'minutas/historico', 'texto'):
            self.assertTrue((self.folder / name).exists(), name)
        self.assertEqual(result['fase'], 'documentos')
        self.assertEqual(result['estudo_sha256'], 'a' * 64)
        self.assertEqual(result['alertas'], [])
        self.assertIn('Não faça levantamento', result['proxima_acao'])
        code, _, err = self.start()
        self.assertEqual(code, 1)
        self.assertIn('já existe', err)
        self.assertIn('status --pasta', err)

    def test_iniciar_without_manifest_records_null_with_alert(self):
        self.manifest.unlink()
        code, out, err = self.start('--esfera', 'municipal')
        self.assertEqual(code, 0, err)
        self.assertIn('aviso: MANIFEST.json', err)
        result = json.loads(out)
        self.assertIsNone(result['estudo_sha256'])
        self.assertEqual(result['certame']['esfera'], 'municipal')
        self.assertTrue(any('hash do estudo' in a for a in result['alertas']))

    def test_status_alerts_when_study_changed(self):
        self.init()
        self.manifest.write_text(json.dumps({'estudo_sha256': 'b' * 64}), encoding='utf-8')
        self.assertTrue(any('o estudo mudou' in a for a in self.status()['alertas']))

    def test_happy_path_until_concluido(self):
        self.assertEqual(self.init()['fase'], 'documentos')
        self.assertEqual(self.gate()['fase'], 'levantamento')
        self.ok('prazo', '--dados', '-', stdin=json.dumps(DEADLINE))
        result = self.add_items(ITEMS[:2])
        self.assertEqual(result['fase'], 'selecao')
        self.assertEqual(result['itens']['pendentes'], ['IMP-100', 'ESC-02'])
        result = self.ok('decidir', '--evidencia', 'Incluo a IMP-100 e o ESC-02')
        self.assertEqual(result['fase'], 'minutas')
        self.assertEqual(result['fila_minutas'], ['IMP-100', 'ESC-02'])
        opened = self.ok('minuta', '--acao', 'abrir')
        self.assertEqual(opened['minuta_em_revisao'],
                         {'id': 'IMP-100', 'versao': 1, 'arquivo': str(self.draft('IMP-100')), 'registrada': False,
                          'sha256': None})
        self.write_draft('IMP-100')
        registered = self.ok('minuta', '--id', 'IMP-100', '--acao', 'registrar')
        self.assertTrue(registered['minuta_em_revisao']['registrada'])
        self.assertEqual(registered['minuta_em_revisao']['sha256'], comum.sha256_file(self.draft('IMP-100')))
        self.assertIn('"aprovo IMP-100" ou "ajuste IMP-100: ', registered['proxima_acao'])
        result = self.ok('minuta', '--evidencia', 'Aprovo a IMP-100.')
        self.assertEqual((result['fase'], result['fila_minutas']), ('minutas', ['ESC-02']))
        self.assertEqual(self.approve('ESC-02')['fase'], 'peca_final')
        (self.assets / 'modelo-impugnacao.docx').write_bytes(b'modelo')
        (self.assets / 'modelo-esclarecimento.docx').write_bytes(b'modelo')
        check = self.ok('peca', '--acao', 'verificar')
        self.assertTrue(check['pronto'], check['pendencias'])
        self.assertEqual([a['id'] for a in check['aprovadas_por_tipo']['impugnacao']], ['IMP-100'])
        self.assertTrue(check['modelos']['esclarecimento'].endswith('modelo-esclarecimento.docx'))
        result = self.ok('peca', '--acao', 'confirmar', '--evidencia', 'Confirmo a peça de impugnação em formato único')
        self.assertEqual(result['fase'], 'peca_final')
        self.assertEqual(result['peca']['impugnacao']['aprovadas'][0]['versao'], 1)
        result = self.ok('peca', '--acao', 'confirmar',
                         '--evidencia', 'confirmo a peça de esclarecimento em formato por ponto')
        self.assertEqual(result['fase'], 'concluido')
        self.assertEqual((result['peca']['impugnacao']['formato'], result['peca']['esclarecimento']['formato']),
                         ('unico', 'por_ponto'))
        self.assertEqual([a['id'] for a in result['aprovadas']], ['IMP-100', 'ESC-02'])
        self.assertEqual(self.validate(), (0, []))

    def test_gate_with_missing_documents_requires_proceed(self):
        self.init()
        result = self.gate('ETP,PESQUISA')
        self.assertEqual(result['fase'], 'documentos')
        self.assertIn('ETP, PESQUISA', result['proxima_acao'])
        self.refused('itens', '--arquivo', self.items_file(ITEMS), contains='portão documental')
        self.assertIn('"prossigo sem ETP e PESQUISA"', result['proxima_acao'])
        self.refused('prosseguir', '--evidencia', 'Pode seguir.', contains='não está no formato do prosseguir')
        result = self.ok('prosseguir', '--evidencia', 'Prossigo sem o ETP e a  pesquisa.')
        self.assertEqual(result['fase'], 'levantamento')
        self.assertEqual(result['documentos']['prosseguir']['evidencia'], 'Prossigo sem o ETP e a pesquisa.')
        self.assertEqual(self.gate('ETP')['fase'], 'levantamento')  # falta já coberta pela decisão
        self.assertEqual(self.gate('ETP,PLANILHA')['fase'], 'documentos')  # falta nova pede nova decisão
        result = self.gate()
        self.assertEqual(result['fase'], 'levantamento')
        self.assertIsNone(result['documentos']['prosseguir'])
        self.refused('prosseguir', '--evidencia', 'prossigo sem ETP', contains='não há faltas')

    def test_documentos_rejects_bad_lists(self):
        self.init()
        others = 'ETP,PLANILHA,PESQUISA,MINUTA'
        self.refused('documentos', '--presentes', 'EDITAL,TR', '--faltas', f'TR,{others}', contains='ao mesmo tempo')
        self.refused('documentos', '--presentes', 'EDITAL', '--faltas', 'TR', contains='faltou classificar ETP')
        self.refused('documentos', '--presentes', 'EDITAL,TR,XYZ', '--faltas', others, contains='desconhecido: XYZ')
        self.assertIsNone(self.status()['documentos'])

    def test_reri_is_out_of_scope(self):
        self.init()
        others = 'ETP,PLANILHA,PESQUISA,MINUTA'
        for present, missing in (('EDITAL,TR,RERI', others), ('EDITAL,TR', f'reri,{others}')):
            with self.subTest(presentes=present, faltas=missing):
                self.refused('documentos', '--presentes', present, '--faltas', missing,
                             contains='fora do escopo desta skill')
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.call('documentos', '--presentes', 'EDITAL,TR', '--faltas', others, '--reri', 'ausente')
        self.assertIsNone(self.status()['documentos'])
        self.gate()
        state = json.loads((self.folder / 'estado.json').read_text(encoding='utf-8'))
        self.assertNotIn('reri', state['documentos'])
        self.assertNotIn('RERI', (self.folder / 'registro.md').read_text(encoding='utf-8'))
        self.assertNotIn('RERI', json.dumps(state['eventos'], ensure_ascii=False))

    def test_items_before_gate_refused(self):
        self.init()
        self.refused('itens', '--arquivo', self.items_file(ITEMS), contains='portão documental')
        self.assertEqual(self.status()['itens']['total'], 0)

    def test_items_with_bad_id_or_class_refused(self):
        self.init()
        self.gate()
        cases = [
            ([{'id': 'IMP-01', 'classe': 'esclarecimento', 'titulo': 'X'}], 'incoerente'),
            ([{'id': 'ESC-03', 'classe': 'impugnacao', 'titulo': 'X'}], 'incoerente'),
            ([{'id': 'ESC-1', 'classe': 'esclarecimento', 'titulo': 'X'}], 'fora do formato'),
            ([{'id': 'imp-01', 'classe': 'impugnacao', 'titulo': 'X'}], 'fora do formato'),
            ([{'id': 'IMP-01', 'classe': 'impugnacao', 'titulo': '  '}], 'título vazio'),
            ([{'id': 'IMP-０２', 'classe': 'impugnacao', 'titulo': 'X'}], 'fora do formato'),  # dígitos largos
            ([ITEMS[0], ITEMS[0]], 'já existe'),
            ([ITEMS[3], {'id': 'IMP-020', 'classe': 'impugnacao', 'titulo': 'X'}], 'IMP-020 repete o número de IMP-20'),
            ({'itens': ITEMS}, 'precisa ser uma lista'),
        ]
        for items, message in cases:
            with self.subTest(message=message, items=items):
                self.refused('itens', '--arquivo', self.items_file(items), contains=message)
        result = self.status()
        self.assertEqual((result['fase'], result['itens']['total']), ('levantamento', 0))

    def test_items_can_be_appended_and_repeated_id_refused(self):
        self.to_selection(ITEMS[:2])
        self.decide_rest('avaliar_depois')
        self.assertEqual(self.status()['fase'], 'concluido')
        result = self.add_items(ITEMS[2:] + [{'id': 'IMP-03', 'classe': 'Impugnação', 'titulo': 'Cota reservada'}])
        self.assertEqual(result['fase'], 'selecao')
        self.assertEqual(result['itens']['pendentes'], ['IMP-03', 'IMP-20', 'ESC-01'])
        self.refused('itens', '--arquivo', self.items_file([ITEMS[0]]), contains='ESC-02 já existe')
        self.refused('itens', '--arquivo', self.items_file([]), contains='nenhum item novo')
        self.assertEqual(self.status()['itens']['total'], 5)

    def test_empty_survey_concludes_without_items(self):
        self.init()
        self.gate()
        result = self.add_items([])
        self.assertEqual(result['fase'], 'concluido')
        self.assertIn('Nenhuma minuta aprovada', result['proxima_acao'])

    def test_queue_orders_imp_before_esc_by_number(self):
        self.to_selection()
        result = self.decide_rest('incluir')
        self.assertEqual(result['fila_minutas'], ['IMP-20', 'IMP-100', 'ESC-01', 'ESC-02'])
        self.refused('minuta', '--acao', 'abrir', '--id', 'IMP-100', contains='a próxima da fila é IMP-20')
        self.assertEqual(self.ok('minuta', '--acao', 'abrir')['minuta_em_revisao']['id'], 'IMP-20')

    def test_second_open_refused(self):
        self.to_selection()
        self.decide_rest('incluir')
        self.ok('minuta', '--acao', 'abrir')
        self.refused('minuta', '--acao', 'abrir', contains='IMP-20 v1 já está em revisão')
        self.assertEqual(self.status()['minuta_em_revisao']['id'], 'IMP-20')

    def test_open_refused_while_items_pending(self):
        self.to_selection()
        self.include('IMP-20')
        self.refused('minuta', '--acao', 'abrir', contains='fase "selecao"')

    def test_approve_without_register_refused(self):
        self.to_selection()
        self.decide_rest('incluir')
        self.ok('minuta', '--acao', 'abrir')
        self.refused('minuta', '--id', 'IMP-20', '--acao', 'registrar', contains='não existe')
        self.write_draft('IMP-20')
        self.refused('minuta', '--evidencia', 'aprovo IMP-20', contains='ainda não foi registrada')
        self.refused('minuta', '--id', 'IMP-100', '--acao', 'registrar', contains='a minuta em revisão é IMP-20')
        self.assertEqual(self.status()['aprovadas'], [])

    def test_file_changed_after_register_blocks_decision(self):
        self.to_selection()
        self.decide_rest('incluir')
        self.open_and_register('IMP-20')
        self.write_draft('IMP-20', 'Texto mudado depois do registro.\n')
        self.refused('minuta', '--evidencia', 'aprovo IMP-20', contains='mudou')
        result = self.status()
        self.assertTrue(any('alterada depois do registro' in a for a in result['alertas']))
        self.assertIn('registre de novo', result['proxima_acao'])
        self.ok('minuta', '--id', 'IMP-20', '--acao', 'registrar')
        self.ok('minuta', '--evidencia', 'aprovo IMP-20')

    def test_free_phrases_refused_with_format_and_example(self):
        self.to_selection()
        for phrase in ('Ok!', 'sim, pode seguir', 'incluir todos', '  ', 'inclui a IMP-20'):
            with self.subTest(phrase=phrase):
                self.refused('decidir', '--evidencia', phrase, contains='não está no formato do decidir')
        self.refused('decidir', '--evidencia', 'ok', contains='Exemplo com os dados desta triagem: "incluo IMP-20; '
                                                             'descarto IMP-100; deixo para depois os demais"')
        self.decide_rest('incluir')
        self.open_and_register('IMP-20')
        cases = [
            ('segue', 'não está no formato da decisão sobre a minuta'),
            ('aprovo', 'não está no formato da decisão sobre a minuta'),
            ('aprovo todas', 'não está no formato da decisão sobre a minuta'),
            ('aprovo IMP-20 e IMP-100', 'um ID só'),
            ('aprovo a IMP-100', 'a frase cita IMP-100, mas a minuta em revisão é IMP-20'),
            ('não aprovo IMP-20', 'não está no formato'),
            ('aprovo IMP-20?', 'não está no formato'),
            ('ajuste IMP-20: muda isso', 'menos de 10 caracteres'),
            ('ajuste: troque o pedido subsidiário', 'não está no formato'),
        ]
        for phrase, message in cases:
            with self.subTest(phrase=phrase):
                self.refused('minuta', '--evidencia', phrase, contains=message)
        self.refused('minuta', '--evidencia', 'aprovo', contains='"aprovo IMP-20" ou "ajuste IMP-20: ')
        self.refused('minuta', '--acao', 'registrar', '--id', 'IMP-20', '--evidencia', 'aprovo IMP-20',
                     contains='--evidencia vai sem --acao')
        self.refused('minuta', contains='informe --acao abrir|registrar ou --evidencia')
        self.refused('minuta', '--id', 'IMP-100', '--evidencia', 'aprovo IMP-100', contains='a minuta em revisão é IMP-20')
        result = self.status()
        self.assertEqual(result['minuta_em_revisao']['versao'], 1)
        self.assertEqual(result['aprovadas'], [])

    def test_decide_applies_every_clause_in_one_call(self):
        self.to_selection()
        result = self.ok('decidir', '--evidencia', 'incluo IMP-20 e ESC-1; deixo para depois ESC-02')
        self.assertEqual((result['itens']['incluidos'], result['itens']['avaliar_depois'], result['itens']['pendentes']),
                         (['IMP-20', 'ESC-01'], ['ESC-02'], ['IMP-100']))
        self.assertIn('Continuam pendentes: IMP-100.', result['mensagem'])
        for phrase, message in (('incluo IMP-100; descarto IMP-100', 'IMP-100 aparece mais de uma vez'),
                                ('incluo IMP-07', 'IMP-07 não está registrado'),
                                ('incluo os demais; descarto os demais', 'mais de uma cláusula'),
                                ('incluo IMP-100; descarto os demais', '"os demais" não tem a que se referir')):
            with self.subTest(phrase=phrase):
                self.refused('decidir', '--evidencia', phrase, contains=message)
        result = self.ok('decidir', '--evidencia', 'descarto os demais; incluo ESC-02')
        self.assertEqual((result['itens']['descartados'], result['itens']['incluidos'], result['fase']),
                         (['IMP-100'], ['IMP-20', 'ESC-01', 'ESC-02'], 'minutas'))
        state = self.read_state()
        self.assertEqual([e['detalhe'] for e in state['eventos'] if e['acao'] == 'decidir'][-2:],
                         ['IMP-100 → descartar: "descarto os demais; incluo ESC-02"',
                          'ESC-02 → incluir: "descarto os demais; incluo ESC-02"'])
        self.ok('minuta', '--acao', 'abrir')
        self.refused('decidir', '--evidencia', 'descarto IMP-20', contains='IMP-20 já tem minuta aberta ou decidida')
        self.refused('decidir', '--evidencia', 'descarto IMP-20', contains='"reabro IMP-20: ')
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.call('decidir', '--ids', 'IMP-20', '--decisao', 'incluir', '--evidencia', 'incluo IMP-20')
        self.assertEqual(self.validate(), (0, []))

    def test_adjust_moves_to_history_and_increments_version(self):
        self.to_selection()
        self.include('IMP-20')
        self.decide_rest('descartar')
        self.open_and_register('IMP-20', 'versão 1\n')
        result = self.ok('minuta', '--evidencia', 'ajuste IMP-20: citar a página do TR no pedido')
        self.assertEqual(result['minuta_em_revisao'],
                         {'id': 'IMP-20', 'versao': 2, 'arquivo': str(self.draft('IMP-20')), 'registrada': False,
                          'sha256': None})
        archived = self.folder / 'minutas' / 'historico' / 'IMP-20.v1.md'
        self.assertEqual(archived.read_text(encoding='utf-8'), 'versão 1\n')
        self.assertFalse(self.draft('IMP-20').exists())
        self.refused('minuta', '--acao', 'abrir', contains='IMP-20 v2 já está em revisão')
        self.write_draft('IMP-20', 'versão 2\n')
        self.ok('minuta', '--id', 'IMP-20', '--acao', 'registrar')
        result = self.ok('minuta', '--evidencia', 'aprovo IMP-20')
        self.assertEqual([(a['id'], a['versao']) for a in result['aprovadas']], [('IMP-20', 2)])
        self.assertEqual(self.validate(), (0, []))

    def test_discard_draft_moves_file_and_finishes_item(self):
        self.to_selection()
        self.include('IMP-20')
        self.decide_rest('avaliar_depois')
        self.open_and_register('IMP-20')
        result = self.ok('minuta', '--evidencia', 'Descarto a IMP-20.')
        self.assertEqual(result['fase'], 'concluido')
        self.assertIn('Para avaliar depois: IMP-100, ESC-01, ESC-02', result['proxima_acao'])
        self.assertFalse(self.draft('IMP-20').exists())
        self.assertTrue((self.folder / 'minutas' / 'historico' / 'IMP-20.v1.md').exists())
        self.assertEqual(self.validate(), (0, []))

    def test_file_changed_after_approval_fails_validation_and_alerts(self):
        self.to_selection()
        self.include('IMP-20')
        self.decide_rest('descartar')
        self.approve('IMP-20')
        self.assertEqual(self.validate(), (0, []))
        self.write_draft('IMP-20', 'Editado depois da aprovação.\n')
        code, found = self.validate()
        self.assertEqual(code, 1)
        self.assertTrue(any('sha256 não confere' in v for v in found), found)
        self.assertTrue(any('alterada ou removida depois de aprovada' in a for a in self.status()['alertas']))
        check = self.ok('peca', '--acao', 'verificar')
        self.assertFalse(check['pronto'])
        self.assertIn('IMP-20: minuta alterada ou removida depois de aprovada', check['pendencias'])

    def test_reopen_returns_to_selection(self):
        self.to_selection()
        self.include('IMP-20')
        self.decide_rest('descartar')
        self.approve('IMP-20')
        self.refused('decidir', '--evidencia', 'descarto IMP-20', contains='rode "reabrir"')
        result = self.ok('reabrir', '--evidencia', 'Reabro a IMP-20: mudei de ideia sobre o capital social')
        self.assertEqual(result['fase'], 'selecao')
        self.assertEqual(result['itens']['pendentes'], ['IMP-20'])
        self.assertEqual(result['aprovadas'], [])
        self.assertFalse(self.draft('IMP-20').exists())
        self.assertTrue((self.folder / 'minutas' / 'historico' / 'IMP-20.v1.md').exists())
        self.refused('reabrir', '--evidencia', 'reabro IMP-20: de novo, por engano', contains='já está pendente')
        for phrase, message in (('reabro IMP-20', 'não está no formato do reabrir'),
                                ('reabro IMP-20: engano', 'menos de 10 caracteres'),
                                ('reabro IMP-07: mudei de ideia sobre isso', 'IMP-07 não está registrado')):
            with self.subTest(phrase=phrase):
                self.refused('reabrir', '--evidencia', phrase, contains=message)
        self.include('IMP-20')
        self.assertEqual(self.ok('minuta', '--acao', 'abrir')['minuta_em_revisao']['versao'], 2)
        self.assertEqual(self.validate(), (0, []))

    def test_reopen_after_confirmation_clears_piece(self):
        self.to_selection(ITEMS[1:2])
        self.include('IMP-100')
        self.approve('IMP-100')
        (self.assets / 'modelo-impugnacao.pdf').write_bytes(b'modelo')
        self.ok('peca', '--acao', 'confirmar', '--evidencia', 'confirmo a peça de impugnação em formato único')
        self.assertEqual(self.status()['fase'], 'concluido')
        result = self.ok('reabrir', '--evidencia', 'reabro IMP-100: quero rever o fundamento do pedido')
        self.assertIsNone(result['peca']['impugnacao'])
        self.assertEqual(result['fase'], 'selecao')
        state = json.loads((self.folder / 'estado.json').read_text(encoding='utf-8'))
        self.assertIn('peca_invalidada', [e['acao'] for e in state['eventos']])
        self.assertEqual(self.validate(), (0, []))

    def test_piece_confirm_without_model_refused(self):
        self.to_selection(ITEMS[1:2])
        self.include('IMP-100')
        self.approve('IMP-100')
        check = self.ok('peca', '--acao', 'verificar')
        self.assertTrue(check['pronto'])
        self.assertEqual(check['modelos'], {'impugnacao': None, 'esclarecimento': None})
        for phrase in ('confirmo a peça de impugnação em formato único', 'Confirmo a peça'):
            with self.subTest(phrase=phrase):
                self.refused('peca', '--acao', 'confirmar', '--evidencia', phrase,
                             contains='só sai quando o modelo existir')
        result = self.status()
        self.assertEqual(result['fase'], 'peca_final')
        self.assertIsNone(result['peca']['impugnacao'])

    def test_piece_confirm_requires_everything_decided(self):
        self.to_selection()
        self.include('IMP-20,ESC-01')
        self.decide_rest('avaliar_depois')
        self.approve('IMP-20')
        self.ok('reabrir', '--evidencia', 'reabro IMP-100: o analista quer decidir a IMP-100 agora')
        (self.assets / 'modelo-impugnacao.docx').write_bytes(b'modelo')
        check = self.ok('peca', '--acao', 'verificar')
        self.assertFalse(check['pronto'])
        self.assertIn('IMP-100: decisão pendente', check['pendencias'])
        self.assertIn('ESC-01: minuta ainda não aberta', check['pendencias'])
        self.refused('peca', '--acao', 'confirmar', '--evidencia', 'confirmo a peça de impugnação em formato único',
                     contains='pendências')

    def test_phase_is_derived_at_each_step(self):
        self.assertEqual(self.init()['fase'], 'documentos')
        self.assertEqual(self.gate('MINUTA')['fase'], 'documentos')
        self.assertEqual(self.ok('prosseguir', '--evidencia', 'prossigo sem a MINUTA')['fase'], 'levantamento')
        self.assertEqual(self.add_items(ITEMS[:2])['fase'], 'selecao')
        self.assertEqual(self.include('IMP-100')['fase'], 'selecao')  # ESC-02 ainda pendente
        self.assertEqual(self.include('ESC-02')['fase'], 'minutas')
        self.assertEqual(self.approve('IMP-100')['fase'], 'minutas')
        self.assertEqual(self.gate('MINUTA,TR')['fase'], 'documentos')  # falta nova reabre o portão
        self.refused('minuta', '--acao', 'abrir', contains='portão documental')
        self.ok('prosseguir', '--evidencia', 'prossigo sem TR e MINUTA')
        self.open_and_register('ESC-02')
        self.ok('minuta', '--evidencia', 'descarto ESC-02')
        self.assertEqual(self.status()['fase'], 'peca_final')

    def test_nothing_included_goes_to_concluido(self):
        self.to_selection()
        result = self.decide_rest('descartar')
        self.assertEqual(result['fase'], 'concluido')
        self.assertEqual(result['itens']['descartados'], ['IMP-20', 'IMP-100', 'ESC-01', 'ESC-02'])
        self.refused('decidir', '--evidencia', 'incluo os demais', contains='"os demais" não tem a que se referir')
        self.refused('decidir', '--evidencia', 'incluo IMP-99', contains='IMP-99 não está registrado')

    def test_registro_md_regenerated(self):
        self.init()
        log = (self.folder / 'registro.md').read_text(encoding='utf-8')
        self.assertIn(f'# Registro da triagem {self.folder.name}', log)
        self.assertIn('- Fase: documentos', log)
        self.assertIn('Nenhum item registrado.', log)
        self.gate()
        self.add_items(ITEMS[:3] + [dict(ITEMS[3], titulo='Atestado | quantitativo excessivo')])
        self.ok('decidir', '--evidencia', 'Incluo a IMP-20')
        log = (self.folder / 'registro.md').read_text(encoding='utf-8')
        self.assertIn('- Fase: selecao', log)
        self.assertIn('| ID | Classe | Título | Decisão | Minuta | Evidência |', log)
        self.assertIn('| IMP-20 | impugnação | Atestado \\| quantitativo excessivo | incluir | — | '
                      'decisão: "Incluo a IMP-20" |', log)
        self.assertIn('| ESC-02 | esclarecimento | Jornada do posto diurno | pendente | — | — |', log)
        self.assertIn('- 2026-10-19T09:30:15-03:00 decidir: IMP-20 → incluir', log)
        self.assertEqual([p.name for p in self.folder.iterdir() if p.name.endswith('.tmp')], [])

    def test_deadline_from_stdin_and_expired_alert(self):
        self.init()
        data = dict(DEADLINE, data_limite='2026-10-16', alertas=['feriado local: conferir'])
        result = self.ok('prazo', '--dados', '-', stdin=json.dumps(data))
        self.assertEqual(result['prazo']['data_limite'], '2026-10-16')
        self.assertIn('prazo: feriado local: conferir', result['alertas'])
        self.assertTrue(any('vencido em 16/10/2026' in a for a in result['alertas']))
        self.ok('prazo', '--dados', '-', stdin=json.dumps(dict(DEADLINE, data_limite='2026-10-19')))
        self.assertTrue(any('último dia' in a for a in self.status()['alertas']))
        self.ok('prazo', '--dados', '-', stdin=json.dumps(DEADLINE))
        self.assertEqual(self.status()['alertas'], [])
        self.assertIn('- Prazo: data-limite 27/10/2026', (self.folder / 'registro.md').read_text(encoding='utf-8'))

    def test_deadline_rejects_incomplete_data(self):
        self.init()
        self.refused('prazo', '--dados', '-', stdin='{"abertura": "2026-10-30"}', contains='sem data_limite, alertas')
        self.refused('prazo', '--dados', '-', stdin='{', contains='não é JSON válido')
        self.refused('prazo', '--dados', '-', stdin='', contains='entrada vazia (os dados do prazo)')
        self.refused('prazo', '--dados', '-', stdin=' \n', contains='o comando anterior falhou')
        self.refused('prazo', '--dados', '-', stdin=json.dumps(dict(DEADLINE, data_limite='amanhã')),
                     contains='data_limite inválida')
        path = self.base / 'prazo.json'
        path.write_text(json.dumps(DEADLINE), encoding='utf-8')
        self.assertEqual(self.ok('prazo', '--dados', path)['prazo']['abertura'], '2026-10-30')

    def test_validar_detects_stray_draft_files(self):
        self.to_selection()
        self.include('IMP-20,IMP-100')
        self.ok('decidir', '--evidencia', 'descarto ESC-01 e ESC-02')
        self.ok('minuta', '--acao', 'abrir')
        self.write_draft('IMP-20')
        self.assertEqual(self.validate(), (0, []))
        self.write_draft('IMP-100')
        self.write_draft('ESC-01')
        (self.folder / 'minutas' / 'notas.txt').write_text('x', encoding='utf-8')
        code, found = self.validate()
        self.assertEqual(code, 1)
        self.assertIn('arquivo inesperado em minutas/: notas.txt', found)
        self.assertTrue(any(v.startswith('minutas/ESC-01.md: o item ESC-01 não está incluído') for v in found), found)
        self.assertTrue(any(v.startswith('minutas/IMP-100.md: minuta não aberta') for v in found), found)

    def test_validar_detects_broken_invariants(self):
        self.to_selection()
        self.include('IMP-20,IMP-100')

        def break_state(state):
            for item in state['itens'][:2]:
                item['minuta']['status'] = 'em_revisao'
            state['itens'][2]['decisao'] = 'descartar'
            state['itens'][3]['classe'] = 'esclarecimento'  # IMP-20
            state['peca']['esclarecimento'] = {'evidencia': 'confirmo', 'aprovadas': []}
        self.edit_state(break_state)
        code, found = self.validate()
        self.assertEqual(code, 1)
        joined = '\n'.join(found)
        for message in ('mais de uma minuta em revisão', 'decisão sem evidência', 'incoerente com o ID',
                        'peça de esclarecimento confirmada com itens não decididos'):
            self.assertIn(message, joined)

    def test_malformed_state_is_reported(self):
        self.init()
        (self.folder / 'estado.json').write_text('{', encoding='utf-8')
        code, found = self.validate()
        self.assertEqual(code, 1)
        self.assertIn('não é JSON válido', found[0])
        self.refused('status', contains='rode "validar"')
        code, _, err = run('status', '--pasta', self.base / 'nao-existe')
        self.assertEqual(code, 1)
        self.assertIn('iniciar', err)

    def test_events_use_replaceable_clock(self):
        self.init()
        self.clock = datetime(2026, 10, 20, 8, 0, 0, tzinfo=TZ)
        self.gate()
        state = json.loads((self.folder / 'estado.json').read_text(encoding='utf-8'))
        self.assertEqual([e['quando'] for e in state['eventos']],
                         ['2026-10-19T09:30:15-03:00', '2026-10-20T08:00:00-03:00'])
        self.assertEqual([e['acao'] for e in state['eventos']], ['iniciar', 'documentos'])

    def test_negative_answers_refused_by_format(self):
        self.init()
        self.gate('ETP')
        for phrase in ('não', 'não prossigo sem ETP', 'prossigo sem ETP?', 'prossigo sem ETP, mas mando depois'):
            with self.subTest(phrase=phrase):
                self.refused('prosseguir', '--evidencia', phrase, contains='"prossigo sem ETP"')
        self.assertEqual(self.status()['fase'], 'documentos')
        self.ok('prosseguir', '--evidencia', 'PROSSIGO SEM ETP!')
        self.add_items(ITEMS[1:2])
        self.refused('decidir', '--evidencia', 'não incluo IMP-100', contains='não está no formato do decidir')
        self.include('IMP-100')
        self.approve('IMP-100')
        (self.assets / 'modelo-impugnacao.docx').write_bytes(b'modelo')
        for phrase in ('não confirmo ainda', 'ainda não', 'confirmo a peça de impugnação em formato único?'):
            with self.subTest(phrase=phrase):
                self.refused('peca', '--acao', 'confirmar', '--evidencia', phrase,
                             contains='não está no formato da confirmação da peça')
        self.assertEqual(self.status()['fase'], 'peca_final')

    def test_validar_reports_numeric_duplicate_and_newline_id(self):
        self.to_selection(ITEMS[3:])
        self.edit_state(lambda state: state['itens'].append(dict(state['itens'][0], id='IMP-020')))
        code, found = self.validate()
        self.assertEqual(code, 1)
        self.assertIn('ID repetido: IMP-020 tem o mesmo número de IMP-20', found)
        self.edit_state(lambda state: state['itens'].pop())
        self.edit_state(lambda state: state['itens'][0].update(id='IMP-20\n'))
        code, found = self.validate()
        self.assertEqual(code, 1)
        self.assertTrue(any(v.startswith('ID fora do formato') for v in found), found)

    def test_hand_edited_state_is_reported_without_traceback(self):
        self.to_selection(ITEMS[3:])
        self.include('IMP-20')
        path = self.folder / 'estado.json'
        original = path.read_text(encoding='utf-8')
        edits = {
            'documentos.faltas': lambda s: s.update(documentos={'presentes': []}),
            'documentos.prosseguir': lambda s: s['documentos'].update(prosseguir='sim'),
            'peca.impugnacao': lambda s: s['peca'].update(impugnacao='sim'),
            'certame.slug': lambda s: s['certame'].pop('slug'),
            'eventos[5]': lambda s: s['eventos'].append('x'),  # depois de iniciar, documentos, itens e decidir
            'minuta.versao': lambda s: s['itens'][0]['minuta'].update(versao='1'),
            'minuta.historico': lambda s: s['itens'][0]['minuta'].update(historico=None),
            'prazo.alertas': lambda s: s.update(prazo={'abertura': None, 'data_limite': None, 'alertas': 'x'}),
        }
        for field, change in edits.items():
            with self.subTest(field=field):
                path.write_text(original, encoding='utf-8')
                self.edit_state(change)
                code, found = self.validate()
                self.assertEqual(code, 1)
                self.assertIn(field, '\n'.join(found))
                self.refused('status', contains='rode "validar"')
                self.refused('minuta', '--acao', 'abrir', contains='rode "validar"')

    def test_parallel_commands_do_not_lose_updates(self):
        self.to_selection([{'id': f'IMP-{n:02d}', 'classe': 'impugnacao', 'titulo': f'Ponto {n}'} for n in range(1, 9)])
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        base = [sys.executable, '-B', estado.__file__, 'decidir', '--pasta', str(self.folder)]
        processes = [subprocess.Popen(base + ['--evidencia', f'descarto IMP-{n:02d}'],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env) for n in range(1, 9)]
        for process in processes:
            _, err = process.communicate(timeout=60)
            self.assertEqual(process.returncode, 0, err)
        result = self.status()
        self.assertEqual(len(result['itens']['descartados']), 8)
        state = json.loads((self.folder / 'estado.json').read_text(encoding='utf-8'))
        self.assertEqual(sum(e['acao'] == 'decidir' for e in state['eventos']), 8)

    def test_input_not_in_utf8_refused_and_bom_accepted(self):
        self.init()
        self.gate()
        latin = json.dumps([{'id': 'IMP-01', 'classe': 'impugnacao', 'titulo': 'Cláusula'}], ensure_ascii=False)
        path = self.base / 'itens.json'
        path.write_bytes(latin.encode('latin-1'))
        self.refused('itens', '--arquivo', path, contains='como UTF-8')
        self.refused('itens', '--arquivo', '-', stdin=latin.encode('latin-1'), contains='como UTF-8')
        cp1252 = json.dumps(dict(DEADLINE, alertas=['feriado municipal: conferir']), ensure_ascii=False)
        self.refused('prazo', '--dados', '-', stdin=cp1252.replace('conferir', 'conferência').encode('cp1252'),
                     contains='como UTF-8')
        path.write_bytes(b'\xef\xbb\xbf' + latin.encode('utf-8'))
        self.assertEqual(self.ok('itens', '--arquivo', path)['itens']['pendentes'], ['IMP-01'])
        self.ok('prazo', '--dados', '-', stdin=json.dumps(DEADLINE).encode('utf-8'))

    def test_os_errors_and_long_slug_reported_without_traceback(self):
        not_a_folder = self.base / 'arquivo'
        not_a_folder.write_text('x', encoding='utf-8')
        code, _, err = run('iniciar', '--raiz', not_a_folder, '--orgao', 'X', '--modalidade', 'PE', '--numero', '1',
                           '--ano', '2026')
        self.assertEqual(code, 1)
        self.assertIn('não foi possível ler ou gravar', err)
        code, _, err = run('iniciar', '--raiz', self.root, '--orgao', 'a' * 300, '--modalidade', 'PE', '--numero', '1',
                           '--ano', '2026')
        self.assertEqual(code, 1)
        self.assertIn('--slug mais curto', err)
        self.assertFalse(self.root.exists())

    def test_existing_folder_without_state_is_reused(self):
        folder = self.root / 'secretaria-municipal-de-saude-de-exemplopolis-pe-90001-2026'
        (folder / 'texto').mkdir(parents=True)
        (folder / 'texto' / 'edital.txt').write_text('texto extraído\n', encoding='utf-8')
        code, _, err = run('status', '--pasta', folder)
        self.assertEqual(code, 1)
        self.assertIn(f'rode "iniciar --raiz {self.root.resolve()} --slug {folder.name}"', err)
        self.assertEqual(self.init()['fase'], 'documentos')
        self.assertEqual(self.folder, folder.resolve())
        self.assertTrue((folder / 'minutas' / 'historico').is_dir())
        self.assertEqual((folder / 'texto' / 'edital.txt').read_text(encoding='utf-8'), 'texto extraído\n')
        other = self.root / 'outra-pe-1-2026'
        other.mkdir()
        (other / 'notas.txt').write_text('x', encoding='utf-8')
        code, _, err = run('iniciar', '--raiz', self.root, '--orgao', 'Outra', '--modalidade', 'PE', '--numero', '1',
                           '--ano', '2026')
        self.assertEqual(code, 1)
        self.assertIn('tem notas.txt', err)

    def test_validar_rejects_forged_approval(self):
        self.to_selection()
        self.include('IMP-20,IMP-100')
        self.decide_rest('descartar')
        self.open_and_register('IMP-20')
        self.write_draft('IMP-100')

        def forge(state):
            for item in state['itens']:
                if item['decisao'] == 'incluir':
                    sha = comum.sha256_file(self.draft(item['id']))
                    item['evidencia'] = 'ok'
                    item['minuta'].update(status='aprovada', versao=1, evidencia='ok, aprova todas', sha256=sha)
        self.edit_state(forge)
        code, found = self.validate()
        self.assertEqual(code, 1)
        joined = '\n'.join(found)
        for message in ('IMP-20: decisão com evidência fora do formato',
                        'IMP-20: minuta aprovada com evidência fora do formato',
                        'IMP-20: minuta aprovada sem a decisão correspondente no histórico',
                        'IMP-100: minuta aprovada v1 sem o evento de registro dessa versão',
                        'IMP-20: minuta aprovada v1 sem o evento minuta_aprovar dessa versão'):
            self.assertIn(message, joined)

    def test_interrupted_adjust_can_be_repeated(self):
        self.to_selection(ITEMS[3:])
        self.include('IMP-20')
        self.open_and_register('IMP-20', 'versão 1\n')
        adjust = ('minuta', '--evidencia', 'ajuste IMP-20: citar a página do TR')
        with mock.patch.object(persistencia, 'write_atomic', side_effect=KeyboardInterrupt), \
                self.assertRaises(KeyboardInterrupt):
            self.call(*adjust)
        self.assertFalse(self.draft('IMP-20').exists())  # o arquivo já foi para o histórico; o estado não mudou
        result = self.ok(*adjust)
        self.assertEqual((result['minuta_em_revisao']['versao'], result['alertas']), (2, []))
        history = self.folder / 'minutas' / 'historico'
        self.assertEqual([p.name for p in history.iterdir()], ['IMP-20.v1.md'])
        self.assertEqual((history / 'IMP-20.v1.md').read_text(encoding='utf-8'), 'versão 1\n')
        self.assertEqual(self.validate(), (0, []))

    def test_nfc_path_finds_nfd_folder(self):
        name = 'Triagens de Licitação'
        nfd_root = self.base / unicodedata.normalize('NFD', name)
        nfc_root = self.base / unicodedata.normalize('NFC', name)
        self.root = nfd_root
        self.init()
        slug = self.folder.name
        code, out, err = run('status', '--pasta', nfc_root / slug)
        self.assertEqual(code, 0, err)
        self.assertEqual((json.loads(out)['fase'], json.loads(out)['pasta']), ('documentos', str(self.folder)))
        self.root = nfc_root
        code, _, err = self.start()
        self.assertEqual(code, 1)
        self.assertIn('já existe', err)
        self.assertEqual(len([p for p in self.base.iterdir() if p.is_dir() and p.name != 'assets']), 1)


    # Brechas fechadas no script (revisão da Fase 3).

    def test_cli_has_no_assets_or_manifest_option(self):
        self.init()
        self.assertEqual(fases.SKILL_DIR, Path(estado.__file__).resolve().parents[1])
        for args in (('peca', '--pasta', self.folder, '--acao', 'verificar', '--assets', self.assets),
                     ('status', '--pasta', self.folder, '--manifesto', self.manifest),
                     ('iniciar', '--raiz', self.root, '--orgao', 'X', '--modalidade', 'PE', '--numero', '2',
                      '--ano', '2026', '--manifesto', self.manifest),
                     ('peca', '--pasta', self.folder, '--acao', 'confirmar', '--tipo', 'impugnacao',
                      '--evidencia', 'confirmo a peça de impugnação em formato único'),
                     ('reabrir', '--pasta', self.folder, '--ids', 'IMP-01', '--evidencia', 'reabro IMP-01: motivo longo'),
                     ('minuta', '--pasta', self.folder, '--acao', 'aprovar')):
            with self.subTest(args=args), redirect_stderr(io.StringIO()) as err, \
                    self.assertRaises(SystemExit) as raised:
                estado.main([str(a) for a in args])
            self.assertEqual(raised.exception.code, 2)
            self.assertRegex(err.getvalue(), 'unrecognized arguments|invalid choice')

    def test_draft_decision_needs_the_id_in_review(self):
        self.to_selection()
        self.include('IMP-20,IMP-100,ESC-01')
        self.decide_rest('descartar')
        self.open_and_register('IMP-20')
        self.ok('minuta', '--evidencia', 'ajuste IMP-20: troque o pedido subsidiário pela republicação')
        self.write_draft('IMP-20', 'versão 2\n')
        self.ok('minuta', '--id', 'IMP-20', '--acao', 'registrar')
        self.ok('minuta', '--evidencia', 'aprovo IMP-20')
        self.open_and_register('IMP-100')
        # A frase de outra minuta não decide esta; a mesma frase com o ID certo vale de novo.
        self.refused('minuta', '--evidencia', 'aprovo IMP-20', contains='a frase cita IMP-20, mas a minuta em revisão '
                                                                       'é IMP-100')
        self.ok('minuta', '--evidencia', 'ajuste IMP-100: troque o pedido subsidiário pela republicação')
        self.write_draft('IMP-100', 'versão 2\n')
        self.ok('minuta', '--id', 'IMP-100', '--acao', 'registrar')
        self.ok('minuta', '--evidencia', 'descarto IMP-100')
        self.open_and_register('ESC-01')
        self.ok('minuta', '--evidencia', 'descarto ESC-01')
        self.ok('reabrir', '--evidencia', 'reabro IMP-20: quero rever o pedido subsidiário')
        self.include('IMP-20')
        self.open_and_register('IMP-20')
        self.assertEqual(self.ok('minuta', '--evidencia', 'aprovo IMP-20')['aprovadas'][0]['versao'], 3)
        self.assertEqual(self.validate(), (0, []))

    def test_survey_asks_deadline_only_when_missing(self):
        self.init()
        action = self.gate()['proxima_acao']
        self.assertIn('calcule o prazo', action)
        action = self.ok('prazo', '--dados', '-', stdin=json.dumps(DEADLINE))['proxima_acao']
        self.assertNotIn('prazo', action)
        self.assertIn('Faça o levantamento, um documento por vez, e registre os itens com "itens"', action)

    def test_piece_action_verifies_first_and_depends_on_model(self):
        self.to_selection()
        self.ok('prazo', '--dados', '-', stdin=json.dumps(DEADLINE))
        self.include('IMP-20,ESC-01')
        self.decide_rest('avaliar_depois')
        self.approve('IMP-20')
        result = self.approve('ESC-01')
        self.assertEqual(result['fase'], 'peca_final')
        action = result['proxima_acao']
        self.assertTrue(action.startswith('Todas as minutas foram decididas. Rode "peca --acao verificar" antes de '
                                          'qualquer pergunta'), action)
        self.assertIn('resolva as pendências que o comando listar', action)
        self.assertIn('Não há modelo da peça de impugnação nem da de esclarecimento em assets/', action)
        self.assertIn('e pare. Não pergunte o formato', action)
        self.assertNotIn('Há modelo', action)
        self.assertIn('itens para avaliar depois (IMP-100, ESC-02) e lembre que o prazo de impugnação está correndo '
                      '(data-limite 27/10/2026)', action)
        self.assertTrue(action.endswith('Não assine, não protocole, não envie.'), action)
        (self.assets / 'modelo-impugnacao.docx').write_bytes(b'modelo')
        action = self.status()['proxima_acao']
        self.assertIn('Não há modelo da peça de esclarecimento em assets/', action)
        self.assertIn('Há modelo para a peça de impugnação: pergunte o formato (único ou por ponto) separadamente '
                      'para cada tipo', action)
        self.assertIn('(por exemplo: "confirmo a peça de impugnação em formato único")', action)
        self.assertLess(action.index('peca --acao verificar'), action.index('pergunte o formato'))
        (self.assets / 'modelo-esclarecimento.docx').write_bytes(b'modelo')
        self.assertNotIn('Não há modelo', self.status()['proxima_acao'])
        self.clock = datetime(2026, 10, 28, 9, 0, 0, tzinfo=TZ)
        self.assertIn('(IMP-100, ESC-02) e lembre que o prazo de impugnação venceu em 27/10/2026',
                      self.status()['proxima_acao'])

    def test_status_shows_review_sha256_and_discarded_drafts(self):
        self.to_selection()
        self.include('IMP-20,IMP-100')
        self.decide_rest('descartar')
        self.approve('IMP-20')
        result = self.open_and_register('IMP-100')
        self.assertEqual(result['minuta_em_revisao']['sha256'], comum.sha256_file(self.draft('IMP-100')))
        self.assertEqual(result['minutas_descartadas'], [])
        result = self.ok('minuta', '--evidencia', 'descarto a IMP-100')
        self.assertEqual(result['minutas_descartadas'], ['IMP-100'])
        self.assertEqual([a['id'] for a in result['aprovadas']], ['IMP-20'])
        self.assertEqual(result['itens']['descartados'], ['ESC-01', 'ESC-02'])
        result = self.ok('reabrir', '--evidencia', 'reabro IMP-100: quero rever a IMP-100 com o TR novo')
        self.assertEqual(result['minutas_descartadas'], [])

    def integrity_file(self):
        return self.folder / '.estado.sha256'

    def hand_edit(self):
        self.edit_state(lambda state: state['itens'][0].update(titulo='Título corrigido à mão'))

    def test_hand_edit_is_detected_and_blocks_writes(self):
        self.to_selection(ITEMS[3:])
        state_path = self.folder / 'estado.json'
        self.assertEqual(self.integrity_file().read_text(encoding='utf-8'),
                         f'{comum.sha256_file(state_path)}  estado.json\n')
        self.assertEqual((self.status()['alertas'], self.validate()), ([], (0, [])))
        original = state_path.read_bytes()
        self.hand_edit()
        result = self.status()
        self.assertTrue(result['alertas'][0].startswith('estado.json foi alterado fora do estado.py'),
                        result['alertas'])
        self.assertIn('aceitar-edicao --pasta', result['proxima_acao'])
        self.assertIn('"aceito a edição do estado: <motivo>"', result['proxima_acao'])
        self.assertIn('Mostre a alteração ao analista', result['proxima_acao'])
        code, found = self.validate()
        self.assertEqual(code, 1)
        self.assertTrue(any(v.startswith('estado.json foi alterado fora do estado.py') for v in found), found)
        edited = state_path.read_bytes()
        writes = [('decidir', '--evidencia', 'incluo IMP-20'),
                  ('documentos', '--presentes', ','.join(comum.DOC_CODES)),
                  ('prazo', '--dados', '-'),
                  ('itens', '--arquivo', self.items_file([ITEMS[0]])),
                  ('minuta', '--acao', 'abrir'),
                  ('reabrir', '--evidencia', 'reabro IMP-20: mudei de ideia sobre o atestado'),
                  ('peca', '--acao', 'confirmar', '--evidencia', 'confirmo a peça de impugnação em formato único')]
        for command, *args in writes:
            with self.subTest(command=command):
                self.refused(command, *args, contains='estado.json foi alterado fora do estado.py',
                             stdin=json.dumps(DEADLINE))
                self.refused(command, *args, contains='Mostre a alteração ao analista', stdin=json.dumps(DEADLINE))
        self.assertEqual(state_path.read_bytes(), edited)
        check = self.ok('peca', '--acao', 'verificar')
        self.assertFalse(check['pronto'])
        self.assertTrue(check['pendencias'][0].startswith('estado.json foi alterado fora do estado.py'))
        state_path.write_bytes(original)  # desfeita exatamente, a alteração deixa de existir
        self.assertEqual(self.status()['alertas'], [])
        self.include('IMP-20')
        self.assertEqual(self.validate(), (0, []))

    def test_accept_edit_records_phrase_and_releases(self):
        self.to_selection(ITEMS[3:])
        self.refused('aceitar-edicao', '--evidencia', 'aceito a edição', contains='não há alteração a aceitar')
        self.hand_edit()
        for phrase, message in (('ok', 'não está no formato do aceite'), ('aceito a edição', 'não está no formato'),
                                ('não aceito a edição do estado: não fui eu', 'não está no formato'),
                                ('aceito a edição do estado? sim, mantenha', 'não está no formato'),
                                ('aceito a edição do estado: ok', 'menos de 10 caracteres')):
            with self.subTest(phrase=phrase):
                self.refused('aceitar-edicao', '--evidencia', phrase, contains=message)
        self.refused('aceitar-edicao', '--evidencia', 'ok', contains=f'Exemplo com os dados desta triagem: "{ACCEPT_EXAMPLE}"')
        self.refused('decidir', '--evidencia', 'incluo IMP-20', contains='alterado fora do estado.py')
        result = self.ok('aceitar-edicao', '--evidencia', 'Aceito a edição do estado: fui eu que corrigi o título')
        self.assertIn('Alteração do estado.json aceita', result['mensagem'])
        self.assertEqual(result['alertas'], [])
        self.assertEqual(self.validate(), (0, []))
        state = json.loads((self.folder / 'estado.json').read_text(encoding='utf-8'))
        self.assertEqual(state['itens'][0]['titulo'], 'Título corrigido à mão')
        self.assertEqual(state['eventos'][-1]['acao'], 'aceitar_edicao')
        self.assertIn('(itens[IMP-20].titulo), mantido pelo analista: "Aceito a edição do estado: fui eu que corrigi o '
                      'título"',
                      state['eventos'][-1]['detalhe'])
        self.include('IMP-20')
        self.refused('aceitar-edicao', '--evidencia', 'aceito a edição', contains='não há alteração a aceitar')

    def test_accept_edit_refuses_state_that_breaks_invariants(self):
        self.to_selection(ITEMS[3:])
        self.include('IMP-20')
        self.open_and_register('IMP-20')

        def forge(state):
            state['itens'][0]['minuta'].update(status='aprovada', evidencia='ok, aprova todas')
        self.edit_state(forge)
        self.refused('aceitar-edicao', '--evidencia', ACCEPT, contains='violações que o aceite não corrige')
        self.assertTrue(self.status()['alertas'][0].startswith('estado.json foi alterado fora do estado.py'))

    def test_deleted_integrity_file_is_detected(self):
        self.init()
        self.gate()
        self.integrity_file().unlink()
        result = self.status()
        self.assertTrue(result['alertas'][0].startswith('estado.json foi alterado fora do estado.py ou '
                                                        '.estado.sha256 foi apagado'), result['alertas'])
        self.assertEqual(self.validate()[0], 1)
        self.refused('itens', '--arquivo', self.items_file(ITEMS), contains='.estado.sha256 foi apagado')
        self.ok('aceitar-edicao', '--evidencia', ACCEPT)
        self.assertTrue(self.integrity_file().is_file())
        self.assertEqual(self.add_items()['alertas'], [])

    def test_old_folder_without_integrity_gets_it_on_next_save(self):
        self.init()
        self.gate()
        # Pasta criada antes do controle: formato 1, sem a marca, sem o .estado.sha256 e sem evento do controle.
        self.edit_state(lambda state: (state.pop('integridade'), state.update(formato=1)))
        self.integrity_file().unlink()
        result = self.status()
        self.assertEqual(len(result['alertas']), 1)
        self.assertIn('anterior ao controle de integridade', result['alertas'][0])
        self.assertIn('registre os itens', result['proxima_acao'])
        self.assertEqual(self.validate(), (0, []))
        self.refused('aceitar-edicao', '--evidencia', 'aceito a edição', contains='não há alteração a aceitar')
        result = self.add_items()
        self.assertEqual(result['alertas'], [])
        self.assertTrue(self.integrity_file().is_file())
        self.assertEqual(self.status()['alertas'], [])
        state = json.loads((self.folder / 'estado.json').read_text(encoding='utf-8'))
        self.assertIn('integridade', [e['acao'] for e in state['eventos']])
        self.assertEqual(self.validate(), (0, []))

    def test_interrupted_save_does_not_look_like_hand_edit(self):
        self.to_selection(ITEMS[3:])
        real = persistencia.write_atomic

        def crash_at(n):
            calls = []

            def write(path, text):
                calls.append(path.name)
                if len(calls) == n:
                    raise KeyboardInterrupt
                real(path, text)
            return write
        # 2: caiu antes de trocar o estado.json; 3: depois de trocá-lo, antes de fechar o .estado.sha256.
        for n, decision in ((2, 'pendente'), (3, 'incluir')):
            with self.subTest(crash_at=n):
                with mock.patch.object(persistencia, 'write_atomic', crash_at(n)), \
                        self.assertRaises(KeyboardInterrupt):
                    self.include('IMP-20')
                self.assertEqual(len(self.integrity_file().read_text(encoding='utf-8').splitlines()), 2)
                result = self.status()
                self.assertEqual((result['alertas'], result['itens']['incluidos'] == ['IMP-20']),
                                 ([], decision == 'incluir'))
                self.assertEqual(self.validate(), (0, []))
        self.include('IMP-20')
        self.assertEqual(len(self.integrity_file().read_text(encoding='utf-8').splitlines()), 1)

    # Brechas fechadas no script (segunda rodada).

    def resign(self):
        """Recalcula o .estado.sha256 depois da edição à mão: edição deliberada, que a integridade não pega."""
        path = self.folder / 'estado.json'
        self.integrity_file().write_text(f'{comum.sha256_file(path)}  estado.json\n', encoding='utf-8')

    def read_state(self):
        return json.loads((self.folder / 'estado.json').read_text(encoding='utf-8'))

    def test_validar_reapplies_the_formats(self):
        self.init()
        self.gate('ETP,PESQUISA')
        self.ok('prosseguir', '--evidencia', 'prossigo sem ETP e PESQUISA')
        self.add_items()
        self.ok('decidir', '--evidencia', 'incluo IMP-20 e ESC-01; descarto os demais')
        self.assertEqual(self.validate(), (0, []))
        self.assertNotIn('selecao', self.read_state()['itens'][0])

        def forge(state):
            state['documentos']['prosseguir']['evidencia'] = 'segue com o que tiver'
            next(item for item in state['itens'] if item['id'] == 'IMP-100')['decisao'] = 'incluir'
        self.edit_state(forge)
        self.resign()
        self.assertEqual(self.status()['alertas'], [])  # o hash confere: só o validar pega a edição
        code, found = self.validate()
        self.assertEqual(code, 1)
        joined = '\n'.join(found)
        for message in ('decisão de prosseguir sem o evento "prosseguir" correspondente',
                        'decisão de prosseguir com evidência fora do formato (a frase "segue com o que tiver" não está '
                        'no formato do prosseguir', 'IMP-100: decisão sem o evento "decidir" correspondente',
                        'IMP-100: decisão com evidência fora do formato (a frase não põe IMP-100 na cláusula de '
                        '"incluir")'):
            self.assertIn(message, joined)

    def test_accept_edit_covers_only_descriptive_fields(self):
        self.to_selection(ITEMS[3:])
        original = (self.folder / 'estado.json').read_bytes()

        def forge(state):  # inclusão forjada coerente: frase no formato e evento batem
            state['itens'][0].update(decisao='incluir', evidencia='incluo IMP-20',
                                     decidido_em='2026-10-19T09:30:15-03:00')
            state['eventos'].append({'quando': '2026-10-19T09:30:15-03:00', 'acao': 'decidir',
                                     'detalhe': 'IMP-20 → incluir: "incluo IMP-20"'})
        self.edit_state(forge)
        self.assertEqual(self.validate(), (1, [fases.TAMPERED['alterado']]))
        self.refused('aceitar-edicao', '--evidencia', ACCEPT, contains='a alteração mexe em eventos')
        self.refused('aceitar-edicao', '--evidencia', ACCEPT, contains='itens[IMP-20].decisao')
        (self.folder / 'estado.json').write_bytes(original)
        self.edit_state(lambda state: state['certame'].update(orgao='Prefeitura Fictícia'))
        result = self.ok('aceitar-edicao', '--evidencia', 'aceito a edição do estado: o órgão estava errado')
        self.assertEqual((result['certame']['orgao'], result['alertas']), ('Prefeitura Fictícia', []))
        self.assertIn('(certame.orgao)', self.read_state()['eventos'][-1]['detalhe'])
        (self.folder / '.estado.gravado.json').unlink()
        self.hand_edit()
        self.refused('aceitar-edicao', '--evidencia', ACCEPT, contains='não há cópia legível')

    def test_folder_with_control_does_not_become_old(self):
        self.init()
        self.gate()
        self.edit_state(lambda state: state.pop('integridade'))
        self.integrity_file().unlink()
        for formato, events in ((2, []), (1, [{'quando': 'x', 'acao': 'integridade', 'detalhe': 'x'}])):
            with self.subTest(formato=formato):
                self.edit_state(lambda state: (state.update(formato=formato), state['eventos'].extend(events)))
                self.assertTrue(self.status()['alertas'][0].startswith(
                    'estado.json foi alterado fora do estado.py ou .estado.sha256 foi apagado'))
                self.assertEqual(self.validate()[0], 1)
                self.refused('itens', '--arquivo', self.items_file(ITEMS), contains='.estado.sha256 foi apagado')

    def test_validar_without_state_creates_no_lock_and_names_integrity(self):
        folder = self.base / 'qualquer'
        folder.mkdir()
        code, _, _ = run('validar', '--pasta', folder)
        self.assertEqual((code, list(folder.iterdir())), (1, []))
        self.init()
        self.edit_state(lambda state: state['certame'].update(orgao='Órgão editado à mão'))
        code, _, err = self.call('validar')
        self.assertEqual(code, 1)
        self.assertIn('erro: 1 violação(ões) (invariante ou integridade).', err)

    def test_piece_model_must_be_exact_and_not_empty(self):
        self.to_selection(ITEMS[1:2])
        self.include('IMP-100')
        self.approve('IMP-100')
        for name, data in (('modelo-impugnacao.md~', b'modelo'), ('modelo-impugnacao.docx.bak', b'modelo'),
                           ('.modelo-impugnacao.docx', b'modelo'), ('modelo-impugnacao.v2.docx', b'modelo'),
                           ('modelo-impugnacao.swp', b'modelo'), ('modelo-impugnacao.docx', b'')):
            (self.assets / name).write_bytes(data)
        self.assertEqual(self.ok('peca', '--acao', 'verificar')['modelos'],
                         {'impugnacao': None, 'esclarecimento': None})
        self.assertIn('Não há modelo da peça de impugnação', self.status()['proxima_acao'])
        self.refused('peca', '--acao', 'confirmar', '--evidencia', 'confirmo a peça de impugnação em formato único',
                     contains='só sai quando o modelo existir')
        (self.assets / 'modelo-impugnacao.docx').write_bytes(b'modelo')
        self.assertTrue(self.ok('peca', '--acao', 'verificar')['modelos']['impugnacao'].endswith(
            'modelo-impugnacao.docx'))

    def test_piece_confirmation_takes_kind_and_format_from_the_phrase(self):
        self.to_selection(ITEMS[1:2])
        self.include('IMP-100')
        self.approve('IMP-100')
        (self.assets / 'modelo-impugnacao.docx').write_bytes(b'modelo')
        (self.assets / 'modelo-esclarecimento.docx').write_bytes(b'modelo')
        for phrase, message in (('Confirmo a peça', 'não está no formato da confirmação da peça'),
                                ('confirmo a peça de impugnação', 'não está no formato'),
                                ('confirmo a peça única', 'não está no formato'),
                                ('confirmo a peça de impugnação em formato tanto faz', 'não está no formato'),
                                ('Confirmo a peça', '"confirmo a peça de impugnação em formato único"'),
                                ('confirmo a peça de esclarecimento em formato único',
                                 'não há minuta de esclarecimento aprovada')):
            with self.subTest(phrase=phrase):
                self.refused('peca', '--acao', 'confirmar', '--evidencia', phrase, contains=message)
        self.refused('peca', '--acao', 'confirmar', contains='informe --evidencia')
        result = self.ok('peca', '--acao', 'confirmar', '--evidencia', 'Confirmo a peça de Impugnação em formato por ponto.')
        self.assertEqual(result['peca']['impugnacao']['formato'], 'por_ponto')
        self.assertEqual(self.validate(), (0, []))
        self.edit_state(lambda state: state['peca']['impugnacao'].update(formato='unico'))
        self.resign()
        self.assertIn('peça de impugnação confirmada com evidência fora do formato (a frase confirma a peça de '
                      'impugnação em formato por_ponto, não a gravada)', '\n'.join(self.validate()[1]))


if __name__ == '__main__':
    unittest.main()
