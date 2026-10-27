"""Comando "aceitar-edicao": registra a decisão do analista de manter um estado.json alterado fora do estado.py.

A frase segue o formato fixo de formatos.py ("aceito a edição do estado: <motivo>"). A alteração só pode mexer em
dados descritivos (título de item, dados do certame): decisões, eventos e controle mudam só pelos comandos, com a
frase do analista. O que mudou sai da comparação com a cópia da última gravação (.estado.gravado.json)."""
import re

from .comum import Refusal, log
from .fases import TAMPERED
from .formatos import parse_accept
from .invariantes import checked
from .persistencia import SAVED_FILE, STATE_FILE, integrity, saved_state

# Campos que o aceite cobre: o resto tem comando próprio.
DESCRIPTIVE = re.compile(r'certame\.(?:orgao|modalidade|numero|ano|esfera)|itens\[[^\]]+\]\.titulo')
RESTORE = ('o estado.json precisa voltar a ser idêntico ao da última gravação (desfaça a alteração ou use uma cópia '
           'do analista) ou a triagem recomeça numa pasta nova')


def changed_items(old, new):
    if not (isinstance(old, list) and isinstance(new, list)):
        return ['itens']
    old_by = {item.get('id'): item for item in old if isinstance(item, dict)}
    new_by = {item.get('id'): item for item in new if isinstance(item, dict)}
    if list(old_by) != list(new_by) or len(old_by) != len(old) or len(new_by) != len(new):
        return ['itens (acrescentados, removidos, reordenados ou renomeados)']
    return [f'itens[{item_id}].{field}' for item_id, item in old_by.items()
            for field in sorted(set(item) | set(new_by[item_id])) if item.get(field) != new_by[item_id].get(field)]


def changed_fields(old, new):
    """Campos do estado.json que mudaram desde a última gravação, com o caminho ("certame.orgao",
    "itens[IMP-01].titulo")."""
    found = []
    for key in sorted(set(old) | set(new)):
        before, after = old.get(key), new.get(key)
        if key == 'itens':
            found += changed_items(before, after)
        elif key == 'certame' and isinstance(before, dict) and isinstance(after, dict):
            found += [f'certame.{name}' for name in sorted(set(before) | set(after))
                      if before.get(name) != after.get(name)]
        elif before != after:
            found.append(key)
    return found


def cmd_accept_edit(state, folder, args):
    check = integrity(folder, state)
    if check == 'ok':
        raise Refusal(f'não há alteração a aceitar: o {STATE_FILE} confere com a última gravação do estado.py.')
    if check not in TAMPERED:
        raise Refusal('não há alteração a aceitar: a pasta é anterior ao controle de integridade, que será criado na '
                      'próxima gravação.')
    evidence = parse_accept(args.evidencia)
    found = checked(state)
    if found:
        raise Refusal(f'a alteração deixou o {STATE_FILE} com violações que o aceite não corrige: {"; ".join(found)}. '
                      f'Mostre-as ao analista: {RESTORE}.')
    saved = saved_state(folder)
    if not isinstance(saved, dict):
        raise Refusal(f'não há cópia legível da última gravação ({SAVED_FILE}) para saber o que mudou, e o aceite '
                      f'não cobre uma alteração que não se pode conferir: {RESTORE}.')
    changed = changed_fields(saved, state)
    blocked = [name for name in changed if not DESCRIPTIVE.fullmatch(name)]
    if blocked:
        raise Refusal(f'a alteração mexe em {", ".join(blocked)}: decisões, eventos e controle mudam só pelos comandos '
                      'do estado.py (prosseguir, decidir, minuta, reabrir, peca), com a frase do analista; o aceite '
                      f'cobre só o título de item e os dados do certame. Mostre isso ao analista: {RESTORE}.')
    what = ', '.join(changed) or 'nenhum campo; só o .estado.sha256 faltava'
    log(state, 'aceitar_edicao', f'{STATE_FILE} alterado fora do estado.py ({what}), mantido pelo analista: '
                                 f'"{evidence}"')
    return ('Alteração do estado.json aceita e registrada com a frase do analista; o .estado.sha256 foi regravado e os '
            'comandos voltam a gravar. Rode "validar".')
