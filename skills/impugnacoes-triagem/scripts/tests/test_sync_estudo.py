import io
import json
import sys
import tempfile
import unicodedata
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import sync_estudo
from sync_estudo import CATALOG, DOCUMENTS, OMITTED_ROWS, sha256

CATALOG_TEXT = '''# 01 - Catálogo de Fontes

Fontes dos arquivos `Estrutura - *.md` e `Analise - *.md`. Os mapas `Fontes - {Documento}.md` citam só o ID (ver `Minhas observacoes.md` e `02 - Plano do Mapeamento de Fontes.md`).

| Sigla | Arquivo |
| :-- | :-- |
| ED-E | `Edital/Estrutura - Edital.md` |

## 1. Fontes internas

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| INT-EDITAL | Edital da licitação | Documento | do ente | PNCP | ED-F | n/a |

## 2. Legislação

| ID | Nome | Tipo | Esfera | Onde consultar | Usado em | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| EXT-LEI14133-ART164 | Art. 164: impugnação até 3 dias úteis antes da abertura | Lei | federal (nacional) | Planalto | ED-F | conferido |
| EXT-TCU-AC1-2020 | Acórdão 1/2020: citação errada. Não usar | Acórdão | federal | TCU | ED-A | a conferir |
| EXT-PEND-TESE | **Resolvido:** ver `EXT-LEI14133-ART164` | Pendência | federal | TCU | — | resolvida |

## 9. Conferência

Detalhes em `briefing/Auditoria_Estrutura/01 - Edital.md`. A divergência está no plano, seção 7, item 10.

| ID | Por que | O que fazer |
| :-- | :-- | :-- |
| EXT-TCU-AC1-2020 | Número errado | Não citar |
'''


HEADER = ('| Ponto a verificar | Fontes internas (ID + seção) | Fontes externas (IDs) | Prova | Gera impugnação se… '
          '| Descarta se… |\n| :-- | :-- | :-- | :-- | :-- | :-- |\n')


def omitted_rows(target, skip=()):
    """Tabela com as linhas sobre ato da RERI que o sync precisa achar e omitir."""
    points = [point for name, point in OMITTED_ROWS if name == target and point not in skip]
    if not points:
        return ''
    return '\n' + HEADER + ''.join(f'| {point} | INT-RERI (resposta) | EXT-LEI14133-ART164 | p | g | d |\n'
                                   for point in points)


def make_source(root, extra=None, skip=()):
    """Árvore mínima do estudo; a pasta do TR fica em NFD, como nos arquivos copiados de outro sistema."""
    (root / CATALOG[0]).write_text(CATALOG_TEXT, encoding='utf-8')
    for folder, dst_folder, _, files in DOCUMENTS:
        name = unicodedata.normalize('NFD', folder) if folder.startswith('Termo') else folder
        (root / name).mkdir()
        for src, dst in files:
            body = f'# {src}\n\nVer `Fontes - Edital.md` e `Edital/Estrutura - Edital.md`. Fonte: `EXT-LEI14133-ART164`.\n'
            body += omitted_rows(f'{dst_folder}/{dst}', skip)
            (root / name / src).write_text(body + (extra or {}).get(src, ''), encoding='utf-8')
    return root


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = sync_estudo.main([str(a) for a in args])
    return code, out.getvalue(), err.getvalue()


class SyncEstudoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.source = base / 'origem'
        self.source.mkdir()
        self.target = base / 'destino'

    def tearDown(self):
        self.tmp.cleanup()

    def sync(self, *extra):
        return run('--origem', self.source, '--destino', self.target, *extra)

    def test_copy_renames_files_and_rewrites_references(self):
        make_source(self.source)
        code, _, err = self.sync()
        self.assertEqual(code, 0, err)
        text = (self.target / 'tr' / 'estrutura.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('<!-- Cópia gerada por scripts/sync_estudo.py'))
        self.assertIn('`edital/fontes.md`', text)
        self.assertIn('`edital/estrutura.md`', text)
        self.assertNotIn('Fontes - Edital.md', text)
        catalog = (self.target / 'catalogo-fontes.md').read_text(encoding='utf-8')
        self.assertNotIn('Minhas observacoes', catalog)
        self.assertIn('`*/estrutura.md` e `*/analise.md`', catalog)
        self.assertIn('`*/fontes.md`', catalog)
        self.assertIn('Detalhes na auditoria de estrutura do repositório de origem.', catalog)
        self.assertIn('no plano do mapeamento (repositório de origem), seção 7', catalog)

    def test_nfd_folder_is_found_and_target_names_are_ascii(self):
        make_source(self.source)
        self.assertEqual(self.sync()[0], 0)
        names = [p.relative_to(self.target).as_posix() for p in self.target.rglob('*') if p.is_file()]
        self.assertIn('tr/fontes.md', names)
        self.assertTrue(all(n.isascii() for n in names))
        self.assertEqual(len(names), 22)

    def test_check_detects_missing_outdated_and_extra_files(self):
        make_source(self.source)
        self.assertEqual(self.sync('--check')[0], 1)  # ainda não há cópia
        self.assertEqual(self.sync()[0], 0)
        self.assertEqual(self.sync('--check')[0], 0)
        (self.target / 'edital' / 'fontes.md').write_text('editado à mão', encoding='utf-8')
        code, out, _ = self.sync('--check')
        self.assertEqual(code, 1)
        self.assertIn('desatualizado: edital/fontes.md', out)
        self.assertEqual(self.sync()[0], 0)
        (self.target / 'solto.md').write_text('x', encoding='utf-8')
        code, out, _ = self.sync('--check')
        self.assertEqual(code, 1)
        self.assertIn('sobrando: solto.md', out)

    def test_write_removes_stale_files(self):
        make_source(self.source)
        self.sync()
        (self.target / 'velho').mkdir()
        (self.target / 'velho' / 'x.md').write_text('x', encoding='utf-8')
        self.assertEqual(self.sync()[0], 0)
        self.assertFalse((self.target / 'velho').exists())

    def test_unknown_id_blocks_copy(self):
        make_source(self.source, {'Fontes - ETP.md': 'Ver `EXT-NAO-EXISTE`.\n'})
        code, _, err = self.sync()
        self.assertEqual(code, 1)
        self.assertIn('etp/fontes.md: ID sem linha no catálogo: EXT-NAO-EXISTE', err)
        self.assertFalse(self.target.exists())

    def test_reference_to_excluded_file_blocks_copy(self):
        make_source(self.source, {'Analise - Minuta Contratual.md': 'Ver `Minhas observacoes.md`.\n'})
        code, _, err = self.sync()
        self.assertEqual(code, 1)
        self.assertIn('minuta/analise.md: referência a arquivo fora da cópia', err)

    def test_reri_is_left_out_and_its_citations_lose_the_path(self):
        make_source(self.source, {'Fontes - Edital.md': 'Ver `Fontes - RERI.md`, seção 1, e '
                                  '`Retificações, Esclarecimentos e Respostas/Estrutura - RERI.md`.\n'})
        reri = self.source / 'Retificações, Esclarecimentos e Respostas'
        reri.mkdir()
        (reri / 'Fontes - RERI.md').write_text('# Fontes - RERI\n', encoding='utf-8')
        code, _, err = self.sync()
        self.assertEqual(code, 0, err)
        self.assertFalse((self.target / 'reri').exists())
        text = (self.target / 'edital' / 'fontes.md').read_text(encoding='utf-8')
        self.assertIn('Ver o mapa da RERI (processo à parte), seção 1, e a Estrutura da RERI (processo à parte).', text)
        self.assertNotIn('RERI.md', text)

    def test_scope_removes_reri_sentences_column_and_cells(self):
        make_source(self.source, {'Fontes - Edital.md': (
            '\n**Como usar:** leia a pergunta. Para toda seção, confira também `INT-RERI` (retificações): uma errata '
            'pode ter alterado a cláusula (ver `Fontes - RERI.md`, seção 1). Normas federais valem só para a União.\n\n'
            + HEADER +
            '| Data da sessão | INT-EDITAL (seção 1); INT-RERI (avisos); INT-EDITAL (seções 5; 9) | EXT-LEI14133-ART164 '
            '| p | g | d |\n'
            '| Só a RERI | INT-RERI | EXT-LEI14133-ART164 | p | g | d |\n\n'
            'Legenda. `INT-RERI` vale para todas as seções (ver "Como usar"); o ✓ marca a fonte direta. Fim.\n\n'
            '| Seção | INT-EDITAL | INT-RERI | Externas principais |\n| :-- | :-- | :-- | :-- |\n'
            '| 1. Preâmbulo | 6 | ✓ | EXT-LEI14133-ART164 |\n')})
        code, _, err = self.sync()
        self.assertEqual(code, 0, err)
        text = (self.target / 'edital' / 'fontes.md').read_text(encoding='utf-8')
        self.assertIn('leia a pergunta. Normas federais valem só para a União.', text)
        self.assertIn('Legenda. Fim.', text)
        self.assertIn('| Data da sessão | INT-EDITAL (seção 1); INT-EDITAL (seções 5; 9) |', text)
        self.assertIn('| Só a RERI | — |', text)
        self.assertIn('| Seção | INT-EDITAL | Externas principais |\n| :-- | :-- | :-- |\n| 1. Preâmbulo | 6 | EXT-', text)
        self.assertNotIn('INT-RERI', text)
        for _, point in OMITTED_ROWS:
            self.assertNotIn(point, text)
        manifest = json.loads((self.target / 'MANIFEST.json').read_text(encoding='utf-8'))
        changes = manifest['escopo_triagem']['ajustes_por_arquivo']['edital/fontes.md']
        self.assertEqual((changes['frases_retiradas'], changes['colunas_retiradas'], changes['celulas_limpas']), (2, 1, 2))
        self.assertEqual(changes['linhas_omitidas'], [p for n, p in OMITTED_ROWS if n == 'edital/fontes.md'])
        self.assertIn('linhas_omitidas', manifest['escopo_triagem']['ajustes_por_arquivo']['minuta/fontes.md'])

    def test_missing_row_to_omit_blocks_copy(self):
        point = next(p for n, p in OMITTED_ROWS if n == 'planilha/fontes.md')
        make_source(self.source, skip={point})
        code, _, err = self.sync()
        self.assertEqual(code, 1)
        self.assertIn(f'planilha/fontes.md: linha a omitir não encontrada na origem: "{point}"', err)
        self.assertFalse(self.target.exists())

    def test_leftover_int_reri_blocks_copy(self):
        make_source(self.source, {'Fontes - ETP.md': 'Prova: ver o `INT-RERI` publicado.\n'})
        code, _, err = self.sync()
        self.assertEqual(code, 1)
        self.assertIn('etp/fontes.md: INT-RERI sobrou na cópia', err)

    def test_wildcard_is_not_treated_as_id(self):
        make_source(self.source, {'Fontes - Edital.md': 'Não cite `EXT-PEND-*` nem `INT-*`.\n'})
        self.assertEqual(self.sync()[0], 0)

    def test_index_marks_sources_that_cannot_be_cited(self):
        make_source(self.source, {'Fontes - Edital.md': 'Ver `EXT-PEND-TESE`.\n'})
        code, out, _ = self.sync()
        self.assertEqual(code, 0)
        self.assertIn('aviso: edital/fontes.md: cita EXT-PEND-TESE, marcado como não (histórico)', out)
        index = (self.target / 'indice-fontes.md').read_text(encoding='utf-8')
        self.assertIn('| EXT-PEND-TESE |', index)
        self.assertIn('| resolvida | não (histórico) |', index)
        self.assertIn('| a conferir | não (citação errada) |', index)
        self.assertIn('| conferido | sim |', index)
        # A tabela de 3 colunas da seção 9 não vira linha de definição.
        self.assertEqual(index.count('| EXT-TCU-AC1-2020 |'), 1)

    def test_manifest_hashes_match_files_and_track_source_changes(self):
        make_source(self.source)
        self.sync()
        manifest = json.loads((self.target / 'MANIFEST.json').read_text(encoding='utf-8'))
        for item in manifest['arquivos']:
            self.assertEqual(sha256((self.target / item['destino']).read_bytes()), item['sha256_destino'])
        before = manifest['estudo_sha256']
        catalog = self.source / CATALOG[0]
        catalog.write_text(catalog.read_text(encoding='utf-8') + '\nNova nota.\n', encoding='utf-8')
        self.sync()
        after = json.loads((self.target / 'MANIFEST.json').read_text(encoding='utf-8'))['estudo_sha256']
        self.assertNotEqual(before, after)

    @unittest.skipUnless(sync_estudo.DEFAULT_SOURCE.exists(), 'estudo de origem fora deste checkout')
    def test_real_copy_is_in_sync_with_briefing(self):
        code, out, err = run('--check')
        self.assertEqual(code, 0, out + err)


if __name__ == '__main__':
    unittest.main()
