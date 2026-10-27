"""Preenchimento do modelo .md: front matter, blocos {{#X}}…{{/X}}, campos {{X}} e trava de referência interna."""
import re

from triagem.comum import Refusal

FRONT = re.compile(r'\A---\n.*?\n---\n', re.S)
TAG_LINE = re.compile(r'[ \t]*\{\{([#/])([A-Z_]+)\}\}[ \t]*')
INLINE_BLOCK = re.compile(r'\{\{#([A-Z_]+)\}\}(.*?)\{\{/\1\}\}')
FIELD = re.compile(r'\{\{([A-Z_]+)\}\}')
# O catálogo de fontes é interno: nenhum ID, marcador [ID · status] ou menção a ele ou aos arquivos do estudo chega à
# peça. "Catálogo" sozinho não conta: um edital pode citar o Catálogo de Serviços.
INTERNAL = re.compile(r'\b(?:EXT|INT|NOVA)-[A-Z0-9]|\[[^\]\n]*·[^\]\n]*\]|cat[aá]logo[ -]de[ -]fontes|'
                      r'(?:catalogo|indice)-fontes|references/estudo|\b[a-z]+/(?:fontes|analise|estrutura)\.md', re.I)


def strip_front(text):
    return FRONT.sub('', text, count=1)


def apply_blocks(text, flags):
    """Linha só com {{#X}} ou {{/X}} abre ou fecha um bloco e sai da peça; o bloco fica se flags[X] for verdadeiro.
    Dentro da linha, {{#X}}…{{/X}} faz o mesmo com o trecho."""
    out, stack = [], []
    for number, line in enumerate(text.split('\n'), 1):
        tag = TAG_LINE.fullmatch(line)
        if tag:
            kind, name = tag.groups()
            if kind == '#':
                stack.append(name)
            elif not stack or stack.pop() != name:
                raise Refusal(f'modelo: {{{{/{name}}}}} na linha {number} não fecha o bloco aberto.')
            continue
        if all(flags.get(name) for name in stack):
            out.append(INLINE_BLOCK.sub(lambda m: m[2] if flags.get(m[1]) else '', line))
    if stack:
        raise Refusal(f'modelo: bloco {{{{#{stack[-1]}}}}} sem fechamento.')
    return '\n'.join(out)


def fill(template, fields, flags):
    text = apply_blocks(strip_front(template), flags)
    missing = sorted({name for name in FIELD.findall(text) if fields.get(name) in (None, '')})
    if missing:
        raise Refusal('faltam campos para montar a peça: ' + ', '.join(missing) + '.')
    text = FIELD.sub(lambda m: str(fields[m[1]]), text)
    return re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'


def check_clean(text, label):
    """A trava: a peça não sai com marcador de campo nem com referência interna da triagem."""
    problems = []
    for number, line in enumerate(text.split('\n'), 1):
        if '{{' in line or '}}' in line:
            problems.append(f'linha {number}: marcador de campo não preenchido')
        found = INTERNAL.search(line)
        if found:
            problems.append(f'linha {number}: referência interna "{found[0]}"')
    if problems:
        raise Refusal(f'{label} não pode sair assim: ' + '; '.join(problems[:10]) + '. Corrija a origem (modelo ou '
                      'minuta aprovada, pela fase certa) e monte de novo; não edite a peça para passar.')
    return text
