"""Render do registro.md, regenerado a partir do estado.json a cada gravação."""
from .comum import KIND_LABEL, ordered, parse_date
from .fases import phase

LAST_EVENTS = 20
DRAFT_LABEL = {'em_revisao': 'em revisão', 'aprovada': 'aprovada', 'descartada': 'descartada'}


def cell(text, limit=120):
    text = ' '.join(str(text).split()).replace('|', '\\|')
    return text if len(text) <= limit else text[:limit - 1] + '…'


def draft_label(draft):
    if not draft['status']:
        return '—'
    text = f'{DRAFT_LABEL[draft["status"]]} v{draft["versao"]}'
    return text + ' (não registrada)' if draft['status'] == 'em_revisao' and not draft['sha256'] else text


def evidence_label(item):
    parts = []
    if item['evidencia']:
        parts.append(f'decisão: "{item["evidencia"]}"')
    if item['minuta']['evidencia']:
        parts.append(f'minuta: "{item["minuta"]["evidencia"]}"')
    return ' / '.join(parts) or '—'


def render_log(state):
    certame, docs, prazo = state['certame'], state['documentos'], state['prazo']
    sphere = f' (esfera {certame["esfera"]})' if certame.get('esfera') else ''
    if docs is None:
        docs_line = 'portão não registrado'
    else:
        docs_line = (f'presentes {", ".join(docs["presentes"]) or "nenhum"}; '
                     f'faltas {", ".join(docs["faltas"]) or "nenhuma"}'
                     + ('; prosseguir autorizado' if docs.get('prosseguir') else ''))
    if prazo is None:
        prazo_line = 'não calculado'
    else:
        limit = parse_date(prazo.get('data_limite'))
        prazo_line = f'data-limite {limit:%d/%m/%Y}' if limit else f'data-limite {prazo.get("data_limite")}'
        prazo_line += f' (abertura {prazo.get("abertura")})'
    lines = ['<!-- Gerado por scripts/estado.py a partir de estado.json. Não edite: use o estado.py. -->', '',
             f'# Registro da triagem {certame["slug"]}', '',
             f'- Certame: {certame["orgao"]}, {certame["modalidade"]} {certame["numero"]}/{certame["ano"]}{sphere}',
             f'- Fase: {phase(state)}',
             f'- Documentos: {docs_line}',
             f'- Prazo: {prazo_line}',
             f'- Estudo: {state["estudo_sha256"] or "sem hash registrado"}',
             '', '## Itens', '']
    if state['itens']:
        lines += ['| ID | Classe | Título | Decisão | Minuta | Evidência |', '| :-- | :-- | :-- | :-- | :-- | :-- |']
        lines += [f'| {item["id"]} | {KIND_LABEL.get(item["classe"], item["classe"])} | {cell(item["titulo"])} | '
                  f'{item["decisao"].replace("_", " ")} | {draft_label(item["minuta"])} | '
                  f'{cell(evidence_label(item))} |' for item in ordered(state['itens'])]
    else:
        lines.append('Nenhum item registrado.')
    lines += ['', '## Últimos eventos', '']
    lines += [f'- {event["quando"]} {event["acao"]}: {cell(event["detalhe"], 200)}'
              for event in state['eventos'][-LAST_EVENTS:]]
    return '\n'.join(lines) + '\n'
