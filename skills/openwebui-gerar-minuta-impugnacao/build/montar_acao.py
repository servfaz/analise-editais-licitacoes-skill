#!/usr/bin/env python3
"""Monta functions/gerar_minuta_impugnacao_action.py para o Open WebUI 0.12.3.

A Action é o caminho de produção: o analista clica na resposta aprovada, confirma
a exportação e recebe o .docx como arquivo nativo do chat. O arquivo gerado é
autônomo porque a instalação de Functions não compartilha os assets de Skills.

Uso:
  montar_acao.py [--saida functions/gerar_minuta_impugnacao_action.py]
"""
import argparse
import base64
from pathlib import Path

from montar_tool import PACOTE, nucleo, timbre_leve


SAIDA = PACOTE / 'functions' / 'gerar_minuta_impugnacao_action.py'

CABECALHO = '''"""
title: Exportar Minuta de Impugnacao Servfaz
description: Após confirmação humana, gera o .docx timbrado a partir da minuta aprovada na resposta selecionada.
author: Servfaz
version: 2.0.0
requirements: python-docx==1.1.2
"""
# Arquivo gerado por build/montar_acao.py. Não edite à mão.
# Compatibilidade alvo: Open WebUI 0.12.3.
import asyncio
import base64
import hashlib
import io
import re
import unicodedata
from types import SimpleNamespace
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field
from starlette.datastructures import Headers

from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from open_webui.routers.files import upload_file_handler

'''

