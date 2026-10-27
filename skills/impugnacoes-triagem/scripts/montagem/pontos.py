"""Minuta aprovada → ponto da peça: lê o cabeçalho e as seções da minuta e escreve o tópico em Markdown corrido, sem
subtítulos internos, sem numeração de parágrafo e sem marcadores [ID · status] (references/minuta-por-ponto.md)."""
import re
from itertools import groupby

from triagem.comum import Refusal, plain

MARKER = re.compile(r'\s*\[(?:EXT|INT|NOVA)-[^\]\n]*\]')
MARKER_ID = re.compile(r'\[((?:EXT|INT|NOVA)-[A-Z0-9-]+)')
PARA_NUMBER = re.compile(r'^\d+\.\s+')
SPAN = r'\d+(?:\s*(?:a|e|–|-)\s*\d+)?'
PAGES = re.compile(rf'\b(p[áa]ginas?|p\.) PDF ({SPAN})(?:,\s*p[áa]ginas? impressas?\s*({SPAN})|\s*\(impr\.\s*({SPAN})\))?')
HEADER_FIELD = re.compile(r'^-\s+([^:]+):\s*(.*)$')
TITLE = re.compile(r'^#\s+(?:IMP|ESC)-\d+\s+[—–-]\s+(.+)$')
QUADRO_FIELDS = ('Cláusula', 'Vício (resumo)', 'Pedido (resumo)')
IMP_BODY = ('dos fatos', 'normas e jurisprudencia', 'aplicacao ao caso', 'resposta ao contraponto da administracao')
ESC_ART164 = {'EXT-LEI14133-ART164'}


def parse(text, item_id):
    """Título, campos do cabeçalho e seções (chave: título da seção ## ou ### normalizado)."""
    title, fields, sections, current = None, {}, {}, None
    for line in text.split('\n'):
        heading = re.match(r'^(#{1,3})\s+(.*)$', line)
        if heading and len(heading[1]) == 1:
            match = TITLE.match(line)
            title = match[1].strip() if match else None
            continue
        if heading:
            current = plain(heading[2])
            sections[current] = []
            continue
        if current is None:
            field = HEADER_FIELD.match(line)
            if field:
                fields[field[1].strip()] = field[2].strip()
        else:
            sections[current].append(line)
    if not title:
        raise Refusal(f'minuta {item_id}: a primeira linha não segue "# {item_id} — <título>".')
    return title, fields, {key: '\n'.join(lines).strip() for key, lines in sections.items()}


def page(match):
    return f'{match[1]} {match[3] or match[4] or match[2]}'


def clean(text):
    """Sem marcador de fonte e com a página como a Administração a vê: "página PDF 23" vira "página 23"; com a
    impressa ao lado ("página PDF 52, página impressa 18"), fica a impressa ("página 18")."""
    return PAGES.sub(page, MARKER.sub('', text)).strip()


def blocks(text):
    """Parágrafos e citações de uma seção. Citação é linha com ">"; uma linha ">" vazia separa citações."""
    found = []
    for chunk in re.split(r'\n[ \t]*\n', text or ''):
        lines = [line.strip() for line in chunk.split('\n') if line.strip()]
        for quoting, group in groupby(lines, key=lambda line: line.startswith('>')):
            group = list(group)
            if not quoting:
                paragraphs = []
                for line in group:  # "1. ", "2. " em linhas seguidas são parágrafos distintos
                    if PARA_NUMBER.match(line) or not paragraphs:
                        paragraphs.append([PARA_NUMBER.sub('', line)])
                    else:
                        paragraphs[-1].append(line)
                found += [('p', ' '.join(lines)) for lines in paragraphs]
                continue
            part = []
            for line in group + ['>']:
                if line[1:].strip():
                    part.append(line[1:].strip())
                elif part:
                    found.append(('quote', ' '.join(part)))
                    part = []
    return [(kind, clean(raw), set(MARKER_ID.findall(raw))) for kind, raw in found if clean(raw)]


