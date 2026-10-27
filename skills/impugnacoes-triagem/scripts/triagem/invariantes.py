"""Invariantes do "validar": o que o estado.json e a pasta precisam cumprir mesmo depois de edição à mão. Na pasta
de formato 2, cada decisão gravada precisa do evento do comando que a registrou, e cada frase passa de novo pelo
formato fixo do comando (formatos.py): uma frase que o comando recusaria não vale no estado."""
import json
import sys

from .arquivos import matches
from .comum import DONE, KIND_LABEL, KINDS, Refusal, id_number, ordered
from .fases import TAMPERED, approval, approved
from .formatos import check_decided, parse_draft, parse_piece, parse_proceed
from .persistencia import STATE_FILE, decode, integrity, located, locked, shape_problems

FINAL_ACTION = {'aprovada': 'aprovar', 'descartada': 'descartar'}


def strict(state):
    """Pasta de formato 2: as frases seguem o formato fixo e cada decisão tem o evento do comando."""
    return type(state.get('formato')) is int and state['formato'] >= 2


def has_event(state, action, detail):
    return any(event['acao'] == action and event['detalhe'] == detail for event in state['eventos'])


def phrase_problems(state, subject, text, check, *args):
    """Frase que falta ou, no formato 2, que o comando recusaria hoje (estado editado à mão, fora da CLI)."""
    if not text:
        return [f'{subject} sem evidência']
    if not strict(state):
        return []
    try:
        check(text, *args)
    except Refusal as exc:
        return [f'{subject} com evidência fora do formato ({exc})']
    return []


def check_final(text, item_id, action):
    found, _ = parse_draft(text, item_id)
    if found != action:
        raise Refusal(f'a frase decide "{found}", não "{action}"')


def check_piece(text, kind, formato):
    found = parse_piece(text)[:2]
    if found != (kind, formato):
        raise Refusal(f'a frase confirma a peça de {KIND_LABEL[found[0]]} em formato {found[1]}, não a gravada')


def decided_event(state, item):
    """Evento "decidir" com o ID do item, a decisão e a frase dele."""
    for event in state['eventos']:
        ids, _, rest = event['detalhe'].partition(' → ')
        if event['acao'] == 'decidir' and item['id'] in ids.split(', ') \
                and rest == f'{item["decisao"]}: "{item["evidencia"]}"':
            return True
    return False


def stray_files(folder, state):
    found, known = [], {item['id']: item for item in state['itens']}
    minutas = folder / 'minutas'
    for path in sorted(minutas.iterdir()) if minutas.is_dir() else []:
        if not path.is_file() or path.name.startswith('.'):
            continue
        item = known.get(path.stem) if path.suffix == '.md' else None
        if item is None:
            found.append(f'arquivo inesperado em minutas/: {path.name}')
        elif item['decisao'] != 'incluir':
            found.append(f'minutas/{path.name}: o item {item["id"]} não está incluído')
        elif item['minuta']['status'] not in ('em_revisao', 'aprovada'):
            found.append(f'minutas/{path.name}: minuta não aberta ou já descartada (abra uma por vez com '
                         '"minuta --acao abrir")')
    return found


def piece_problems(state):
    found = []
    for kind, confirmed in state['peca'].items():
        if not confirmed:
            continue
        label = KIND_LABEL.get(kind, kind)
        found += phrase_problems(state, f'peça de {label} confirmada', confirmed.get('evidencia'), check_piece, kind,
                                 confirmed.get('formato'))
        undecided = [item['id'] for item in ordered(state['itens']) if item['classe'] == kind and (
            item['decisao'] == 'pendente' or (item['decisao'] == 'incluir' and item['minuta']['status'] not in DONE))]
        if undecided:
            found.append(f'peça de {label} confirmada com itens não decididos: {", ".join(undecided)}')
        if confirmed.get('aprovadas') != [approval(item) for item in approved(state, kind)]:
            found.append(f'peça de {label} confirmada com versões que não batem com as minutas aprovadas')
    return found


def final_problems(state, item):
    """Minuta aprovada ou descartada só pela CLI: decisão no histórico, registro da versão e evidência válida."""
    item_id, draft = item['id'], item['minuta']
    status_name, action = draft['status'], FINAL_ACTION[draft['status']]
    found = phrase_problems(state, f'{item_id}: minuta {status_name}', draft['evidencia'], check_final, item_id, action)
    last = draft['historico'][-1] if draft['historico'] else {}
    expected = {'acao': action, 'versao': draft['versao'], 'sha256': draft['sha256'], 'evidencia': draft['evidencia']}
    if any(last.get(key) != value for key, value in expected.items()):
        found.append(f'{item_id}: minuta {status_name} sem a decisão correspondente no histórico '
                     '(ação, versão, sha256 e evidência)')
    registered = f'{item_id} v{draft["versao"]} ({(draft["sha256"] or "")[:12]})'
    if not has_event(state, 'minuta_registrar', registered):
        found.append(f'{item_id}: minuta {status_name} v{draft["versao"]} sem o evento de registro dessa versão')
    decided = f'{item_id} v{draft["versao"]}: "{draft["evidencia"]}"'
    if strict(state) and not has_event(state, f'minuta_{action}', decided):
        found.append(f'{item_id}: minuta {status_name} v{draft["versao"]} sem o evento minuta_{action} dessa versão')
    return found


