"""Base comum: recusa, relógio, normalização de texto, listas, hash, datas, IDs e slug."""
import hashlib
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

# 2: pasta com controle de integridade desde o início e frases do analista no formato fixo (formatos.py), que o
# "validar" confere de novo, com o evento de cada decisão. Pastas com 1 (frase livre, anteriores ao controle)
# continuam válidas: o "validar" só exige que a frase exista.
FORMAT_VERSION = 2
MAX_SLUG = 200

DOC_CODES = ('EDITAL', 'TR', 'ETP', 'PLANILHA', 'PESQUISA', 'MINUTA')
SPHERES = ('federal', 'estadual', 'distrital', 'municipal')
KINDS = {'IMP': 'impugnacao', 'ESC': 'esclarecimento'}
KIND_LABEL = {'impugnacao': 'impugnação', 'esclarecimento': 'esclarecimento'}
DECISIONS = ('incluir', 'descartar', 'avaliar_depois')
DONE = ('aprovada', 'descartada')
ID_RE = re.compile(r'(IMP|ESC)-(\d{2,})', re.ASCII)  # sempre com fullmatch
SLUG_RE = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')


class Refusal(Exception):
    """Transição fora de ordem ou dado inválido; a mensagem diz o que fazer."""


def now():
    """Horário local com fuso; os testes substituem esta função."""
    return datetime.now().astimezone().replace(microsecond=0)


def stamp():
    return now().isoformat()


def today():
    return now().date()


def plain(text):
    text = unicodedata.normalize('NFKD', text or '')
    text = ''.join(c for c in text if not unicodedata.combining(c)).lower()
    return ' '.join(re.sub(r'[^a-z0-9]+', ' ', text).split())


def nfc(text):
    return unicodedata.normalize('NFC', text)


def join_ids(ids):
    return ids[0] if len(ids) == 1 else f'{", ".join(ids[:-1])} e {ids[-1]}'


def split_list(text):
    return [part.strip() for part in (text or '').split(',') if part.strip()]


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def study_hash(manifest):
    try:
        return json.loads(Path(manifest).read_text(encoding='utf-8')).get('estudo_sha256')
    except (OSError, ValueError, AttributeError):
        return None


def parse_date(value):
    text = str(value or '').strip()[:10]
    for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None


def check_year(year):
    if not re.fullmatch(r'\d{4}', year or ''):
        raise Refusal(f'ano inválido: "{year}" (use AAAA).')


def make_slug(orgao, modalidade, numero, ano):
    check_year(ano)
    if not all(plain(part) for part in (orgao, modalidade, numero)):
        raise Refusal('órgão, modalidade e número precisam ter letras ou números.')
    return '-'.join(plain(' '.join((orgao, modalidade, numero, ano))).split())


def canonical_id(prefix, number):
    return f'{prefix}-{int(number):02d}'


def id_number(item_id):
    """(prefixo, número) de um ID válido, ou None. IMP-02 e IMP-002 têm o mesmo número: não podem coexistir."""
    match = ID_RE.fullmatch(str(item_id))
    return (match[1], int(match[2])) if match else None


def id_key(item_id):
    number = id_number(item_id)
    return (0 if number[0] == 'IMP' else 1, number[1], item_id) if number else (2, 0, str(item_id))


def ordered(items):
    return sorted(items, key=lambda item: id_key(item['id']))


def log(state, action, detail):
    state['eventos'].append({'quando': stamp(), 'acao': action, 'detalhe': detail})
