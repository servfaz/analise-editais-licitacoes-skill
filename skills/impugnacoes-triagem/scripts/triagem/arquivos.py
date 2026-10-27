"""Arquivos das minutas: caminho, conferência do sha256, arquivamento no histórico e restauração."""
import os
import re

from .comum import log, sha256_file


def draft_path(folder, item_id):
    return folder / 'minutas' / f'{item_id}.md'


def matches(folder, item):
    path = draft_path(folder, item['id'])
    return path.is_file() and sha256_file(path) == item['minuta']['sha256']


def archive(folder, item_id, version):
    """Move minutas/<ID>.md para o histórico sem sobrescrever uma versão já arquivada."""
    source = draft_path(folder, item_id)
    if not source.is_file():
        return None
    history = folder / 'minutas' / 'historico'
    target, n = history / f'{item_id}.v{version}.md', 2
    while target.exists():
        target, n = history / f'{item_id}.v{version}-{n}.md', n + 1
    history.mkdir(parents=True, exist_ok=True)
    os.replace(source, target)
    return target.relative_to(folder).as_posix()


def archived_copies(folder, item_id, version):
    history = folder / 'minutas' / 'historico'
    name = re.compile(rf'{re.escape(item_id)}\.v{version}(?:-\d+)?\.md')
    return sorted(path for path in history.iterdir() if name.fullmatch(path.name)) if history.is_dir() else []


def restore(folder, state):
    """Desfaz um arquivamento interrompido (o arquivo foi para o histórico, mas o estado não chegou a ser gravado):
    a minuta registrada sumiu de minutas/ e a cópia com o mesmo sha256 está no histórico."""
    for item in state['itens']:
        draft, path = item['minuta'], draft_path(folder, item['id'])
        if draft['status'] not in ('em_revisao', 'aprovada') or not draft['sha256'] or path.exists():
            continue
        for copy in archived_copies(folder, item['id'], draft['versao']):
            if sha256_file(copy) == draft['sha256']:
                os.replace(copy, path)
                log(state, 'minuta_restaurada', f'{item["id"]} v{draft["versao"]}: {copy.name} voltou para minutas/')
                break
