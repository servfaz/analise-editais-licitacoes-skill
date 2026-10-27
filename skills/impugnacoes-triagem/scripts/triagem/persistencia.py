"""Gravação e trava: leitura de entrada e JSON, gravação atômica, trava da pasta, forma do estado.json e
integridade dele (.estado.sha256)."""
import hashlib
import json
import os
import re
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

from .arquivos import restore
from .comum import DECISIONS, DOC_CODES, DONE, SLUG_RE, SPHERES, Refusal, log, nfc, sha256_file
from .fases import TAMPERED, status, tampered_help
from .registro import render_log

try:
    import fcntl
except ImportError:  # Windows: sem fcntl, os comandos rodam sem trava
    fcntl = None

STATE_FILE = 'estado.json'
LOG_FILE = 'registro.md'
LOCK_FILE = '.estado.lock'
# sha256 dos bytes do estado.json na última gravação do estado.py: o que diverge foi editado fora dele.
INTEGRITY_FILE = '.estado.sha256'
# Marca no estado.json de que a pasta já tem o controle: sem ela e sem o arquivo, a pasta é anterior a ele.
INTEGRITY_KEY = 'integridade'
# Eventos que só existem em pasta com o controle: sem o arquivo, a pasta não volta a ser "anterior" a ele.
CONTROL_EVENTS = {'integridade', 'aceitar_edicao'}
# Cópia do estado.json da última gravação do estado.py: o aceitar-edicao compara com ela para saber o que mudou.
SAVED_FILE = '.estado.gravado.json'
HASH_RE = re.compile(r'[0-9a-f]{64}')
# O que o "iniciar" aceita numa pasta sem estado.json (texto/ do extrair_texto.py, iniciar interrompido).
REUSABLE = {'minutas', 'texto', LOCK_FILE, INTEGRITY_FILE, SAVED_FILE}

NONE = type(None)
SHAPE = {'certame': dict, 'estudo_sha256': (str, NONE), 'documentos': (dict, NONE), 'prazo': (dict, NONE),
         'itens_registrados_em': (str, NONE), 'itens': list, 'peca': dict, 'eventos': list}
CERTAME_FIELDS = {'slug': str, 'orgao': str, 'modalidade': str, 'numero': str, 'ano': str}
DOCS_FIELDS = {'presentes': list, 'faltas': list}
PROCEED_FIELDS = {'evidencia': str, 'faltas': list}
DEADLINE_FIELDS = {'abertura': object, 'data_limite': object, 'alertas': list}
EVENT_FIELDS = {'quando': str, 'acao': str, 'detalhe': str}
ITEM_FIELDS = {'id': str, 'classe': str, 'titulo': str, 'decisao': str, 'evidencia': (str, NONE), 'minuta': dict}
DRAFT_FIELDS = {'status': (str, NONE), 'versao': int, 'sha256': (str, NONE), 'evidencia': (str, NONE),
                'historico': list}


def decode(data, label):
    try:
        return data.decode('utf-8-sig')
    except UnicodeDecodeError:
        raise Refusal(f'não foi possível ler {label} como UTF-8: salve o arquivo em UTF-8 e rode de novo.')


def read_input(source):
    if str(source) != '-':
        return Path(source).read_bytes()
    stream = getattr(sys.stdin, 'buffer', None)
    # Sem buffer (entrada trocada por texto), o surrogateescape devolve os bytes que não eram UTF-8.
    return stream.read() if stream else sys.stdin.read().encode('utf-8', 'surrogateescape')


def read_json(source, label):
    try:
        data = read_input(source)
    except OSError as exc:
        raise Refusal(f'não foi possível ler {source}: {exc}')
    text = decode(data, label)
    if not text.strip():
        raise Refusal(f'entrada vazia ({label}): se veio de um pipe, o comando anterior falhou '
                      '(veja o erro dele acima); nada foi registrado.')
    try:
        return json.loads(text)
    except ValueError as exc:
        raise Refusal(f'o conteúdo de {label} não é JSON válido: {exc}')


