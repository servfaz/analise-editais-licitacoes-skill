"""Portões e fase derivada: fila de minutas, minuta em revisão, aprovadas, próxima ação, alertas e status, com
os caminhos fixos do estudo e dos modelos da peça."""
import json
import re
from pathlib import Path

from .arquivos import draft_path, matches
from .comum import DONE, KIND_LABEL, KINDS, Refusal, ordered, parse_date, study_hash, today
from .formatos import ACCEPT_EXAMPLE, decide_example, draft_example, proceed_example, quoted

SKILL_DIR = Path(__file__).resolve().parents[2]
# Fixos, sem opção na linha de comando: o estudo vale só na cópia da skill e o modelo da peça só em assets/ dela.
# Os testes trocam os dois com mock.patch neste módulo.
MANIFEST = SKILL_DIR / 'references' / 'estudo' / 'MANIFEST.json'
ASSETS = SKILL_DIR / 'assets'
MODEL_SKIP = {'bak', 'orig', 'tmp', 'temp', 'swp', 'swo', 'old', 'part', 'crdownload'}
# Situações do .estado.sha256 (persistencia.integrity) que bloqueiam a gravação.
TAMPERED = {
    'alterado': 'estado.json foi alterado fora do estado.py (o sha256 dele não confere com o de .estado.sha256, '
                'escrito na última gravação do estado.py)',
    'removido': 'estado.json foi alterado fora do estado.py ou .estado.sha256 foi apagado (o estado registra o '
                'controle de integridade, mas o arquivo falta)',
}
OLD_FOLDER = ('esta pasta é anterior ao controle de integridade do estado.json: o .estado.sha256 será criado na '
              'próxima gravação; avise o analista de que uma edição à mão anterior a ela não seria detectada (este '
              'alerta se repete até a próxima gravação).')


def current_study():
    return study_hash(MANIFEST)


def find_model(kind):
    """modelo-<tipo>.<ext> em assets/: nome exato, uma extensão só e arquivo não vazio. Cópia de editor ("~", ".bak",
    ".swp"), arquivo oculto ou com outro sufixo ("modelo-impugnacao.md~") não é o modelo revisado."""
    name = re.compile(rf'modelo-{re.escape(kind)}\.([A-Za-z0-9]+)')
    try:
        entries = sorted(Path(ASSETS).iterdir())
    except OSError:
        return None
    for path in entries:
        match = name.fullmatch(path.name)
        if match and match[1].lower() not in MODEL_SKIP and path.is_file() and path.stat().st_size > 0:
            return str(path)
    return None


def tampered_help(folder):
    return ('Não edite o estado.json para destravar: os comandos que gravam ficam recusados. Mostre a alteração ao '
            'analista (compare o estado.json com o registro.md, que reflete a última gravação do estado.py, e rode '
            '"validar"). Se ele decidir manter a alteração, peça a frase no formato "aceito a edição do estado: '
            f'<motivo>" (por exemplo: "{ACCEPT_EXAMPLE}") e registre com "aceitar-edicao --pasta {folder} '
            '--evidencia \'<frase>\'". Se não, o '
            'estado.json precisa voltar a ser idêntico ao da última gravação: desfaça a alteração, se você sabe '
            'exatamente qual foi, ou use uma cópia que o analista tenha.')


def gate_open(state):
    docs = state['documentos']
    return docs is not None and (not docs['faltas'] or bool(docs.get('prosseguir')))


def require_gate(state):
    if not gate_open(state):
        raise Refusal('o portão documental não foi resolvido: registre "documentos" (e "prosseguir", se houver '
                      'faltas, com a frase do analista) antes disso.')


def queue(state):
    return [item for item in ordered(state['itens'])
            if item['decisao'] == 'incluir' and item['minuta']['status'] not in DONE]


def in_review(state):
    return [item for item in state['itens'] if item['minuta']['status'] == 'em_revisao']


def approved(state, kind=None):
    return [item for item in ordered(state['itens'])
            if item['minuta']['status'] == 'aprovada' and kind in (None, item['classe'])]


def discarded(state):
    """Itens incluídos cuja minuta foi descartada: não entram na peça nem contam como peça no relatório."""
    return [item['id'] for item in ordered(state['itens'])
            if item['decisao'] == 'incluir' and item['minuta']['status'] == 'descartada']


def approval(item):
    return {'id': item['id'], 'versao': item['minuta']['versao'], 'sha256': item['minuta']['sha256']}


def ids_with(state, decision):
    return [item['id'] for item in ordered(state['itens']) if item['decisao'] == decision]


