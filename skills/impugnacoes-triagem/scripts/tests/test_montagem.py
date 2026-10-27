import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


import estado
import montar_peca
from montagem import modelo, pontos
from triagem import comum, fases
from triagem.comum import Refusal

ASSETS_SOURCE = Path(__file__).resolve().parents[2] / 'assets'
TZ = timezone(timedelta(hours=-3))
# Dados fictícios.
ITEMS = [{'id': 'IMP-01', 'classe': 'impugnacao', 'titulo': 'Capital e patrimônio cumulativos'},
         {'id': 'IMP-02', 'classe': 'impugnacao', 'titulo': 'Atestado sem pertinência'},
         {'id': 'ESC-01', 'classe': 'esclarecimento', 'titulo': 'Categoria da convenção'}]
DADOS = {'destinatario': 'PREGOEIRO DA SECRETARIA MUNICIPAL DE EXEMPLÓPOLIS', 'setor_orgao': 'Diretoria de Compras',
         'endereco_orgao': 'Rua Exemplo, 100, Centro, Exemplópolis/UF', 'uasg': '123456',
         'item_impugnacao': 'item 19.1', 'objeto': 'a contratação de serviços de limpeza',
         'opcionais': {'atual_prestadora': False, 'republicacao': False, 'efeito_suspensivo': False,
                       'prova_documental': False, 'protesto': False}}
def run(*args, stdin=''):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err), mock.patch('sys.stdin', io.StringIO(stdin)):
        code = estado.main([str(a) for a in args])
    return code, out.getvalue(), err.getvalue()


REPRESENTANTE = {'nome': 'Pessoa Fictícia', 'cargo': 'Sócia Administradora', 'designacao': 'sua sócia administradora'}


def imp_draft(item_id, title, clause='Item 8.6.3 do Edital', extra=''):
    return f"""# {item_id} — {title}

- ID: {item_id}
- Versão: v1
- Certame: Órgão Exemplo — Pregão Eletrônico 111/2026
- Item do levantamento: levantamento.md, {item_id}
- Data: 2026-10-20
- Cláusula: {clause}
- Vício (resumo): Cumulação vedada
- Pedido (resumo): Exigir um dos parâmetros

## Dos fatos

1. O edital dispõe:

   > "8.6.3. A licitante deverá comprovar, cumulativamente: a) capital social; b) patrimônio líquido."
   >
   > (Edital, item 8.6.3, página PDF 23)

2. O Termo de Referência repete a exigência.{extra}

## Da fundamentação

### Normas e jurisprudência

1. A Lei 14.133/2021, no art. 69, § 4º, admite capital ou patrimônio [EXT-LEI14133-ART69 · conferido].

### Aplicação ao caso

1. O item exige os dois ao mesmo tempo.

### Resposta ao contraponto da Administração

1. A garantia contratual já cobre o risco [EXT-LEI14133-ART98 · conferido].

## Do pedido

### Pedido principal

1. A retificação do item 8.6.3 do edital, para exigir um dos parâmetros.

2. A divulgação da alteração na forma do art. 55, § 1º [EXT-LEI14133-ART55 · conferido].

### Pedido subsidiário

Não há: o vício tem uma única correção.

### Redação retificadora sugerida

> "8.6.3. A licitante deverá comprovar patrimônio líquido mínimo de 10%."

## Provas e anexos indicados

1. Edital, item 8.6.3.

## Pendências de conferência

1. Conferir a Súmula no catálogo de fontes.
"""


ESC_DRAFT = """# ESC-01 — Categoria da convenção

- ID: ESC-01
- Versão: v1

## Da dúvida

1. O Termo de Referência nomeia os postos de dois modos.

## Da pergunta

1. Qual categoria corresponde aos postos?
2. Qual CBO a Administração adotou?

## Do fundamento

1. O pedido tem por base o art. 164 da Lei 14.133/2021 [EXT-LEI14133-ART164 · conferido].

2. A categoria é necessária para a declaração do art. 63, § 1º [EXT-LEI14133-ART63 · conferido].

## Pendências de conferência

Nenhuma.
"""


class MontagemTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.root = self.base / 'files' / 'triagens'
        self.assets = self.base / 'assets'
        self.assets.mkdir()
        for kind in ('impugnacao', 'esclarecimento'):
            shutil.copy(ASSETS_SOURCE / f'modelo-{kind}.md', self.assets / f'modelo-{kind}.md')
        manifest = self.base / 'MANIFEST.json'
        manifest.write_text(json.dumps({'estudo_sha256': 'a' * 64}), encoding='utf-8')
        clock = datetime(2026, 10, 19, 9, 30, tzinfo=TZ)
        for patcher in (mock.patch.object(comum, 'now', lambda: clock),
                        mock.patch.object(fases, 'MANIFEST', manifest),
                        mock.patch.object(fases, 'ASSETS', self.assets)):
            patcher.start()
            self.addCleanup(patcher.stop)

    def tearDown(self):
        self.tmp.cleanup()

    def ok(self, *args, stdin=''):
        code, out, err = run(args[0], '--pasta', self.folder, *args[1:], stdin=stdin)
        self.assertEqual(code, 0, err)
        return json.loads(out)

    def approve(self, item_id, text):
        self.ok('minuta', '--acao', 'abrir')
        (self.folder / 'minutas' / f'{item_id}.md').write_text(text, encoding='utf-8')
        self.ok('minuta', '--id', item_id, '--acao', 'registrar')
        self.ok('minuta', '--evidencia', f'aprovo {item_id}')

    def triage(self, formato='único', imp_text=None, dados=DADOS):
        code, out, err = run('iniciar', '--raiz', self.root, '--orgao', 'Secretaria de Exemplópolis', '--modalidade',
                             'PE', '--numero', '111', '--ano', '2026', '--esfera', 'municipal')
        self.assertEqual(code, 0, err)
        self.folder = Path(json.loads(out)['pasta'])
        self.ok('documentos', '--presentes', ','.join(comum.DOC_CODES), '--faltas', '')
        deadline = {'abertura': '2026-10-30', 'data_limite': '2026-10-27', 'alertas': []}
        self.ok('prazo', '--dados', '-', stdin=json.dumps(deadline))
        items = self.base / 'itens.json'
        items.write_text(json.dumps(ITEMS, ensure_ascii=False), encoding='utf-8')
        self.ok('itens', '--arquivo', items)
        self.ok('decidir', '--evidencia', 'incluo os demais')
        self.approve('IMP-01', imp_text or imp_draft('IMP-01', 'Capital e patrimônio cumulativos'))
        self.approve('IMP-02', imp_draft('IMP-02', 'Atestado sem pertinência', 'Item 8.5.1 do Edital'))
        self.approve('ESC-01', ESC_DRAFT)
        for kind in ('impugnação', 'esclarecimento'):
            self.ok('peca', '--acao', 'confirmar', '--evidencia', f'confirmo a peça de {kind} em formato {formato}')
        (self.folder / 'documentos.md').write_text('- Processo administrativo: 0001/2026 (preâmbulo, p. PDF 1)\n',
                                                   encoding='utf-8')
        (self.folder / 'dados-peca.json').write_text(json.dumps(dados, ensure_ascii=False), encoding='utf-8')
        (self.base / 'files' / 'representante.json').write_text(json.dumps(REPRESENTANTE, ensure_ascii=False),
                                                                encoding='utf-8')

    def assemble(self, kind='impugnacao'):
        from montagem.montar import assemble
        return assemble(self.folder, kind, when=date(2026, 10, 20))

    def test_impugnation_single_piece(self):
        self.triage()
        [path] = self.assemble()
        text = path.read_text(encoding='utf-8')
        self.assertEqual(path.name, 'peca-impugnacao.md')
        for expected in ('**ILUSTRÍSSIMO SENHOR PREGOEIRO DA SECRETARIA MUNICIPAL DE EXEMPLÓPOLIS.**',
                         'Pregão Eletrônico nº 111/2026 – Processo Administrativo nº 0001/2026 – UASG 123456.',
                         'prazo encerra-se em 27/10/2026', 'em 20/10/2026', '20 de outubro de 2026',
                         '**III.1 – CAPITAL E PATRIMÔNIO CUMULATIVOS**', '**III.2 – ATESTADO SEM PERTINÊNCIA**',
                         '| III.2 | Item 8.5.1 do Edital | Cumulação vedada | Exigir um dos parâmetros |',
                         'ao final dos itens III.1 a III.2', 'Desta forma, **IMPUGNA-SE** o edital e seus anexos',
                         '1. a retificação do item 8.6.3 do edital, para exigir um dos parâmetros;',
                         'Sugere-se a seguinte redação:', '> (Edital, item 8.6.3, página 23)',
                         'neste ato representada por sua sócia administradora, Pessoa Fictícia'):
            self.assertIn(expected, text)
        self.assertIn('com o acolhimento dos pedidos deduzidos ao final dos itens III.1 a III.2', text)
        for absent in ('EXT-', '·', 'PDF', 'subsidiários deduzidos', '{{', 'Dos fatos', 'Normas e jurisprudência', 'Pendências', 'Provas e anexos',
                       'DA NECESSIDADE', 'EFEITO SUSPENSIVO', 'atual prestadora', 'Protesta', 'nova divulgação e',
                       'Não há', 'catálogo'):
            self.assertNotIn(absent, text)

    def test_optional_blocks_follow_dados(self):
        dados = dict(DADOS, opcionais={key: True for key in DADOS['opcionais']})
        self.triage(dados=dados)
        text = self.assemble()[0].read_text(encoding='utf-8')
        for expected in ('# DA NECESSIDADE DE SANEAMENTO E DA REPUBLICAÇÃO', 'EFEITO SUSPENSIVO',
                         'atual prestadora', 'Protesta a Impugnante', 'prova documental suplementar',
                         'com nova divulgação e reabertura do prazo'):
            self.assertIn(expected, text)

    def test_subsidiary_wording_follows_drafts(self):
        text = imp_draft('IMP-01', 'Capital').replace('Não há: o vício tem uma única correção.',
                                                      '1. A motivação expressa da exigência cumulativa.')
        self.triage(imp_text=text)
        piece = self.assemble()[0].read_text(encoding='utf-8')
        self.assertIn('pedidos principais e subsidiários deduzidos', piece)
        self.assertIn('1. subsidiariamente, a motivação expressa da exigência cumulativa;', piece)

    def test_optional_choice_must_be_explicit(self):
        dados = dict(DADOS, opcionais={'atual_prestadora': False})
        self.triage(dados=dados)
        with self.assertRaisesRegex(Refusal, 'opcionais.republicacao'):
            self.assemble()

    def test_per_point_has_one_piece_each_without_quadro(self):
        self.triage(formato='por ponto')
        paths = self.assemble()
        self.assertEqual([p.name for p in paths], ['peca-impugnacao-IMP-01.md', 'peca-impugnacao-IMP-02.md'])
        text = paths[1].read_text(encoding='utf-8')
        self.assertIn('**III.1 – ATESTADO SEM PERTINÊNCIA**', text)
        self.assertIn('ao final do item III.1', text)
        self.assertNotIn('QUADRO', text)
        self.assertNotIn('| #', text)

    def test_clarification(self):
        self.triage()
        text = self.assemble('esclarecimento')[0].read_text(encoding='utf-8')
        self.assertIn('**QUESITO 1 – Categoria da convenção**', text)
        self.assertIn('Indaga-se:\n\n1. Qual categoria corresponde aos postos?\n1. Qual CBO', text)
        self.assertIn('A categoria é necessária para a declaração do art. 63, § 1º.', text)
        self.assertNotIn('O pedido tem por base o art. 164', text)

    def test_quadro_needs_header_fields(self):
        text = imp_draft('IMP-01', 'Capital').replace('- Vício (resumo): Cumulação vedada\n', '')
        self.triage(imp_text=text)
        with self.assertRaisesRegex(Refusal, r'IMP-01 \(Vício \(resumo\)\)'):
            self.assemble()

    def test_internal_reference_blocks_piece(self):
        self.triage(imp_text=imp_draft('IMP-01', 'Capital', extra=' Ver o catálogo de fontes.'))
        with self.assertRaisesRegex(Refusal, 'referência interna'):
            self.assemble()
        self.assertFalse((self.folder / 'peca' / 'peca-impugnacao.md').exists())

    def test_service_catalog_is_not_internal(self):
        self.triage(imp_text=imp_draft('IMP-01', 'Capital', extra=' O código consta do Catálogo de Serviços.'))
        self.assertIn('Catálogo de Serviços', self.assemble()[0].read_text(encoding='utf-8'))

    def test_requires_confirmation_and_unchanged_drafts(self):
        self.triage()
        self.ok('reabrir', '--evidencia', 'reabro ESC-01: o analista quer rever a pergunta')
        with self.assertRaisesRegex(Refusal, 'pendências'):
            self.assemble('esclarecimento')

    def test_piece_after_deadline_refused(self):
        self.triage()
        from montagem.montar import assemble
        with self.assertRaisesRegex(Refusal, 'posterior à data-limite'):
            assemble(self.folder, 'impugnacao', when=date(2026, 10, 28))
        self.assertFalse((self.folder / 'peca').exists())

    def test_changed_draft_after_approval_refused(self):
        self.triage()
        (self.folder / 'minutas' / 'IMP-01.md').write_text('# IMP-01 — outro texto\n', encoding='utf-8')
        with self.assertRaisesRegex(Refusal, 'alterada ou removida depois de aprovada'):
            self.assemble()

    def test_cli_assemble(self):
        self.triage()
        piece = self.folder / 'peca' / 'peca-impugnacao.md'
        with redirect_stdout(io.StringIO()):
            self.assertEqual(montar_peca.main(['montar', '--pasta', str(self.folder), '--tipo', 'impugnacao',
                                               '--data', '2026-10-20']), 0)
        self.assertTrue(piece.is_file())
        self.assertFalse(piece.with_suffix('.docx').exists())