def write_atomic(path, text):
    """Grava os bytes UTF-8 de text, sem tradução de fim de linha: o sha256 do estado.json é o do texto gravado."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f'.{path.name}.', suffix='.tmp')
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(text.encode('utf-8'))
        mask = os.umask(0)
        os.umask(mask)
        os.chmod(tmp, 0o666 & ~mask)  # o mkstemp cria com 0600; o resto da pasta segue o umask
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def wrong_fields(value, fields, prefix):
    """Campos ausentes ou de tipo errado, com o caminho (ex.: documentos.faltas). bool não vale como número."""
    if not isinstance(value, dict):
        return [prefix or 'objeto']
    return [f'{prefix}.{name}' if prefix else name for name, kind in fields.items()
            if name not in value or not isinstance(value[name], kind) or isinstance(value[name], bool)]


def docs_problems(docs):
    if docs is None:
        return []
    found = wrong_fields(docs, DOCS_FIELDS, 'documentos')
    if found:
        return found
    if not all(code in DOC_CODES for code in docs['presentes'] + docs['faltas']):
        found.append('documentos.presentes/faltas (código desconhecido)')
    proceed = docs.get('prosseguir')
    if proceed is not None:
        found += wrong_fields(proceed, PROCEED_FIELDS, 'documentos.prosseguir')
    return found


def item_problems(item):
    found = wrong_fields(item, ITEM_FIELDS, '')
    if found:
        return found
    draft = item['minuta']
    found = wrong_fields(draft, DRAFT_FIELDS, 'minuta')
    if item['decisao'] not in ('pendente',) + DECISIONS:
        found.append(f'decisao ("{item["decisao"]}")')
    if found:
        return found
    if draft['status'] not in (None, 'em_revisao') + DONE:
        found.append(f'minuta.status ("{draft["status"]}")')
    if draft['versao'] < 0:
        found.append('minuta.versao')
    if not all(isinstance(entry, dict) for entry in draft['historico']):
        found.append('minuta.historico')
    return found


def shape_problems(state):
    """Esquema do estado.json: o que os comandos usam precisa existir com o tipo certo (edição à mão não derruba)."""
    if not isinstance(state, dict):
        return [f'{STATE_FILE} não é um objeto JSON']
    found = [f'campo ausente ou inválido em {STATE_FILE}: {key}'
             for key, kind in SHAPE.items() if not isinstance(state.get(key), kind)]
    if found:
        return found
    bad = wrong_fields(state['certame'], CERTAME_FIELDS, 'certame') + docs_problems(state['documentos'])
    if state['certame'].get('esfera') not in (None,) + SPHERES:
        bad.append('certame.esfera')
    if state['prazo'] is not None:
        bad += wrong_fields(state['prazo'], DEADLINE_FIELDS, 'prazo')
    bad += [f'peca.{kind}' for kind, value in state['peca'].items() if not isinstance(value, (dict, NONE))]
    bad += [f'eventos[{n}]' for n, event in enumerate(state['eventos'], 1) if wrong_fields(event, EVENT_FIELDS, '')]
    found = [f'campo ausente ou inválido em {STATE_FILE}: {name}' for name in bad]
    for n, item in enumerate(state['itens'], 1):
        problems = item_problems(item)
        if problems:
            found.append(f'item {n} fora do formato em {STATE_FILE}: {", ".join(problems)}')
    return found


def twin(folder, name):
    """Entrada de folder com o mesmo nome em NFC (pastas copiadas de outro sistema podem vir em NFD)."""
    try:
        return next((entry for entry in folder.iterdir() if nfc(entry.name) == nfc(name)), None)
    except OSError:
        return None


def located(path):
    """Caminho real no disco, aceitando partes digitadas em NFC quando a pasta está em NFD (ou o contrário)."""
    path = Path(os.path.abspath(path))
    found = Path(path.anchor)
    for part in path.parts[1:]:
        candidate = found / part
        if not candidate.exists() and found.is_dir():
            candidate = twin(found, part) or candidate
        found = candidate
    return found.resolve()


def leftovers(folder):
    """O que impede o "iniciar" de aproveitar uma pasta que já existe sem estado.json."""
    return sorted(entry.name for entry in folder.iterdir() if entry.name not in REUSABLE) if folder.is_dir() else []


def state_file(folder):
    path = folder / STATE_FILE
    if path.is_file():
        return path
    if folder.is_dir() and SLUG_RE.fullmatch(folder.name) and not leftovers(folder):
        raise Refusal(f'{folder} existe, mas não tem {STATE_FILE}: rode "iniciar --raiz {folder.parent} --slug '
                      f'{folder.name}" com os dados do certame (ele aproveita a pasta).')
    raise Refusal(f'{folder} não tem {STATE_FILE}: crie a pasta do edital com "iniciar".')


def load(folder):
    path = state_file(folder)
    text = decode(path.read_bytes(), str(path))
    try:
        state = json.loads(text)
    except ValueError as exc:
        raise Refusal(f'{path} não é JSON válido ({exc}): rode "validar" e corrija antes de seguir.')
    problems = shape_problems(state)
    if problems:
        raise Refusal('; '.join(problems) + ': rode "validar" e corrija antes de seguir.')
    return state


@contextmanager
def locked(folder, shared=False):
    """Trava da pasta. Exclusiva para gravar: quem grava espera o outro terminar, em vez de sobrescrever o que ele
    gravou. Compartilhada para ler estado.json e .estado.sha256 juntos, sem pegar uma gravação pela metade; se a
    pasta não deixa criar a trava, a leitura segue sem ela."""
    try:
        handle = open(folder / LOCK_FILE, 'a', encoding='utf-8')
    except OSError:
        if not shared:
            raise
        handle = None
    try:
        if handle and fcntl:
            fcntl.flock(handle, fcntl.LOCK_SH if shared else fcntl.LOCK_EX)
        yield
    finally:
        if handle:
            handle.close()


def recorded_hashes(folder):
    """sha256 aceitos pelo .estado.sha256 (None se ele não existe; vazio se ilegível). Durante uma gravação ele traz
    também o hash anterior, para que uma gravação interrompida não pareça edição à mão."""
    try:
        text = (folder / INTEGRITY_FILE).read_text(encoding='utf-8')
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError):
        return set()
    return {line.split()[0] for line in text.splitlines() if line.split() and HASH_RE.fullmatch(line.split()[0])}


def controlled(state):
    """O estado é de pasta que já tem o controle de integridade: a marca, o formato 2 ou um evento do controle. Tirar
    a marca e o .estado.sha256 não faz a pasta voltar a ser "anterior" ao controle."""
    if not isinstance(state, dict):
        return False
    version, events = state.get('formato'), state.get('eventos')
    return bool(state.get(INTEGRITY_KEY)) or (type(version) is int and version >= 2) or (
        isinstance(events, list) and any(isinstance(event, dict) and event.get('acao') in CONTROL_EVENTS
                                         for event in events))


def integrity(folder, state):
    """'ok'; 'antiga' (pasta anterior ao controle: a próxima gravação cria o arquivo); 'removido' (o estado é de pasta
    com o controle, mas o arquivo falta); ou 'alterado' (o sha256 do estado.json não confere)."""
    accepted = recorded_hashes(folder)
    if accepted is None:
        return 'removido' if controlled(state) else 'antiga'
    try:
        return 'ok' if sha256_file(folder / STATE_FILE) in accepted else 'alterado'
    except OSError:
        return 'alterado'


def snapshot(folder):
    """Estado e situação da integridade, lidos juntos sob a trava compartilhada (status e peça a verificar)."""
    state_file(folder)
    with locked(folder, shared=True):
        state = load(folder)
        return state, integrity(folder, state)


def require_intact(folder, state):
    """Recusa gravar sobre um estado.json alterado fora do estado.py; numa pasta antiga, anota que o controle começa."""
    check = integrity(folder, state)
    if check in TAMPERED:
        raise Refusal(f'{TAMPERED[check]}: nada foi gravado. {tampered_help(folder)}')
    if check == 'antiga':
        log(state, 'integridade', f'{INTEGRITY_FILE} criado: a pasta é anterior ao controle de integridade do '
                                  f'{STATE_FILE}, e uma edição à mão anterior a esta gravação não seria detectada')


def save(folder, state):
    """Grava estado.json, a cópia dele (.estado.gravado.json), .estado.sha256 e registro.md; só dentro da trava
    exclusiva da pasta. Enquanto o estado.json é trocado, o .estado.sha256 aceita o hash do arquivo que está no disco
    e o do novo; depois, só o do novo."""
    state[INTEGRITY_KEY] = INTEGRITY_FILE
    path, text = folder / STATE_FILE, json.dumps(state, ensure_ascii=False, indent=2) + '\n'
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    current = [sha256_file(path)] if path.is_file() else []
    write_atomic(folder / INTEGRITY_FILE, ''.join(f'{value}  {STATE_FILE}\n' for value in [digest] + current))
    write_atomic(path, text)
    write_atomic(folder / SAVED_FILE, text)
    write_atomic(folder / INTEGRITY_FILE, f'{digest}  {STATE_FILE}\n')
    write_atomic(folder / LOG_FILE, render_log(state))


def saved_state(folder):
    """O estado da última gravação do estado.py (.estado.gravado.json), ou None se a cópia falta ou não se lê."""
    try:
        return json.loads(decode((folder / SAVED_FILE).read_bytes(), SAVED_FILE))
    except (OSError, ValueError, Refusal):
        return None


def changing(change, intact=True):
    """Carrega o estado sob a trava da pasta, aplica a mudança, grava e devolve o status. Com intact (todos os
    comandos, menos o aceitar-edicao), recusa o estado.json alterado fora do estado.py antes de mexer em arquivo."""
    def handler(args):
        folder = located(args.pasta)
        state_file(folder)
        with locked(folder):
            state = load(folder)
            if intact:
                require_intact(folder, state)
                restore(folder, state)
            message = change(state, folder, args)
            save(folder, state)
        return {'mensagem': message, **status(state, folder)}
    return handler