def phase(state):
    if not gate_open(state):
        return 'documentos'
    if state['itens_registrados_em'] is None:
        return 'levantamento'
    if ids_with(state, 'pendente'):
        return 'selecao'
    if queue(state):
        return 'minutas'
    if any(approved(state, kind) and not state['peca'].get(kind) for kind in KINDS.values()):
        return 'peca_final'
    return 'concluido'


def deadline_note(prazo):
    limit = parse_date((prazo or {}).get('data_limite'))
    if limit is None:
        return 'o prazo de impugnação está correndo (prazo não registrado: calcule e registre com "prazo")'
    if today() > limit:
        return f'o prazo de impugnação venceu em {limit:%d/%m/%Y}, segundo o prazo registrado'
    return f'o prazo de impugnação está correndo (data-limite {limit:%d/%m/%Y})'


def piece_action(state):
    """Peça final: verificar antes de perguntar; sem modelo, informar e parar; com modelo, formato por tipo."""
    kinds = [kind for kind in KINDS.values() if approved(state, kind) and not state['peca'].get(kind)]
    without = [KIND_LABEL[kind] for kind in kinds if not find_model(kind)]
    ready = [KIND_LABEL[kind] for kind in kinds if find_model(kind)]
    parts = ['Todas as minutas foram decididas. Rode "peca --acao verificar" antes de qualquer pergunta ao analista '
             'e resolva as pendências que o comando listar.']
    later = ids_with(state, 'avaliar_depois')
    if later:
        parts.append(f'Liste ao analista os itens para avaliar depois ({", ".join(later)}) e lembre que '
                     f'{deadline_note(state["prazo"])}; se ele decidir algum agora, registre com "decidir".')
    if without:
        parts.append(f'Não há modelo da peça de {" nem da de ".join(without)} em assets/: informe ao analista que as '
                     'minutas aprovadas estão em minutas/ (ID e versão de cada uma) e que a peça final só sai quando '
                     'o modelo existir, e pare. Não pergunte o formato nem monte a peça por outro meio.')
    if ready:
        parts.append(f'Há modelo para a peça de {" e para a de ".join(ready)}: pergunte o formato (único ou por '
                     'ponto) separadamente para cada tipo, a cada uso, liste as versões aprovadas e peça a '
                     'confirmação no formato "confirmo a peça de <impugnação|esclarecimento> em formato <único|por '
                     f'ponto>" (por exemplo: "confirmo a peça de {ready[0]} em formato único"); registre com "peca '
                     '--acao confirmar". Depois, monte a peça com "montar_peca.py montar" (SKILL.md, Fase 5).')
    return ' '.join(parts + ['Não assine, não protocole, não envie.'])


def next_action(state, folder, current):
    docs, review = state['documentos'], in_review(state)
    if current == 'documentos':
        if docs is None:
            return ('Verifique pelo conteúdo Edital, TR, ETP, Planilha, Pesquisa de preços e Minuta e registre '
                    'com "documentos". Não faça levantamento nem minuta antes disso.')
        return (f'Apresente o relatório do portão (faltam {", ".join(docs["faltas"])}, com o efeito de cada falta) e '
                'pergunte se o analista envia os documentos ou prossegue. Espere a resposta e registre com '
                '"documentos" (documentos novos) ou "prosseguir" (frase no formato fixo, por exemplo: '
                f'"{proceed_example(docs["faltas"])}"). Não faça levantamento.')
    if current == 'levantamento':
        deadline = ' calcule o prazo' if state['prazo'] is None else ''
        return (f'Faça o levantamento, um documento por vez,{deadline} e registre os itens com "itens". '
                'Não gere minuta nem peça.')
    if current == 'selecao':
        note = f' A minuta {review[0]["id"]} continua em revisão, aguardando decisão.' if review else ''
        return (f'Peça ao analista a decisão sobre os itens pendentes ({", ".join(ids_with(state, "pendente"))}) '
                'numa frase de formato fixo: cláusulas "incluo <IDs>", "descarto <IDs>" e "deixo para depois <IDs>" '
                f'separadas por ";", com "os demais" para os pendentes não citados (por exemplo: '
                f'"{decide_example(state["itens"])}"). Registre a frase com "decidir"; o item não citado continua '
                'pendente. Não abra minuta nova.' + note)
    if current == 'minutas':
        if not review:
            return (f'Abra a próxima minuta ({queue(state)[0]["id"]}) com "minuta --acao abrir" e escreva só ela. '
                    'Não escreva outras minutas nem a peça.')
        item = review[0]
        draft, path = item['minuta'], draft_path(folder, item['id'])
        if not draft['sha256']:
            return (f'Escreva a minuta {item["id"]} v{draft["versao"]} em {path} e registre com "minuta --id '
                    f'{item["id"]} --acao registrar". Não abra outra minuta.')
        if not matches(folder, item):
            return (f'A minuta {item["id"]} mudou depois do registro: registre de novo e apresente a versão atual '
                    'antes de pedir a decisão.')
        return (f'Apresente a minuta {item["id"]} v{draft["versao"]} com o checklist de auditoria e peça a decisão '
                f'numa destas frases: {quoted(draft_example(item["id"]))}. Registre-a com "minuta --evidencia". '
                'Não abra outra minuta nem gere a peça.')
    if current == 'peca_final':
        return piece_action(state)
    text = 'Nada pendente nesta triagem.' if approved(state) else 'Nenhuma minuta aprovada: não há peça a gerar.'
    later = ids_with(state, 'avaliar_depois')
    if later:
        text += f' Para avaliar depois: {", ".join(later)} (retome com "decidir").'
    confirmed = [KIND_LABEL[kind] for kind in KINDS.values() if state['peca'].get(kind)]
    if confirmed:
        text += (f' Peça confirmada ({", ".join(confirmed)}): monte com "montar_peca.py montar", apresente o texto '
                 'montado ao analista e, com o "ok" dele, converta com "montar_peca.py converter" (SKILL.md, Fase 5).')
    return text + ' Não assine, não protocole, não envie.'


