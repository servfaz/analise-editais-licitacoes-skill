#!/usr/bin/env python3
"""Copia o estudo de briefing/Mapeamento_Analise para references/estudo da skill. Python 3.10+.

Uso:
  sync_estudo.py           gera ou atualiza a cópia
  sync_estudo.py --check   só confere; sai com 1 se a cópia estiver desatualizada ou inválida
"""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = SKILL_DIR.parents[1] / 'briefing' / 'Mapeamento_Analise'
DEFAULT_TARGET = SKILL_DIR / 'references' / 'estudo'
SOURCE_LABEL = 'briefing/Mapeamento_Analise'

CATALOG = ('01 - Catalogo de Fontes.md', 'catalogo-fontes.md')
# (pasta de origem, pasta de destino, título, [(arquivo de origem, arquivo de destino)])
DOCUMENTS = [
    ('Edital', 'edital', 'Edital', [
        ('Estrutura - Edital.md', 'estrutura.md'),
        ('Analise - Edital.md', 'analise.md'),
        ('Fontes - Edital.md', 'fontes.md')]),
    ('Termo de Referência', 'tr', 'Termo de Referência', [
        ('Estrutura - Termo de Refencia.md', 'estrutura.md'),
        ('Analise - Termo de Referencia.md', 'analise.md'),
        ('Fontes - Termo de Referencia.md', 'fontes.md')]),
    ('Estudo Técnico Preliminar', 'etp', 'Estudo Técnico Preliminar', [
        ('Estrutura - ETP.md', 'estrutura.md'),
        ('Analise - Estudo tecnico Preliminar.md', 'analise.md'),
        ('Fontes - ETP.md', 'fontes.md')]),
    ('Planilha de Custos', 'planilha', 'Planilha de Custos', [
        ('Estrutura - Planilha de Custos.md', 'estrutura.md'),
        ('Analise - Planilha de Custos.md', 'analise.md'),
        ('Fontes - Planilha de Custos.md', 'fontes.md')]),
    ('Pesquisa(Mapa) de Preços', 'pesquisa', 'Pesquisa de Preços', [
        ('Estrutura - Pesquisa de Precos.md', 'estrutura.md'),
        ('Analise - Pesquisa de Precos.md', 'analise.md'),
        ('Fontes - Pesquisa de Precos.md', 'fontes.md')]),
    ('Minuta Contratual', 'minuta', 'Minuta Contratual', [
        ('Estrutura - Minuta Contratual.md', 'estrutura.md'),
        ('Analise - Minuta Contratual.md', 'analise.md'),
        ('Fontes - Minuta Contratual.md', 'fontes.md')]),
]
# A RERI é um processo à parte (só existe dias depois do lançamento do edital): fica fora da cópia,
# e as citações aos seus arquivos viram uma menção sem caminho.
OUT_OF_SCOPE_FOLDER = 'Retificações, Esclarecimentos e Respostas'
OUT_OF_SCOPE = [
    ('Estrutura - RERI.md', 'a Estrutura da RERI (processo à parte)'),
    ('Analise - RERI.md', 'a Análise da RERI (processo à parte)'),
    ('Fontes - RERI.md', 'o mapa da RERI (processo à parte)'),
]
# Escopo da triagem nos mapas copiados: saem as linhas cujo assunto é um ato da RERI, a instrução geral
# "confira também INT-RERI", a legenda e a coluna INT-RERI das matrizes e o INT-RERI das fontes internas.
OMITTED_ROWS = [
    ('edital/fontes.md', 'Prazo e divulgação da resposta'),
    ('edital/fontes.md', 'Resposta depois do prazo de impugnar'),
    ('planilha/fontes.md', 'Resposta que muda a CCT de referência'),
    ('minuta/fontes.md', 'Repactuação logo após a assinatura'),
]
RERI_ID = 'INT-RERI'
# O fim da frase é o ponto seguido de espaço ou fim de linha: "fontes.md" tem ponto no meio.
RERI_SENTENCE = re.compile(r' ?(?:Para tod[ao] \w+, confira também `INT-RERI`|`INT-RERI` vale para todas as seções)'
                           r'.*?\.(?=\s|$)', re.M)
TOP_LEVEL_SEMICOLON = re.compile(r';\s*(?![^()]*\))')

