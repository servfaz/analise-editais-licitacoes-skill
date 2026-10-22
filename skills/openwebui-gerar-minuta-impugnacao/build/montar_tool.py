#!/usr/bin/env python3
"""Monta tools/gerar_minuta_impugnacao.py, o arquivo único que se cola no editor de Tools do Open WebUI. Só para quem
mantém o pacote; a Tool em uso não roda este script. Python 3.10+.

A Tool junta, num só arquivo: o núcleo de conversão de skills/gerar-minuta-impugnacao/scripts/gerar_minuta.py (o trecho
entre os marcadores "núcleo", copiado sem alteração), o timbre da Servfaz embutido em base64 (o Open WebUI não tem
pasta de assets) e o adaptador da Tool. Refaça a montagem sempre que o gerar_minuta.py ou o timbre mudarem; o teste do
pacote falha se a Tool estiver defasada.

O timbre original é incorporado sem alteração para que a Action e a Tool tenham saída reprodutível em qualquer
ambiente de montagem.

Uso:
  montar_tool.py [--saida tools/gerar_minuta_impugnacao.py]
"""
import argparse
import base64
import re
import sys
from pathlib import Path

PACOTE = Path(__file__).resolve().parents[1]
SKILL = PACOTE.parent / 'gerar-minuta-impugnacao'
FONTE = SKILL / 'scripts' / 'gerar_minuta.py'
TIMBRE = SKILL / 'assets' / 'timbre-servfaz.docx'
SAIDA = PACOTE / 'tools' / 'gerar_minuta_impugnacao.py'
NUCLEO = re.compile(r'^# === núcleo.*?\n(.*?)^# === fim do núcleo ===\n', re.S | re.M)

CABECALHO = '''"""
title: Gerar Minuta de Impugnacao (legado)
description: Conversor legado de Markdown para .docx timbrado da Servfaz; prefira a Action de exportação aprovada.
author: Servfaz
version: 2.0.0
requirements: python-docx==1.1.2
"""
# Arquivo gerado por build/montar_tool.py; não edite à mão. O núcleo de conversão vem de
# skills/gerar-minuta-impugnacao/scripts/gerar_minuta.py e o timbre fica embutido no fim do arquivo.
import base64
import io
import re
import unicodedata
from datetime import date
from html import escape
from typing import Optional

from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

'''

