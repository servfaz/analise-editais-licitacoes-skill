"""Montagem da peça: confere o estado da triagem, lê dados-peca.json, o arquivo do representante e as minutas aprovadas
e grava <pasta>/peca/peca-<tipo>[-<ID>].md a partir do modelo .md de assets/ (assets/LEIA-ME.md)."""
import json
import re
from pathlib import Path

from triagem.arquivos import draft_path
from triagem.comum import KIND_LABEL, Refusal, nfc, parse_date, sha256_file, today
from triagem.fases import find_model
from triagem.peca import piece_check
from triagem.persistencia import located, snapshot

from . import pontos
from .modelo import apply_blocks, check_clean, fill, strip_front

DATA_FIELDS = ('destinatario', 'setor_orgao', 'endereco_orgao', 'item_impugnacao', 'objeto')
OPTIONALS = ('atual_prestadora', 'republicacao', 'efeito_suspensivo', 'prova_documental', 'protesto')
REPRESENTATIVE_FIELDS = ('nome', 'cargo', 'designacao')
MODALITIES = {'pe': 'Pregão Eletrônico', 'pp': 'Pregão Presencial', 'cc': 'Concorrência',
              'ce': 'Concorrência Eletrônica'}
MONTHS = ('janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro',
          'novembro', 'dezembro')