# Trechos que apontam para arquivos que não entram na cópia (anotações, planos, auditorias).
FIXED_REWRITES = [
    (re.compile(r'\s*\(ver `Minhas observacoes\.md` e `02 - Plano do Mapeamento de Fontes\.md`\)'), ''),
    (re.compile(r'Detalhes em `briefing/Auditoria_Estrutura/[^`]+`\.'),
     'Detalhes na auditoria de estrutura do repositório de origem.'),
    (re.compile(r'\bno plano, seção'), 'no plano do mapeamento (repositório de origem), seção'),
    (re.compile(r'`Estrutura - \*\.md` e `Analise - \*\.md`'), '`*/estrutura.md` e `*/analise.md`'),
    (re.compile(r'`Fontes - \{Documento\}\.md`'), '`*/fontes.md`'),
]
# Depois da reescrita, nada disto pode sobrar na cópia.
FORBIDDEN = re.compile(r'Minhas observacoes|0[0-3] - [^`\n|]*\.md|Auditoria_Estrutura|Contexto_Sessao'
                       r'|(?:Estrutura|Analise|Fontes) - [A-Z][^`\n]*\.md|\breri/')
ID_TOKEN = re.compile(r'\b((?:INT|EXT)-[A-Z0-9]+(?:-[A-Z0-9]+)*)\b')
ROW = re.compile(r'^\| ((?:INT|EXT)-[A-Z0-9-]+) \|')


def nfc(text):
    return unicodedata.normalize('NFC', text)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def find(folder, name):
    """Acha um arquivo ou pasta pelo nome em NFC (pastas copiadas de outro sistema podem vir em NFD)."""
    for entry in folder.iterdir():
        if nfc(entry.name) == nfc(name):
            return entry
    raise FileNotFoundError(f'{name} não encontrado em {folder}')


def rewrites():
    pairs = [(f'{folder}/{src}', f'{dst_folder}/{dst}')
             for folder, dst_folder, _, files in DOCUMENTS for src, dst in files]
    pairs += [(src, f'{dst_folder}/{dst}') for _, dst_folder, _, files in DOCUMENTS for src, dst in files]
    pairs.append((CATALOG[0], CATALOG[1]))
    pairs += [(f'`{OUT_OF_SCOPE_FOLDER}/{src}`', note) for src, note in OUT_OF_SCOPE]
    pairs += [(f'`{src}`', note) for src, note in OUT_OF_SCOPE]
    pairs += [(f'{OUT_OF_SCOPE_FOLDER}/{src}', note) for src, note in OUT_OF_SCOPE]
    pairs += [(src, note) for src, note in OUT_OF_SCOPE]
    # Caminho com pasta antes do nome solto, e nomes mais longos antes dos mais curtos.
    return sorted(pairs, key=lambda p: (p[0].count('/') == 0, -len(p[0])))


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def table_line(values):
    return '| ' + ' | '.join(values) + ' |'


def scope(text, target_name):
    """Ajusta um mapa ao escopo da triagem. Devolve o texto, o que mudou e as linhas a omitir não achadas."""
    omit = {point for name, point in OMITTED_ROWS if name == target_name}
    text, sentences = RERI_SENTENCE.subn('', text)
    changes = {'frases_retiradas': sentences, 'colunas_retiradas': 0, 'celulas_limpas': 0, 'linhas_omitidas': []}
    lines, drop = [], None  # drop: posição da coluna INT-RERI na tabela atual
    for line in text.split('\n'):
        if not line.startswith('|'):
            drop = None
            lines.append(line)
            continue
        row = cells(line)
        if row[0] == 'Seção' and RERI_ID in row:
            drop = row.index(RERI_ID)
            changes['colunas_retiradas'] += 1
        if drop is not None:
            lines.append(table_line(row[:drop] + row[drop + 1:]))
        elif row[0] in omit:
            changes['linhas_omitidas'].append(row[0])
        elif len(row) > 1 and RERI_ID in row[1]:
            parts = [part for part in TOP_LEVEL_SEMICOLON.split(row[1]) if not part.startswith(RERI_ID)]
            row[1] = '; '.join(parts) or '—'
            changes['celulas_limpas'] += 1
            lines.append(table_line(row))
        else:
            lines.append(line)
    return '\n'.join(lines), changes, sorted(omit - set(changes['linhas_omitidas']))


def transform(text, source_name, target_name):
    """Devolve a cópia do arquivo, os ajustes de escopo feitos e as linhas a omitir não achadas."""
    text = nfc(text)
    changes, missing = None, []
    if target_name != CATALOG[1]:
        text, changes, missing = scope(text, target_name)
    for pattern, replacement in FIXED_REWRITES:
        text = pattern.sub(replacement, text)
    for old, new in rewrites():
        text = text.replace(old, new)
    header = (f'<!-- Cópia gerada por scripts/sync_estudo.py a partir de {SOURCE_LABEL}/{source_name}. '
              'Não edite aqui: corrija a origem e rode o sync. -->\n\n')
    return header + text, changes, missing