class ModeloTests(unittest.TestCase):
    def test_blocks_inline_and_by_line(self):
        template = '---\ntipo: x\n---\nA{{#X}} b{{/X}}{{#Y}} c{{/Y}}.\n{{#Y}}\nlinha {{CAMPO}}\n{{/Y}}\nfim\n'
        self.assertEqual(modelo.fill(template, {'CAMPO': 'v'}, {'X': True}), 'A b.\nfim\n')
        self.assertEqual(modelo.fill(template, {'CAMPO': 'v'}, {'Y': True}), 'A c.\nlinha v\nfim\n')

    def test_missing_field_and_unbalanced_block(self):
        with self.assertRaisesRegex(Refusal, 'CAMPO'):
            modelo.fill('{{CAMPO}}\n', {}, {})
        with self.assertRaisesRegex(Refusal, 'sem fechamento'):
            modelo.fill('{{#X}}\ntexto\n', {}, {})

    def test_markers_removed_from_points(self):
        body, row = pontos.impugnation(imp_draft('IMP-01', 'Capital'), 'IMP-01', 'III.1')
        self.assertNotIn('[', body.replace('[...]', ''))
        self.assertEqual(row, ['III.1', 'Item 8.6.3 do Edital', 'Cumulação vedada', 'Exigir um dos parâmetros'])

    def test_pages_as_the_administration_sees_them(self):
        cases = {'(Edital, item 8.6.3, página PDF 23)': '(Edital, item 8.6.3, página 23)',
                 'item 12.3 (página PDF 52, página impressa 18)': 'item 12.3 (página 18)',
                 'ETP, páginas PDF 61 a 72': 'ETP, páginas 61 a 72',
                 'Edital, p. PDF 23 (impr. 21)': 'Edital, p. 21'}
        for source, expected in cases.items():
            self.assertEqual(pontos.clean(source), expected)


if __name__ == '__main__':
    unittest.main()