ADAPTADOR = '''

DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
PAGINA = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
:root {{ color-scheme: light dark; }}
body {{ font-family: system-ui, sans-serif; margin: 0; padding: 4px; }}
.cartao {{ border: 1px solid #8884; border-radius: 8px; padding: 12px 14px; max-width: 520px; }}
.nome {{ color: #888; font-size: 13px; margin: 2px 0 10px; }}
a.baixar {{ display: inline-block; padding: 8px 14px; background: #1f6feb; color: #fff; border-radius: 6px;
  text-decoration: none; font-weight: 600; }}
.pendencias {{ margin-top: 12px; font-size: 13px; }}
.pendencias mark {{ background: #ffeb3b; color: #000; padding: 0 2px; }}
</style></head><body><div class="cartao">
<div><strong>Minuta gerada</strong></div>
<div class="nome">{nome} · {tamanho} KB</div>
<a class="baixar" id="baixar" href="#" download="{nome}">Baixar .docx</a>
{pendencias}
</div>
<script>
const b64 = "{dados}";
const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
document.getElementById("baixar").href = URL.createObjectURL(new Blob([bytes], {{ type: "{mime}" }}));
function reportHeight() {{
  parent.postMessage({{ type: 'iframe:height', height: document.documentElement.scrollHeight }}, '*');
}}
window.addEventListener('load', reportHeight);
new ResizeObserver(reportHeight).observe(document.body);
</script></body></html>"""


def nome_seguro(nome):
    """Nome de arquivo só com letras, números, ponto, hífen e sublinhado; sempre termina em .docx."""
    base = unicodedata.normalize('NFKD', nome or '').encode('ascii', 'ignore').decode()
    base = re.sub(r'[^\\w.-]+', '-', re.sub(r'\\.docx$', '', base.strip(), flags=re.I)).strip('.-_')
    return (base or 'minuta-impugnacao') + '.docx'


class Tools:
    class Valves(BaseModel):
        CNPJ: str = Field('', description='CNPJ da empresa, para o campo "[Inserir CNPJ]".')
        ENDERECO: str = Field('', description='Endereço da sede, para o campo "[Inserir Endereço Completo]".')

    def __init__(self):
        self.valves = self.Valves()

    def gerar_minuta_impugnacao(self, markdown: str, data: Optional[str] = None, nome_arquivo: Optional[str] = None):
        """
        Conversor legado de uma impugnação já aprovada em Markdown no .docx da Servfaz. Para o fluxo operacional,
        prefira a Action "Exportar Minuta de Impugnacao Servfaz", que exige clique e confirmação humana antes de
        gerar o arquivo. Esta Tool não escreve, corrige nem resume o texto: o que está no Markdown vai para o Word.
        Só CNPJ e endereço corporativos configurados são preenchidos; nome, RG, CPF e campos ausentes ficam em
        destaque amarelo para preenchimento manual. Recusa referência interna da triagem ou marcação não tratada.

        :param markdown: Texto completo da impugnação, em Markdown, exatamente como o usuário aprovou.
        :param data: Data da peça no formato AAAA-MM-DD, só se o usuário a informou. Não invente uma data.
        :param nome_arquivo: Nome do arquivo .docx (opcional), por exemplo "impugnacao-ufpi-pe-90009-2026".
        """
        try:
            when = date.fromisoformat(data) if data else None
        except ValueError:
            return {'ok': False, 'erro': f'data inválida: {data} (use AAAA-MM-DD).'}
        if not (markdown or '').strip():
            return {'ok': False, 'erro': 'O Markdown da impugnação está vazio.'}
        dados = {'cnpj': self.valves.CNPJ, 'endereco': self.valves.ENDERECO}
        try:
            doc, pendentes = render(markdown, io.BytesIO(base64.b64decode(_TIMBRE_B64)), dados, when)
        except Refusal as exc:
            return {'ok': False, 'erro': str(exc)}
        buffer = io.BytesIO()
        doc.save(buffer)
        nome = nome_seguro(nome_arquivo)
        kb = max(1, round(buffer.tell() / 1024))
        itens = ''.join(f'<li>linha {n}: <mark>{escape(marcador)}</mark></li>' for n, marcador in pendentes)
        bloco = (f'<div class="pendencias">{len(pendentes)} campo(s) em branco, em destaque amarelo no .docx, '
                 f'para preencher à mão:<ul>{itens}</ul></div>') if pendentes else ''
        html = PAGINA.format(nome=escape(nome), tamanho=kb, mime=DOCX, pendencias=bloco,
                             dados=base64.b64encode(buffer.getvalue()).decode())
        contexto = {'ok': True, 'arquivo': nome, 'tamanho_kb': kb,
                    'campos_em_branco': [{'linha': n, 'marcador': m} for n, m in pendentes],
                    'proxima_acao': 'O botão de download já está no chat. Diga ao usuário o nome do arquivo e, se '
                                    'houver campos_em_branco, liste-os e explique que estão em destaque amarelo no '
                                    '.docx para preencher à mão. Lembre que revisão, assinatura e protocolo são dele.'}
        return HTMLResponse(content=html, headers={'Content-Disposition': 'inline'}), contexto
'''


def nucleo():
    achado = NUCLEO.search(FONTE.read_text(encoding='utf-8'))
    if not achado:
        raise SystemExit(f'marcadores de núcleo não encontrados em {FONTE}')
    return achado[1].rstrip() + '\n'


def timbre_leve():
    """Devolve o modelo integral, sem otimização dependente do ambiente de montagem."""
    return TIMBRE.read_bytes()


def montar():
    codificado = base64.b64encode(timbre_leve()).decode()
    linhas = '\n'.join(codificado[i:i + 120] for i in range(0, len(codificado), 120))
    return (CABECALHO + '\n' + nucleo() + ADAPTADOR + '\n\n# Timbre da Servfaz (assets/timbre-servfaz.docx), em base64.\n'
            '_TIMBRE_B64 = """\n' + linhas + '\n"""\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--saida', type=Path, default=SAIDA, help='destino (padrão: tools/gerar_minuta_impugnacao.py)')
    args = parser.parse_args(argv)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(montar(), encoding='utf-8')
    print(f'{args.saida} ({args.saida.stat().st_size // 1024} KB)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
