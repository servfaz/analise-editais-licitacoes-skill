"""Respostas do analista em formato fixo: o script confere só o formato e nunca interpreta texto livre.

A comparação ignora maiúsculas, acentos, espaços repetidos, o artigo antes de ID ou de código ("a IMP-01", "o ETP")
e a pontuação final ("." ou "!"). Em listas, vírgula e "e" separam os itens; no "decidir", ";" separa as cláusulas.
IDs: IMP-NN ou ESC-NN ("IMP-1" vale IMP-01). Códigos: EDITAL, TR, ETP, PLANILHA, PESQUISA, MINUTA.

  prosseguir      prossigo sem <códigos>                    (exatamente as faltas registradas)
  decidir         incluo <IDs>; descarto <IDs>; deixo para depois <IDs>   ("os demais" ou "todos": pendentes não citados)
  minuta          aprovo <ID> | descarto <ID> | ajuste <ID>: <o que mudar>   (ID da minuta em revisão)
  reabrir         reabro <IDs>: <motivo>
  peca            confirmo a peça de impugnação|esclarecimento em formato único|por ponto
  aceitar-edicao  aceito a edição do estado: <motivo>
Instrução e motivo têm pelo menos 10 caracteres. Toda recusa traz o formato esperado e um exemplo preenchido com os
dados da triagem, para a skill mostrar ao analista."""
import re
import unicodedata

from .comum import DOC_CODES, KIND_LABEL, Refusal, canonical_id, id_number, join_ids, ordered

MIN_TEXT = 10
ARTICLE = re.compile(r'^(?:a|o|os|as) ')
ID_TOKEN = re.compile(r'(imp|esc)-(\d+)')
PROCEED = re.compile(r'prossigo sem (.+)')
CLAUSE = re.compile(r'(incluo|descarto|deixo para depois) (.+)')
REST = re.compile(r'(?:(?:os|as) )?demais|todos|todas')  # "todos" = os pendentes não citados
DRAFT = re.compile(r'(aprovo|descarto) (.+)|ajuste ([^:]+): ?(.*)')
REOPEN = re.compile(r'reabro ([^:]+): (.*)')
PIECE = re.compile(r'confirmo (?:a )?peca de (impugnacao|esclarecimento) em formato (unico|por ponto)')
ACCEPT = re.compile(r'aceito (?:a )?edicao do estado: (.*)')

DECIDE_VERBS = {'incluo': 'incluir', 'descarto': 'descartar', 'deixo para depois': 'avaliar_depois'}
DRAFT_ACTIONS = {'aprovo': 'aprovar', 'descarto': 'descartar', 'ajuste': 'ajustar'}
PIECE_FORMATS = {'unico': 'único', 'por_ponto': 'por ponto'}

PROCEED_FORMAT = f'"prossigo sem <códigos>", com exatamente os documentos que faltam ({", ".join(DOC_CODES)})'
DECIDE_FORMAT = ('uma ou mais cláusulas separadas por ";": "incluo <IDs>", "descarto <IDs>", "deixo para depois '
                 '<IDs>"; no lugar dos IDs, "os demais" (ou "todos") são os pendentes não citados na frase')
DRAFT_FORMAT = ('"aprovo <ID>", "descarto <ID>" ou "ajuste <ID>: <o que mudar, com pelo menos 10 caracteres>", com o '
                'ID da minuta em revisão')
REOPEN_FORMAT = '"reabro <IDs>: <motivo, com pelo menos 10 caracteres>"'
PIECE_FORMAT = '"confirmo a peça de impugnação|esclarecimento em formato único|por ponto"'
ACCEPT_FORMAT = '"aceito a edição do estado: <motivo, com pelo menos 10 caracteres>"'
ACCEPT_EXAMPLE = 'aceito a edição do estado: corrigi à mão o título do ESC-02'
REASK = 'Peça ao analista que digite a frase nesse formato; não converta uma resposta livre.'


def clean(text):
    """A frase como fica registrada: a do analista, só com os espaços repetidos reduzidos."""
    return ' '.join((text or '').split())


def norm(text):
    text = unicodedata.normalize('NFKD', text or '')
    text = ''.join(c for c in text if not unicodedata.combining(c)).lower()
    text = re.sub(r'\s*([,;:])\s*', r'\1 ', ' '.join(text.split()))
    return re.sub(r'[\s.!,;]+$', '', text).strip()