def catalog_rows(text):
    """Linhas de definição do catálogo (tabelas de 7 colunas), com a seção em que aparecem."""
    rows, section = [], ''
    for line in text.splitlines():
        if line.startswith('## ') or line.startswith('### '):
            section = line.lstrip('#').strip()
        if not ROW.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) == 7:
            rows.append(dict(zip(('id', 'nome', 'tipo', 'esfera', 'onde', 'usado_em', 'status'), cells),
                             secao=section))
    return rows


def citable(row):
    if row['id'].startswith('EXT-PEND-') or row['status'] == 'resolvida':
        return 'não (histórico)'
    if re.search(r'não usar', row['nome'], re.I):
        return 'não (citação errada)'
    if row['status'] == 'a conferir':
        return 'só após conferir'
    return 'sim'


def short(text, limit=140):
    text = re.sub(r'[*`]', '', text)
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(' ', 1)[0] + '…'


def build_index(rows):
    lines = ['<!-- Gerado por scripts/sync_estudo.py a partir do catálogo. Não edite aqui. -->', '',
             '# Índice de fontes', '',
             'Resumo do `catalogo-fontes.md` para resolver um ID sem abrir o catálogo inteiro. '
             'O nome está abreviado: antes de citar em minuta, abra a linha completa no catálogo. '
             '"Citável" é derivado do status e do nome: `não (histórico)` para pendências resolvidas, '
             '`não (citação errada)` para fontes marcadas "não usar", `só após conferir` para `a conferir`.', '']
    section = None
    for row in rows:
        if row['secao'] != section:
            section = row['secao']
            lines += ['', f'## {section}', '', '| ID | Nome (resumo) | Esfera | Status | Citável |',
                      '| :-- | :-- | :-- | :-- | :-- |']
        lines.append(f"| {row['id']} | {short(row['nome'])} | {row['esfera']} | {row['status']} | {citable(row)} |")
    return '\n'.join(lines) + '\n'


def build_readme():
    folders = '\n'.join(f'| `{dst}/` | {title} |' for _, dst, title, _ in DOCUMENTS)
    return f'''<!-- Gerado por scripts/sync_estudo.py. Não edite aqui. -->

# Estudo de impugnação (cópia de referência)

Cópia do estudo de `{SOURCE_LABEL}`. Não edite estes arquivos: corrija a origem e rode `scripts/sync_estudo.py`. Os caminhos citados dentro dos arquivos são relativos a esta pasta.

| Pasta | Documento |
| :-- | :-- |
{folders}

Cada pasta tem três arquivos:

- `estrutura.md`: as seções do documento, a finalidade de cada uma e a base legal. A numeração das seções é a chave usada nos mapas (por exemplo, `INT-TR (seção III)`).
- `analise.md`: onde o vício costuma se esconder, como cruzar com outros documentos e o fundamento.
- `fontes.md`: o mapa de fontes. Para cada seção: ponto a verificar, fontes internas (`INT-*` com a seção a abrir), fontes externas (IDs do catálogo), prova a extrair, "gera impugnação se" e "descarta se". Fecha com uma matriz resumo.

Na raiz:

- `catalogo-fontes.md`: fonte de verdade do nome, da esfera, de onde consultar e do status de cada ID.
- `indice-fontes.md`: resumo do catálogo (ID, nome abreviado, esfera, status, se pode ser citado).
- `MANIFEST.json`: hash da origem e da cópia, para saber que versão do estudo foi usada.

Regras de uso:

- Fontes externas são citadas pelo ID. Antes de citar em minuta, confira a linha completa no catálogo.
- `a conferir` nunca aparece como certo. `EXT-PEND-*` e as fontes marcadas "não usar" não são citados.
- Esfera `federal (União)`: o ente do edital pode ter regulamento próprio (`EXT-REG-ENTE`).
- A RERI (retificações, esclarecimentos e respostas) é um processo à parte, depois do lançamento do edital, e fica fora desta cópia. Para a triagem, os mapas foram ajustados: saíram a instrução "confira também `INT-RERI`", a coluna e a legenda `INT-RERI` das matrizes, o `INT-RERI` das fontes internas e as linhas cujo assunto é um ato da RERI. O que saiu de cada mapa está em `MANIFEST.json` (`escopo_triagem`). O catálogo continua inteiro.
'''


