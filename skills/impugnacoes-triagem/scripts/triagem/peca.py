"""Peça final: verificação, confirmação (tipo e formato vêm da frase do analista, no formato fixo de formatos.py) e
invalidação da confirmação. A peça sai pelo montar_peca.py, que só monta a peça do tipo confirmado aqui."""
from pathlib import Path

from .arquivos import matches
from .comum import KIND_LABEL, KINDS, Refusal, log, stamp
from .fases import TAMPERED, approval, approved, find_model, gate_open, ids_with, queue
from .formatos import PIECE_FORMATS, parse_piece
from .persistencia import changing, located, snapshot


def invalidate_piece(state, kind, reason):
    if state['peca'].get(kind):
        state['peca'][kind] = None
        log(state, 'peca_invalidada', f'confirmação da peça de {KIND_LABEL[kind]} desfeita: {reason}')


def piece_check(state, folder, integrity='ok'):
    """Pendências, aprovadas por tipo e modelos; integrity é a situação do .estado.sha256 lida com o estado."""
    pending = [TAMPERED[integrity]] if integrity in TAMPERED else []
    if not gate_open(state):
        pending.append('portão documental não resolvido')
    elif state['itens_registrados_em'] is None:
        pending.append('levantamento não registrado')
    pending += [f'{item_id}: decisão pendente' for item_id in ids_with(state, 'pendente')]
    for item in queue(state):
        draft = item['minuta']
        opened = draft['status'] == 'em_revisao'
        pending.append(f'{item["id"]}: minuta em revisão (v{draft["versao"]})' if opened
                       else f'{item["id"]}: minuta ainda não aberta')
    pending += [f'{item["id"]}: minuta alterada ou removida depois de aprovada'
                for item in approved(state) if not matches(folder, item)]
    by_kind = {kind: [approval(item) for item in approved(state, kind)] for kind in KINDS.values()}
    if not any(by_kind.values()):
        pending.append('nenhuma minuta aprovada')
    return {'pronto': not pending, 'pendencias': pending, 'aprovadas_por_tipo': by_kind,
            'modelos': {kind: find_model(kind) for kind in KINDS.values()}, 'confirmadas': state['peca']}


def confirm_piece(state, folder, args):
    if not args.evidencia:
        raise Refusal('informe --evidencia com a frase do analista que confirma a peça.')
    check = piece_check(state, folder)
    if not check['pronto']:
        raise Refusal('a peça ainda não pode ser confirmada; pendências: ' + '; '.join(check['pendencias']) + '.')
    kinds = [kind for kind, approvals in check['aprovadas_por_tipo'].items() if approvals]
    if not any(check['modelos'][kind] for kind in kinds):
        raise no_model(kinds)
    kind, formato, evidence = parse_piece(args.evidencia, kinds)
    label, approvals = KIND_LABEL[kind], check['aprovadas_por_tipo'][kind]
    if not approvals:
        raise Refusal(f'não há minuta de {label} aprovada: não há peça de {label} a confirmar.')
    model = check['modelos'][kind]
    if not model:
        raise no_model([kind])
    state['peca'][kind] = {'formato': formato, 'evidencia': evidence, 'quando': stamp(), 'modelo': Path(model).name,
                           'aprovadas': approvals}
    ids = ', '.join(entry['id'] for entry in approvals)
    log(state, 'peca_confirmar', f'{label} ({formato}) com {ids}: "{evidence}"')
    return (f'Peça de {label} confirmada (formato {PIECE_FORMATS[formato]}) com {ids}. Monte-a com "montar_peca.py '
            'montar"; não assine, não protocole, não envie.')


def no_model(kinds):
    labels = ' nem de '.join(KIND_LABEL[kind] for kind in kinds)
    pattern = ', '.join(f'modelo-{kind}.*' for kind in kinds)
    return Refusal(f'não há modelo de {labels} em assets/ da skill ({pattern}): a peça final só sai quando o modelo '
                   'existir. Informe o analista e pare aqui; não gere a peça por outro meio nem crie modelo.')


def cmd_piece(args):
    if args.acao == 'confirmar':
        return changing(confirm_piece)(args)
    folder = located(args.pasta)
    state, integrity = snapshot(folder)
    return piece_check(state, folder, integrity)