def quoted(examples):
    return ' ou '.join(f'"{example}"' for example in ([examples] if isinstance(examples, str) else examples))


def refuse(problem, expected, examples):
    raise Refusal(f'{problem}. Formato esperado: {expected}. Exemplo com os dados desta triagem: {quoted(examples)}. '
                  f'{REASK}')


def split_items(text):
    return [ARTICLE.sub('', part) for part in re.split(r'\s*(?:,|\be\b)\s*', text) if part]


def id_list(text):
    """Números (prefixo, n) dos IDs da lista, ou None se algum item não é ID."""
    found = []
    for part in split_items(text):
        match = ID_TOKEN.fullmatch(part)
        if not match:
            return None
        found.append((match[1].upper(), int(match[2])))
    return found or None


def label(number):
    return canonical_id(*number)


# --- exemplos com os dados da triagem ---

def proceed_example(missing):
    return f'prossigo sem {join_ids(list(missing))}'


def decide_example(items):
    pending = [item['id'] for item in ordered(items) if item['decisao'] == 'pendente']
    ids = pending or [item['id'] for item in ordered(items) if not item['minuta']['status']] or ['IMP-01']
    if len(ids) == 1:
        return f'incluo {ids[0]}'
    if len(ids) == 2:
        return f'incluo {ids[0]}; descarto {ids[1]}'
    # "os demais" só vale com pendentes; sem eles o script recusaria o próprio exemplo.
    rest = 'os demais' if pending else join_ids(ids[2:])
    return f'incluo {ids[0]}; descarto {ids[1]}; deixo para depois {rest}'


def draft_example(item_id):
    return f'aprovo {item_id}', f'ajuste {item_id}: cite a página do TR no pedido', f'descarto {item_id}'


def reopen_example(ids):
    return f'reabro {join_ids(list(ids))}: mudei de ideia sobre este ponto'


def piece_example(kinds):
    return f'confirmo a peça de {KIND_LABEL[(list(kinds) or ["impugnacao"])[0]]} em formato único'


# --- conferência ---

def parse_proceed(text, missing):
    example = proceed_example(missing)
    match = PROCEED.fullmatch(norm(text))
    if not match:
        refuse(f'a frase "{clean(text)}" não está no formato do prosseguir', PROCEED_FORMAT, example)
    codes = [part.upper() for part in split_items(match[1])]
    unknown = [code for code in codes if code not in DOC_CODES]
    if unknown:
        refuse(f'"{", ".join(unknown)}" não é código de documento', PROCEED_FORMAT, example)
    extra = sorted({code for code in codes if code not in missing}, key=DOC_CODES.index)
    absent = [code for code in missing if code not in codes]
    if extra or absent:
        details = ([f'cita {join_ids(extra)}, que não falta'] if extra else []) + \
            ([f'não cita {join_ids(absent)}'] if absent else [])
        refuse(f'a frase precisa citar exatamente as faltas registradas ({join_ids(list(missing))}): '
               f'{" e ".join(details)}', PROCEED_FORMAT, example)
    return clean(text)


def decide_clauses(text, example):
    """[(decisão, números dos IDs ou None para "os demais")], na ordem da frase."""
    found = []
    for part in norm(text).split(';'):
        match = CLAUSE.fullmatch(part.strip())
        rest = bool(match) and bool(REST.fullmatch(match[2]))
        numbers = None if rest or not match else id_list(match[2])
        if not (rest or numbers):
            refuse(f'a frase "{clean(text)}" não está no formato do decidir (cláusula "{part.strip()}")',
                   DECIDE_FORMAT, example)
        found.append((DECIDE_VERBS[match[1]], numbers))
    return found


