import asyncio
import importlib.util
import io
import sys
import types
import unittest
from pathlib import Path

from docx import Document

PACOTE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACOTE / 'build'))

import montar_acao

ACTION = PACOTE / 'functions' / 'gerar_minuta_impugnacao_action.py'


class UploadFile:
    def __init__(self, file, filename, headers=None):
        self.file = file
        self.filename = filename
        self.headers = headers or {}


def load_action(upload_handler):
    """Carrega a Function compilada sem precisar de uma instalação local do Open WebUI."""
    fastapi = types.ModuleType('fastapi')
    fastapi.UploadFile = UploadFile
    starlette = types.ModuleType('starlette')
    datastructures = types.ModuleType('starlette.datastructures')
    datastructures.Headers = dict
    routers = types.ModuleType('open_webui.routers')
    files = types.ModuleType('open_webui.routers.files')
    files.upload_file_handler = upload_handler
    open_webui = types.ModuleType('open_webui')
    open_webui.routers = routers
    routers.files = files
    modules = {'fastapi': fastapi, 'starlette': starlette, 'starlette.datastructures': datastructures,
               'open_webui': open_webui, 'open_webui.routers': routers, 'open_webui.routers.files': files}
    saved = {name: sys.modules.get(name) for name in modules}
    sys.modules.update(modules)
    try:
        spec = importlib.util.spec_from_file_location('gerar_minuta_action_test', ACTION)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for name, prior in saved.items():
            if prior is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = prior


MARKDOWN = '''## IMPUGNAÇÃO AO EDITAL

**SERVFAZ SERVIÇOS LTDA.**, inscrita no CNPJ nº [Inserir CNPJ], com sede em [Inserir Endereço Completo],
representada por [Inserir Nome], RG [Inserir RG], CPF [Inserir CPF].

### I. DO PEDIDO

1. O conhecimento da impugnação;
2. O acolhimento do pedido;
'''


class ActionTests(unittest.TestCase):
    def test_generated_action_matches_source_and_declares_target_release(self):
        self.assertEqual(ACTION.read_text(encoding='utf-8'), montar_acao.montar())
        source = ACTION.read_text(encoding='utf-8')
        self.assertIn("OPENWEBUI_COMPATIBILITY = '0.12.3'", source)
        self.assertIn("'type': 'files'", source)
        self.assertIn("'type': 'confirmation'", source)

    def test_requires_one_explicit_approved_block(self):
        module = load_action(lambda **kwargs: None)
        self.assertEqual(module.extrair_minuta(f'{module.INICIO}\ntexto\n{module.FIM}'), 'texto')
        with self.assertRaises(module.Refusal):
            module.extrair_minuta('texto sem bloco')
        with self.assertRaises(module.Refusal):
            module.extrair_minuta(f'{module.INICIO}a{module.FIM}\n{module.INICIO}b{module.FIM}')

    def test_confirmed_action_exports_exact_approved_text_as_native_file(self):
        received = {}

        async def upload_handler(request, file, metadata, process, process_in_background, user):
            received.update(request=request, filename=file.filename, data=file.file.read(), metadata=metadata,
                            process=process, user=user)
            return {'id': 'arquivo-123'}

        module = load_action(upload_handler)
        events = []

        async def emit(event):
            events.append(event)

        async def confirm(event):
            self.assertEqual(event['type'], 'confirmation')
            self.assertIn('Hash da versão:', event['data']['message'])
            return True

        content = f'{module.INICIO}\n{MARKDOWN}\n{module.FIM}'
        body = {'id': 'mensagem-1', 'messages': [{'id': 'mensagem-1', 'role': 'assistant', 'content': content}]}
        action = module.Action()
        action.valves.CNPJ = '00.000.000/0001-00'
        action.valves.ENDERECO = 'Rua Exemplo, 1'
        asyncio.run(action.action(body, __user__={'id': 'usuario-1', 'email': 'a@b.test', 'name': 'Analista'},
                                  __request__=object(), __event_emitter__=emit, __event_call__=confirm))

        self.assertFalse(received['process'])
        self.assertEqual(received['user'].id, 'usuario-1')
        self.assertEqual(received['metadata']['source'], 'exportar-minuta-servfaz')
        doc = Document(io.BytesIO(received['data']))
        paragraphs = [paragraph.text for paragraph in doc.paragraphs]
        self.assertTrue(any('00.000.000/0001-00' in paragraph and 'Rua Exemplo' in paragraph
                            for paragraph in paragraphs))
        self.assertTrue(any('[Inserir Nome]' in paragraph and '[Inserir CPF]' in paragraph
                            for paragraph in paragraphs))
        file_event = next(event for event in events if event['type'] == 'files')
        self.assertEqual(file_event['data']['files'][0]['id'], 'arquivo-123')
        self.assertIn('/api/v1/files/arquivo-123/content', file_event['data']['files'][0]['url'])

    def test_cancelled_action_never_uploads_a_file(self):
        uploaded = []

        async def upload_handler(**kwargs):
            uploaded.append(kwargs)
            return {'id': 'erro'}

        module = load_action(upload_handler)
        events = []

        async def emit(event):
            events.append(event)

        async def cancel(event):
            return False

        content = f'{module.INICIO}\n{MARKDOWN}\n{module.FIM}'
        body = {'id': 'mensagem-1', 'messages': [{'id': 'mensagem-1', 'role': 'assistant', 'content': content}]}
        asyncio.run(module.Action().action(body, __user__={'id': 'usuario-1'}, __request__=object(),
                                            __event_emitter__=emit, __event_call__=cancel))
        self.assertEqual(uploaded, [])
        self.assertEqual(events[-1]['data']['type'], 'warning')


if __name__ == '__main__':
    unittest.main()