ROMAN = ((10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I'))
PROCESS_LINE = re.compile(r'^-\s*Processo administrativo:\s*(.+?)\s*(?:\(.*\))?\s*$', re.M | re.I)


def roman(number):
    out = ''
    for value, letters in ROMAN:
        while number >= value:
            out, number = out + letters, number - value
    return out


def read_json(path, label):
    try:
        data = json.loads(Path(path).read_text(encoding='utf-8'))
    except FileNotFoundError:
        raise Refusal(f'{label} não encontrado em {path}.') from None
    except (OSError, ValueError) as error:
        raise Refusal(f'{label} ilegível ({path}): {error}.') from None
    if not isinstance(data, dict):
        raise Refusal(f'{label} precisa ser um objeto JSON ({path}).')
    return data


def piece_data(folder, kind):
    """dados-peca.json: os campos do órgão e, na impugnação, a escolha explícita de cada opcional (ausência não é
    escolha: o analista decide cada um a cada peça)."""
    data = read_json(folder / 'dados-peca.json', 'dados-peca.json')
    missing = [name for name in DATA_FIELDS if not str(data.get(name) or '').strip()]
    chosen = data.get('opcionais') if isinstance(data.get('opcionais'), dict) else {}
    if kind == 'impugnacao':
        missing += [f'opcionais.{name}' for name in OPTIONALS if not isinstance(chosen.get(name), bool)]
    if missing:
        raise Refusal('dados-peca.json incompleto: falta ' + ', '.join(missing) + '. Os opcionais precisam de '
                      'true ou false, escolhidos pelo analista.')
    return data, {name.upper(): chosen.get(name) is True for name in OPTIONALS}


def representative(path):
    data = read_json(path, 'arquivo do representante')
    missing = [name for name in REPRESENTATIVE_FIELDS if not str(data.get(name) or '').strip()]
    if missing:
        raise Refusal(f'arquivo do representante ({path}) sem: ' + ', '.join(missing) + '.')
    return {f'REPRESENTANTE_{name.upper()}': data[name].strip() for name in REPRESENTATIVE_FIELDS}


def process_number(folder):
    try:
        found = PROCESS_LINE.search((folder / 'documentos.md').read_text(encoding='utf-8'))
    except OSError:
        return ''
    value = found[1].strip() if found else ''
    return '' if value.lower().startswith('não informado') else value


def certame_label(certame, data):
    name = data.get('modalidade_extenso') or MODALITIES.get(certame['modalidade'].strip().lower())
    if not name:
        raise Refusal(f'modalidade "{certame["modalidade"]}" sem nome por extenso conhecido: informe '
                      '"modalidade_extenso" em dados-peca.json (ex.: "Pregão Eletrônico").')
    return f'{name} nº {certame["numero"]}/{certame["ano"]}'


def br_date(value, label):
    date = parse_date(value)
    if not date:
        raise Refusal(f'{label} não registrada no estado da triagem (rode o comando "prazo" do estado.py).')
    return f'{date:%d/%m/%Y}'


def check_on_time(when, limit_value):
    """O texto fixo afirma que a peça é tempestiva: depois da data-limite, a afirmação seria falsa."""
    limit = parse_date(limit_value)
    if limit and when > limit:
        raise Refusal(f'a data da peça ({when:%d/%m/%Y}) é posterior à data-limite do art. 164 ({limit:%d/%m/%Y}), e '
                      'o modelo afirma que a peça é tempestiva. Informe o analista: decidir se ainda vale protocolar é '
                      'dele, e uma peça fora do prazo pede texto que o modelo não tem. Não mude a data da peça nem a '
                      'data-limite para passar.')


def approved_drafts(state, folder, kind, check):
    """As minutas da confirmação, conferidas pelo sha256: o texto montado é o que o analista aprovou."""
    confirmed = state['peca'].get(kind)
    label = KIND_LABEL[kind]
    if not confirmed:
        raise Refusal(f'a peça de {label} não foi confirmada: peça ao analista a frase "confirmo a peça de {label} '
                      'em formato único" (ou "por ponto") e registre com estado.py peca --acao confirmar.')
    if confirmed['aprovadas'] != check['aprovadas_por_tipo'][kind]:
        raise Refusal(f'a confirmação da peça de {label} não corresponde às minutas aprovadas hoje: confirme de novo.')
    drafts = []
    for entry in confirmed['aprovadas']:
        path = draft_path(folder, entry['id'])
        if not path.is_file() or sha256_file(path) != entry['sha256']:
            raise Refusal(f'{entry["id"]}: o arquivo da minuta não é a versão aprovada (v{entry["versao"]}).')
        drafts.append((entry['id'], nfc(path.read_text(encoding='utf-8'))))
    return confirmed['formato'], drafts


def section_of_points(template, flags):
    """Número romano da seção que recebe {{PONTOS}}, contado nos títulos "# " que sobram depois dos blocos."""
    lines = apply_blocks(strip_front(template), flags).split('\n')
    for index, line in enumerate(lines):
        if '{{PONTOS}}' in line:
            return roman(sum(1 for previous in lines[:index] if previous.startswith('# ')))
    raise Refusal('o modelo não tem {{PONTOS}}.')


def points_fields(kind, template, flags, drafts):
    if kind == 'esclarecimento':
        return {'PONTOS': '\n\n'.join(pontos.clarification(text, item_id, n)
                                      for n, (item_id, text) in enumerate(drafts, 1))}
    flags['SUBSIDIARIOS'] = any(pontos.has_subsidiary(text, item_id) for item_id, text in drafts)
    section = section_of_points(template, flags)
    built = [pontos.impugnation(text, item_id, f'{section}.{n}') for n, (item_id, text) in enumerate(drafts, 1)]
    numbers = [row[0] for _, row in built]
    span = f'do item {numbers[0]}' if len(numbers) == 1 else f'dos itens {numbers[0]} a {numbers[-1]}'
    fields = {'PONTOS': '\n\n'.join(body for body, _ in built), 'FAIXA_PONTOS': span}
    if flags['FORMATO_UNICO']:
        fields['QUADRO_RESUMO'] = pontos.quadro([row for _, row in built], [item_id for item_id, _ in drafts])
    return fields


def assemble(pasta, kind, representative_file=None, when=None):
    folder = located(pasta)
    state, integrity = snapshot(folder)
    check = piece_check(state, folder, integrity)
    if not check['pronto']:
        raise Refusal('a peça não pode ser montada; pendências: ' + '; '.join(check['pendencias']) + '.')
    model = find_model(kind)
    if not model or Path(model).suffix != '.md':
        raise Refusal(f'não há modelo .md de {KIND_LABEL[kind]} em assets/ da skill (modelo-{kind}.md).')
    formato, drafts = approved_drafts(state, folder, kind, check)
    data, flags = piece_data(folder, kind)
    rep_path = Path(representative_file) if representative_file else folder.parent.parent / 'representante.json'
    when = when or today()
    check_on_time(when, (state['prazo'] or {}).get('data_limite'))
    process = process_number(folder)
    fields = {'DESTINATARIO': data['destinatario'], 'SETOR_ORGAO': data['setor_orgao'],
              'ENDERECO_ORGAO': data['endereco_orgao'], 'UASG': str(data.get('uasg') or '').strip(),
              'ITEM_IMPUGNACAO': data['item_impugnacao'], 'OBJETO': data['objeto'], 'PROCESSO': process,
              'CERTAME': certame_label(state['certame'], data),
              'DATA_ABERTURA': br_date((state['prazo'] or {}).get('abertura'), 'data de abertura'),
              'DATA_LIMITE': br_date((state['prazo'] or {}).get('data_limite'), 'data-limite'),
              'DATA_PECA': f'{when:%d/%m/%Y}', 'DATA_PECA_EXTENSO': f'{when.day} de {MONTHS[when.month - 1]} de '
                                                                    f'{when.year}'}
    fields.update(representative(rep_path))
    flags.update(PROCESSO=bool(process), UASG=bool(fields['UASG']), FORMATO_UNICO=formato == 'unico')
    template = nfc(Path(model).read_text(encoding='utf-8'))
    groups = [drafts] if formato == 'unico' else [[draft] for draft in drafts]
    out_dir = folder / 'peca'
    out_dir.mkdir(exist_ok=True)
    written = []
    for group in groups:
        text = fill(template, {**fields, **points_fields(kind, template, flags, group)}, flags)
        suffix = '' if formato == 'unico' else f'-{group[0][0]}'
        path = out_dir / f'peca-{kind}{suffix}.md'
        check_clean(text, path.name)
        path.write_text(text, encoding='utf-8')
        written.append(path)
    return written