def deadline_alerts(prazo):
    if not prazo:
        return []
    found = [f'prazo: {a if isinstance(a, str) else json.dumps(a, ensure_ascii=False)}'
             for a in prazo.get('alertas') or []]
    limit, current = parse_date(prazo.get('data_limite')), today()
    if limit and current > limit:
        found.append(f'prazo de impugnação vencido em {limit:%d/%m/%Y}, segundo o prazo registrado: avise o analista.')
    elif limit == current:
        found.append('hoje é o último dia do prazo de impugnação, segundo o prazo registrado.')
    return found


def integrity_alerts(integrity):
    if integrity in TAMPERED:
        return [f'{TAMPERED[integrity]}: mostre a alteração ao analista antes de seguir; os comandos que gravam '
                'ficam recusados até ele decidir (veja proxima_acao).']
    return [OLD_FOLDER] if integrity == 'antiga' else []


def alerts(state, folder):
    found, current = [], current_study()
    if state['estudo_sha256'] is None:
        found.append('o hash do estudo não foi registrado no início (MANIFEST.json ausente): não dá para saber que '
                     'versão do estudo foi usada.')
    elif current is None:
        found.append(f'MANIFEST.json do estudo não encontrado em {MANIFEST}: não dá para conferir se o estudo mudou.')
    elif current != state['estudo_sha256']:
        found.append('o estudo mudou desde o início da triagem: confira se os itens levantados continuam válidos.')
    for item in approved(state):
        if not matches(folder, item):
            found.append(f'minuta {item["id"]} alterada ou removida depois de aprovada: restaure a versão aprovada '
                         'ou use "reabrir".')
    for item in in_review(state):
        if item['minuta']['sha256'] and not matches(folder, item):
            found.append(f'minuta {item["id"]} alterada depois do registro: registre de novo antes de pedir decisão.')
    return found + deadline_alerts(state['prazo'])


def review_info(folder, item):
    draft = item['minuta']
    return {'id': item['id'], 'versao': draft['versao'], 'arquivo': str(draft_path(folder, item['id'])),
            'registrada': bool(draft['sha256']), 'sha256': draft['sha256']}


def status(state, folder, integrity='ok'):
    """Status da triagem; integrity é a situação do .estado.sha256 (persistencia.integrity) lida com o estado."""
    current, review = phase(state), in_review(state)
    action = next_action(state, folder, current)
    if integrity in TAMPERED:
        action = f'O {TAMPERED[integrity]}. {tampered_help(folder)}'
    return {
        'pasta': str(folder), 'certame': state['certame'], 'fase': current,
        'proxima_acao': action,
        'documentos': state['documentos'], 'prazo': state['prazo'],
        'itens': {'total': len(state['itens']), 'pendentes': ids_with(state, 'pendente'),
                  'incluidos': ids_with(state, 'incluir'), 'descartados': ids_with(state, 'descartar'),
                  'avaliar_depois': ids_with(state, 'avaliar_depois')},
        'fila_minutas': [item['id'] for item in queue(state)],
        'minuta_em_revisao': review_info(folder, review[0]) if review else None,
        'aprovadas': [approval(item) for item in approved(state)],
        'minutas_descartadas': discarded(state),
        'peca': state['peca'], 'estudo_sha256': state['estudo_sha256'],
        'alertas': integrity_alerts(integrity) + alerts(state, folder),
    }