def decision_problems(state, item):
    """A decisão do item: frase gravada e, no formato 2, o evento "decidir" com ela e a frase no formato."""
    subject = f'{item["id"]}: decisão'
    found = phrase_problems(state, subject, item['evidencia'], check_decided, item['id'], item['decisao'])
    if strict(state) and item['evidencia'] and not decided_event(state, item):
        found.append(f'{subject} sem o evento "decidir" correspondente')
    return found


def item_violations(state, item, seen):
    item_id, draft = item['id'], item['minuta']
    number = id_number(item_id)
    if not number:
        return [f'ID fora do formato IMP-NN/ESC-NN: {item_id!r}']
    found = []
    if number in seen:
        found.append(f'ID repetido: {item_id}' if seen[number] == item_id else
                     f'ID repetido: {item_id} tem o mesmo número de {seen[number]}')
    seen.setdefault(number, item_id)
    if item['classe'] != KINDS[number[0]]:
        found.append(f'{item_id}: classe "{item["classe"]}" incoerente com o ID')
    if item['decisao'] != 'pendente':
        found += decision_problems(state, item)
    if draft['status'] and item['decisao'] != 'incluir':
        found.append(f'{item_id}: minuta {draft["status"]} em item não incluído')
    if draft['status'] in DONE:
        found += final_problems(state, item)
    return found


def changed_drafts(folder, state):
    return [f'{item["id"]}: minuta aprovada alterada ou removida (sha256 não confere)' for item in state['itens']
            if id_number(item['id']) and item['minuta']['status'] == 'aprovada' and not matches(folder, item)]


def proceed_problems(state, proceed):
    faltas = [str(code) for code in proceed['faltas']]
    found = phrase_problems(state, 'decisão de prosseguir', proceed['evidencia'], parse_proceed, faltas)
    if strict(state) and not has_event(state, 'prosseguir', f'sem {", ".join(faltas)}: "{proceed["evidencia"]}"'):
        found.append('decisão de prosseguir sem o evento "prosseguir" correspondente')
    return found


def invariant_problems(state, folder=None):
    """Invariantes do estado.json e, com folder, também dos arquivos da pasta (minutas aprovadas e soltas)."""
    found, seen = [], {}
    for item in state['itens']:
        found += item_violations(state, item, seen)
    review = [item['id'] for item in state['itens'] if item['minuta']['status'] == 'em_revisao']
    if len(review) > 1:
        found.append(f'mais de uma minuta em revisão: {", ".join(review)}')
    proceed = (state['documentos'] or {}).get('prosseguir')
    if proceed is not None:
        found += proceed_problems(state, proceed)
    found += piece_problems(state)
    if folder is not None:
        found += changed_drafts(folder, state) + stray_files(folder, state)
    return found


def checked(state, folder=None):
    """Esquema e invariantes; o validar não pode cair: o que o esquema não previu vira violação, não traceback."""
    found = shape_problems(state)
    if found:
        return found
    try:
        return invariant_problems(state, folder)
    except Exception as exc:
        return [f'{STATE_FILE} fora do formato ({type(exc).__name__}: {exc}): corrija o arquivo']


def read_state(folder):
    """(estado, violações de leitura): estado.json ilegível ou que não é JSON vira violação."""
    try:
        return json.loads(decode((folder / STATE_FILE).read_bytes(), STATE_FILE)), []
    except OSError as exc:
        return None, [f'{STATE_FILE} ilegível: {exc}']
    except Refusal as exc:
        return None, [str(exc)]
    except ValueError as exc:
        return None, [f'{STATE_FILE} não é JSON válido: {exc}']


def violations(folder):
    if not (folder / STATE_FILE).is_file():
        return read_state(folder)[1]  # sem estado.json não há o que travar (e a pasta não ganha .estado.lock)
    with locked(folder, shared=True):
        state, found = read_state(folder)
        check = integrity(folder, state)
        if not found:
            found = checked(state, folder)
    return found + ([TAMPERED[check]] if check in TAMPERED else [])


def cmd_validate(args):
    found = violations(located(args.pasta))
    print(json.dumps({'valido': not found, 'violacoes': found}, ensure_ascii=False, indent=2))
    if found:
        print(f'erro: {len(found)} violação(ões) (invariante ou integridade).', file=sys.stderr)
        return 1
    return 0