def as_markdown(found):
    return [f'> {text}' if kind == 'quote' else text for kind, text, _ in found]


def lower_first(text):
    """Inicial minúscula para a alínea ("A retificação" → "a retificação"), salvo sigla ("TR", "CCT")."""
    first = text.split()[0] if text.split() else ''
    return text if len(first) > 1 and first.isupper() else text[:1].lower() + text[1:]


def none_left(found):
    return not found or plain(found[0][1]).startswith('nao ha')


def requests(sections):
    """Pedido principal e subsidiário como alíneas, cada uma terminada em ";" (o conversor fecha a última com ".")."""
    main = [text for kind, text, _ in blocks(sections.get('pedido principal')) if kind == 'p']
    if not main:
        raise Refusal('a minuta não tem "Pedido principal".')
    extra = blocks(sections.get('pedido subsidiario'))
    items = [lower_first(text) for text in main]
    if not none_left(extra):
        paragraphs = [text for kind, text, _ in extra if kind == 'p']
        items += ['subsidiariamente, ' + lower_first(paragraphs[0])] + [lower_first(t) for t in paragraphs[1:]]
    return [f'1. {re.sub(r"[.;:]+$", "", item)};' for item in items]


def has_subsidiary(text, item_id):
    """A minuta traz pedido subsidiário (a seção existe e não começa por "Não há")."""
    return not none_left(blocks(parse(text, item_id)[2].get('pedido subsidiario')))


def impugnation(text, item_id, number):
    """Tópico <número> (ex.: "III.2") da peça de impugnação e a linha do quadro resumo."""
    title, fields, sections = parse(text, item_id)
    if 'dos fatos' not in sections:
        raise Refusal(f'minuta {item_id}: falta a seção "Dos fatos".')
    lines = [f'**{number} – {title.upper()}**']
    for key in IMP_BODY:
        lines += as_markdown(blocks(sections.get(key)))
    try:
        lines += ['Desta forma, **IMPUGNA-SE** o edital e seus anexos, requerendo-se:', '\n'.join(requests(sections))]
    except Refusal as error:
        raise Refusal(f'minuta {item_id}: {error}') from None
    wording = blocks(sections.get('redacao retificadora sugerida'))
    if not none_left(wording):
        lines += ['Sugere-se a seguinte redação:'] + as_markdown(wording)
    row = [number] + [fields.get(name, '') for name in QUADRO_FIELDS]
    return '\n\n'.join(lines), row


def clarification(text, item_id, number):
    """Quesito <número> da peça de esclarecimento. Sai o parágrafo de "Do fundamento" que só cita o art. 164: a
    tempestividade da peça já o cita."""
    title, _, sections = parse(text, item_id)
    questions = [text for kind, text, _ in blocks(sections.get('da pergunta')) if kind == 'p']
    if not questions:
        raise Refusal(f'minuta {item_id}: falta a seção "Da pergunta".')
    basis = [block for block in blocks(sections.get('do fundamento')) if block[2] != ESC_ART164]
    lines = [f'**QUESITO {number} – {title}**'] + as_markdown(blocks(sections.get('da duvida')))
    lines += as_markdown(basis) + ['Indaga-se:', '\n'.join(f'1. {q}' for q in questions)]
    return '\n\n'.join(lines)


def quadro(rows, item_ids):
    missing = [f'{item_id} ({", ".join(n for n, v in zip(QUADRO_FIELDS, row[1:]) if not v)})'
               for item_id, row in zip(item_ids, rows) if not all(row[1:])]
    if missing:
        raise Refusal('o quadro resumo precisa dos campos "Cláusula", "Vício (resumo)" e "Pedido (resumo)" no '
                      'cabeçalho da minuta; faltam em: ' + '; '.join(missing) + '.')
    cell = lambda value: clean(value).replace('|', '/')  # noqa: E731
    lines = ['| # | Cláusula impugnada | Vício | Pedido principal |', '| :-- | :-- | :-- | :-- |']
    return '\n'.join(lines + ['| ' + ' | '.join(cell(v) for v in row) + ' |' for row in rows])