ADAPTADOR = r'''

OPENWEBUI_COMPATIBILITY = '0.12.3'
DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
INICIO = '<!-- minuta-servfaz:inicio -->'
FIM = '<!-- minuta-servfaz:fim -->'
_BLOCO = re.compile(re.escape(INICIO) + r'\s*(.*?)\s*' + re.escape(FIM), re.S)


def nome_seguro(nome):
    """Nome de arquivo só com letras, números, ponto, hífen e sublinhado; sempre termina em .docx."""
    base = unicodedata.normalize('NFKD', nome or '').encode('ascii', 'ignore').decode()
    base = re.sub(r'[^\w.-]+', '-', re.sub(r'\.docx$', '', base.strip(), flags=re.I)).strip('.-_')
    return (base or 'minuta-impugnacao') + '.docx'


def extrair_minuta(content):
    """Lê um único bloco explícito de minuta na resposta que recebeu a Action."""
    matches = _BLOCO.findall(content or '')
    if len(matches) != 1:
        raise Refusal('a resposta selecionada precisa conter exatamente um bloco entre '
                      f'{INICIO} e {FIM}. Revise a minuta antes de exportar.')
    markdown = matches[0].strip()
    if not markdown:
        raise Refusal('o bloco da minuta aprovada está vazio.')
    return markdown


def mensagem_alvo(body):
    target_id = body.get('id')
    for message in body.get('messages') or []:
        if message.get('id') == target_id:
            if message.get('role') != 'assistant':
                raise Refusal('a Action só exporta uma resposta do assistente.')
            return message.get('content') or ''
    raise Refusal('não foi possível localizar a resposta selecionada para exportação.')


def ator(user):
    if not isinstance(user, dict) or not user.get('id'):
        raise Refusal('não foi possível identificar o usuário que solicitou a exportação.')
    # upload_file_handler só necessita destes atributos na criação do arquivo. Não registramos dados do signatário.
    return SimpleNamespace(id=str(user['id']), email=str(user.get('email') or ''),
                           name=str(user.get('name') or user.get('username') or ''),
                           role=str(user.get('role') or 'user'))


async def avisar(emitter, kind, content):
    if emitter:
        await emitter({'type': 'notification', 'data': {'type': kind, 'content': content}})


class Action:
    class Valves(BaseModel):
        CNPJ: str = Field('', description='CNPJ da Servfaz; preenche apenas [Inserir CNPJ].')
        ENDERECO: str = Field('', description='Endereço da Servfaz; preenche [Inserir Endereço] quando existir.')
        priority: int = 10

    def __init__(self):
        self.valves = self.Valves()

    async def action(self, body: dict, __user__=None, __request__=None, __event_emitter__=None,
                     __event_call__=None):
        """Gera um DOCX da resposta aprovada, após confirmação explícita do analista.

        A resposta deve conter somente um bloco da forma:
        <!-- minuta-servfaz:inicio -->
        ... Markdown aprovado ...
        <!-- minuta-servfaz:fim -->
        """
        try:
            markdown = extrair_minuta(mensagem_alvo(body))
            check_clean(markdown, 'a minuta selecionada')
        except Refusal as exc:
            await avisar(__event_emitter__, 'error', str(exc))
            return

        digest = hashlib.sha256(markdown.encode('utf-8')).hexdigest()
        if not __event_call__:
            await avisar(__event_emitter__, 'error', 'a confirmação no navegador é obrigatória para exportar a minuta.')
            return
        confirmation = await __event_call__({
            'type': 'confirmation',
            'data': {
                'title': 'Confirmar geração da minuta',
                'message': ('Será gerado um .docx do texto exatamente como aparece no bloco aprovado. '
                            f'Hash da versão: {digest[:12]}. A Action não assina nem protocola a peça.')
            }
        })
        if not confirmation or (isinstance(confirmation, dict) and confirmation.get('error')):
            await avisar(__event_emitter__, 'warning', 'Geração cancelada ou confirmação indisponível; nenhum arquivo foi criado.')
            return

        try:
            dados = {'cnpj': self.valves.CNPJ, 'endereco': self.valves.ENDERECO}
            doc, pending = render(markdown, io.BytesIO(base64.b64decode(_TIMBRE_B64)), dados,
                                  label='a minuta selecionada')
            buffer = io.BytesIO()
            doc.save(buffer)
            contents = buffer.getvalue()
            filename = nome_seguro(f'minuta-impugnacao-{digest[:12]}')
            upload = UploadFile(file=io.BytesIO(contents), filename=filename,
                                headers=Headers({'content-type': DOCX}))
            result = await upload_file_handler(__request__, file=upload,
                                               metadata={'source': 'exportar-minuta-servfaz',
                                                         'markdown_sha256': digest},
                                               process=False, process_in_background=False, user=ator(__user__))
            item = result.model_dump() if hasattr(result, 'model_dump') else dict(result)
            file_id = item['id']
        except (OSError, Refusal, ValueError, KeyError) as exc:
            await avisar(__event_emitter__, 'error', f'Não foi possível gerar a minuta: {exc}')
            return
        except Exception:
            await avisar(__event_emitter__, 'error', 'Não foi possível guardar o .docx no Open WebUI. Consulte o log do servidor.')
            raise

        await __event_emitter__({
            'type': 'files',
            'data': {'files': [{
                'type': 'file',
                'id': file_id,
                'name': filename,
                'url': f'/api/v1/files/{file_id}/content',
                'meta': {'name': filename, 'content_type': DOCX, 'size': len(contents),
                         'markdown_sha256': digest}
            }]}
        })
        detail = (f'{len(pending)} campo(s) ficaram destacados em amarelo no Word.' if pending
                  else 'Nenhum campo de preenchimento ficou pendente.')
        await avisar(__event_emitter__, 'success', f'Minuta gerada: {filename}. {detail} Revise, assine e protocole fora do sistema.')
'''


def montar():
    codificado = base64.b64encode(timbre_leve()).decode()
    linhas = '\n'.join(codificado[index:index + 120] for index in range(0, len(codificado), 120))
    return (CABECALHO + '\n' + nucleo() + ADAPTADOR + '\n\n# Timbre da Servfaz, em base64.\n'
            '_TIMBRE_B64 = """\n' + linhas + '\n"""\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--saida', type=Path, default=SAIDA, help='destino da Function')
    args = parser.parse_args(argv)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(montar(), encoding='utf-8')
    print(f'{args.saida} ({args.saida.stat().st_size // 1024} KB)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