def build(source):
    """Monta em memória a cópia ({caminho relativo: bytes}), as fontes do catálogo e os problemas de escopo."""
    outputs, manifest, adjusted, problems = {}, [], {}, []
    catalog_file = find(source, CATALOG[0])
    entries = [(catalog_file, CATALOG[0], CATALOG[1])]
    for folder, dst_folder, _, files in DOCUMENTS:
        origin = find(source, folder)
        entries += [(find(origin, src), f'{folder}/{src}', f'{dst_folder}/{dst}') for src, dst in files]
    for path, source_name, target_name in entries:
        raw = path.read_bytes()
        text, changes, missing = transform(raw.decode('utf-8'), source_name, target_name)
        data = text.encode('utf-8')
        outputs[target_name] = data
        if changes and any(changes.values()):
            adjusted[target_name] = changes
        problems += [f'{target_name}: linha a omitir não encontrada na origem: "{point}" '
                     '(o estudo mudou: revise OMITTED_ROWS)' for point in missing]
        manifest.append({'origem': source_name, 'destino': target_name,
                         'sha256_origem': sha256(raw), 'sha256_destino': sha256(data)})
    rows = catalog_rows(nfc(catalog_file.read_text(encoding='utf-8')))
    outputs['indice-fontes.md'] = build_index(rows).encode('utf-8')
    outputs['LEIA-ME.md'] = build_readme().encode('utf-8')
    study = sha256(''.join(m['sha256_origem'] for m in sorted(manifest, key=lambda m: m['origem'])).encode())
    outputs['MANIFEST.json'] = (json.dumps({
        'gerado_por': 'scripts/sync_estudo.py', 'origem': SOURCE_LABEL, 'estudo_sha256': study,
        'arquivos': manifest,
        'escopo_triagem': {
            'fora_da_copia': f'{OUT_OF_SCOPE_FOLDER}/ (RERI: processo à parte)',
            'ajustes_por_arquivo': adjusted,
        },
        'gerados': [{'destino': n, 'sha256': sha256(outputs[n])} for n in ('indice-fontes.md', 'LEIA-ME.md')],
    }, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return outputs, rows, problems


def validate(outputs, rows, problems=()):
    """Erros impedem gravar a cópia; avisos só são relatados."""
    errors, warnings = list(problems), []
    known = {r['id']: r for r in rows}
    for name, data in sorted(outputs.items()):
        if not name.endswith('.md') or name in ('indice-fontes.md', 'LEIA-ME.md'):
            continue
        text = data.decode('utf-8')
        body = text.split('\n', 2)[-1]  # ignora o cabeçalho que cita a origem
        for match in FORBIDDEN.finditer(body):
            errors.append(f'{name}: referência a arquivo fora da cópia: "{match.group(0)}"')
        if name == CATALOG[1]:
            continue
        if RERI_ID in body:
            errors.append(f'{name}: {RERI_ID} sobrou na cópia (a RERI é processo à parte; revise o ajuste de escopo)')
        for match in ID_TOKEN.finditer(text):
            token = match.group(1)
            if text[match.end():match.end() + 1] in ('*', '-'):
                continue  # curinga como EXT-PEND-*
            if token not in known:
                errors.append(f'{name}: ID sem linha no catálogo: {token}')
            elif citable(known[token]).startswith('não'):
                warnings.append(f'{name}: cita {token}, marcado como {citable(known[token])}')
    return errors, sorted(set(warnings))


def compare(outputs, target):
    """Diferenças entre a cópia esperada e a que está em disco."""
    problems = []
    existing = {p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file()} if target.exists() else set()
    for name in sorted(outputs):
        path = target / name
        if not path.exists():
            problems.append(f'faltando: {name}')
        elif path.read_bytes() != outputs[name]:
            problems.append(f'desatualizado: {name}')
    problems += [f'sobrando: {name}' for name in sorted(existing - set(outputs))]
    return problems


def write(outputs, target):
    target.mkdir(parents=True, exist_ok=True)
    for name, data in outputs.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
    for path in sorted(target.rglob('*'), reverse=True):
        rel = path.relative_to(target).as_posix()
        if path.is_file() and rel not in outputs:
            path.unlink()
        elif path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--origem', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--destino', type=Path, default=DEFAULT_TARGET)
    parser.add_argument('--check', action='store_true', help='só confere, sem gravar')
    args = parser.parse_args(argv)
    try:
        outputs, rows, problems = build(args.origem)
    except (FileNotFoundError, UnicodeDecodeError) as exc:
        print(f'erro: {exc}', file=sys.stderr)
        return 1
    errors, warnings = validate(outputs, rows, problems)
    for warning in warnings:
        print(f'aviso: {warning}')
    if errors:
        for error in errors:
            print(f'erro: {error}', file=sys.stderr)
        print(f'{len(errors)} erro(s) no estudo de origem; nada foi gravado.', file=sys.stderr)
        return 1
    if args.check:
        problems = compare(outputs, args.destino)
        for problem in problems:
            print(problem)
        if problems:
            print('A cópia está desatualizada: rode scripts/sync_estudo.py.', file=sys.stderr)
            return 1
        print(f'OK: {len(outputs)} arquivos conferidos, {len(rows)} fontes no catálogo.')
        return 0
    write(outputs, args.destino)
    print(f'Cópia atualizada em {args.destino}: {len(outputs)} arquivos, {len(rows)} fontes no catálogo.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