def parse_decide(text, items):
    """(frase, [(decisão, itens)]): cada cláusula com os itens que ela decide; "os demais" vira os pendentes não
    citados. Recusa ID não registrado, ID em duas cláusulas e "os demais" sem pendente."""
    example = decide_example(items)
    clauses = decide_clauses(text, example)
    known = {id_number(item['id']): item for item in items}
    cited = []
    for _, numbers in clauses:
        for number in numbers or []:
            if number not in known:
                refuse(f'{label(number)} não está registrado', DECIDE_FORMAT, example)
            if number in cited:
                refuse(f'{known[number]["id"]} aparece mais de uma vez na frase', DECIDE_FORMAT, example)
            cited.append(number)
    if sum(numbers is None for _, numbers in clauses) > 1:
        refuse('"os demais" aparece em mais de uma cláusula', DECIDE_FORMAT, example)
    rest = [item for item in ordered(items) if item['decisao'] == 'pendente' and id_number(item['id']) not in cited]
    if any(numbers is None for _, numbers in clauses) and not rest:
        refuse('"os demais" não tem a que se referir: não há item pendente fora dos citados', DECIDE_FORMAT, example)
    return clean(text), [(decision, rest if numbers is None else [known[number] for number in numbers])
                         for decision, numbers in clauses]


def check_decided(text, item_id, decision):
    """A frase gravada decide item_id com decision: o ID na cláusula dessa decisão ou, se ele não é citado, "os
    demais" nela."""
    clauses, number = decide_clauses(text, f'incluo {item_id}'), id_number(item_id)
    cited = [found for found, numbers in clauses if numbers and number in numbers]
    rest = [found for found, numbers in clauses if numbers is None]
    if (cited or rest)[:1] != [decision]:
        raise Refusal(f'a frase não põe {item_id} na cláusula de "{decision}"')


def parse_draft(text, item_id):
    """(ação, frase) da decisão sobre a minuta em revisão: aprovar, ajustar ou descartar."""
    example = draft_example(item_id)
    match = DRAFT.fullmatch(norm(text))
    if not match:
        refuse(f'a frase "{clean(text)}" não está no formato da decisão sobre a minuta', DRAFT_FORMAT, example)
    verb = 'ajuste' if match[3] else match[1]
    numbers = id_list(match[3] or match[2])
    if not numbers:
        refuse(f'a frase "{clean(text)}" não está no formato da decisão sobre a minuta', DRAFT_FORMAT, example)
    if len(numbers) != 1:
        refuse('a frase precisa citar um ID só, o da minuta em revisão', DRAFT_FORMAT, example)
    if numbers[0] != id_number(item_id):
        refuse(f'a frase cita {label(numbers[0])}, mas a minuta em revisão é {item_id}', DRAFT_FORMAT, example)
    if verb == 'ajuste' and len(match[4]) < MIN_TEXT:
        refuse('a instrução do ajuste tem menos de 10 caracteres', DRAFT_FORMAT, example)
    return DRAFT_ACTIONS[verb], clean(text)


def parse_reopen(text, items):
    """(itens, frase) do reabrir; recusa ID não registrado e motivo curto."""
    decided = [item['id'] for item in ordered(items) if item['decisao'] != 'pendente' or item['minuta']['status']]
    example = reopen_example(decided[:1] or ['IMP-01'])
    match = REOPEN.fullmatch(norm(text))
    numbers = id_list(match[1]) if match else None
    if not numbers:
        refuse(f'a frase "{clean(text)}" não está no formato do reabrir', REOPEN_FORMAT, example)
    if len(match[2]) < MIN_TEXT:
        refuse('o motivo tem menos de 10 caracteres', REOPEN_FORMAT, example)
    known = {id_number(item['id']): item for item in items}
    unknown = [label(number) for number in numbers if number not in known]
    if unknown:
        refuse(f'{join_ids(unknown)} não está registrado', REOPEN_FORMAT, example)
    return [known[number] for number in dict.fromkeys(numbers)], clean(text)


def parse_piece(text, kinds=()):
    """(tipo, formato, frase) da confirmação da peça; kinds (tipos com minuta aprovada) só entra no exemplo."""
    match = PIECE.fullmatch(norm(text))
    if not match:
        refuse(f'a frase "{clean(text)}" não está no formato da confirmação da peça', PIECE_FORMAT,
               piece_example(kinds))
    return match[1], match[2].replace(' ', '_'), clean(text)


def parse_accept(text):
    match = ACCEPT.fullmatch(norm(text))
    if not match:
        refuse(f'a frase "{clean(text)}" não está no formato do aceite', ACCEPT_FORMAT, ACCEPT_EXAMPLE)
    if len(match[1]) < MIN_TEXT:
        refuse('o motivo tem menos de 10 caracteres', ACCEPT_FORMAT, ACCEPT_EXAMPLE)
    return clean(text)
