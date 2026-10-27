#!/usr/bin/env python3
"""Gera assets/timbre-servfaz.docx a partir de uma peça .docx da Servfaz (a de referência é a da FMS). Python 3.10+.

Só para quem mantém a skill; a geração da minuta nunca roda este script. Da peça de origem ficam o cabeçalho e o rodapé com o
timbre, as imagens, as margens e os estilos; o corpo é apagado inteiro. Ficam acrescentados os estilos "Peca ..." e a
numeração (romana nas seções, alíneas a), b) nas listas) que gerar_minuta.py usa. Os metadados de autoria são
limpos, porque o timbre vai para o git.

Uso:
  criar_timbre.py --origem PECA.docx [--saida assets/timbre-servfaz.docx]
"""
import argparse
import sys
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gerar_minuta import ALINEA_NUMBERING, ROMAN_NUMBERING, STYLES  # noqa: E402

DEFAULT_OUT = Path(__file__).resolve().parents[1] / 'assets' / 'timbre-servfaz.docx'
FONT, SIZE = 'Times New Roman', Pt(12.5)


def clear_body(doc):
    body = doc.element.body
    for child in list(body):
        if child.tag != qn('w:sectPr'):
            body.remove(child)


def clear_metadata(doc):
    props = doc.core_properties
    props.author, props.last_modified_by, props.title, props.subject = 'Servfaz', 'Servfaz', '', ''
    props.comments, props.keywords, props.revision = '', '', 1


def element(tag, **attrs):
    node = OxmlElement(tag)
    for name, value in attrs.items():
        node.set(qn(f'w:{name}'), str(value))
    return node


def add_abstract(numbering, name, fmt, text, left, hanging, bold=False):
    """Acrescenta um abstractNum de um nível, identificado por w:name (o conversor o procura pelo nome)."""
    ids = [int(n.get(qn('w:abstractNumId'))) for n in numbering.findall(qn('w:abstractNum'))]
    abstract_id = max(ids, default=0) + 1
    abstract = element('w:abstractNum', abstractNumId=abstract_id)
    abstract.append(element('w:multiLevelType', val='singleLevel'))
    abstract.append(element('w:name', val=name))
    level = element('w:lvl', ilvl=0)
    for child in (element('w:start', val=1), element('w:numFmt', val=fmt), element('w:lvlText', val=text),
                  element('w:lvlJc', val='left')):
        level.append(child)
    ppr = element('w:pPr')
    ppr.append(element('w:ind', left=left, hanging=hanging))
    level.append(ppr)
    if bold:
        rpr = element('w:rPr')
        rpr.append(element('w:b'))
        level.append(rpr)
    abstract.append(level)
    existing = numbering.findall(qn('w:abstractNum'))
    if existing:
        existing[-1].addnext(abstract)
    else:
        numbering.insert(0, abstract)
    return abstract_id


def add_num(numbering, abstract_id):
    ids = [int(n.get(qn('w:numId'))) for n in numbering.findall(qn('w:num'))]
    num_id = max(ids, default=0) + 1
    num = element('w:num', numId=num_id)
    num.append(element('w:abstractNumId', val=abstract_id))
    numbering.append(num)
    return num_id


def paragraph_style(doc, name, base=None):
    styles = doc.styles
    style = styles[name] if name in [s.name for s in styles] else styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    style.base_style = styles[base] if base else None
    style.quick_style = True
    return style


def define_styles(doc, roman_num):
    body = paragraph_style(doc, STYLES['corpo'])
    body.font.name, body.font.size = FONT, SIZE
    body.element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:cs'), FONT)
    fmt = body.paragraph_format
    fmt.alignment, fmt.space_before, fmt.space_after, fmt.line_spacing = WD_ALIGN_PARAGRAPH.JUSTIFY, Pt(0), Pt(10), 1.0
    fmt.widow_control = True

    title = paragraph_style(doc, STYLES['titulo'], STYLES['corpo'])
    title.font.bold = True
    title.paragraph_format.keep_with_next, title.paragraph_format.space_before = True, Pt(12)
    numpr = element('w:numPr')
    numpr.append(element('w:ilvl', val=0))
    numpr.append(element('w:numId', val=roman_num))
    title.element.get_or_add_pPr().insert(0, numpr)

    sub = paragraph_style(doc, STYLES['subtitulo'], STYLES['corpo'])
    sub.font.bold = True
    sub.paragraph_format.keep_with_next, sub.paragraph_format.space_before = True, Pt(6)

    quote = paragraph_style(doc, STYLES['citacao'], STYLES['corpo'])
    quote.font.italic = True
    quote.paragraph_format.left_indent = Cm(4)

    alinea = paragraph_style(doc, STYLES['alinea'], STYLES['corpo'])
    alinea.paragraph_format.left_indent, alinea.paragraph_format.first_line_indent = Cm(1.25), Cm(-0.63)

    center = paragraph_style(doc, STYLES['centro'], STYLES['corpo'])
    center.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    table = paragraph_style(doc, STYLES['tabela'], STYLES['corpo'])
    table.font.size = Pt(10)
    table.paragraph_format.alignment, table.paragraph_format.space_after = WD_ALIGN_PARAGRAPH.LEFT, Pt(0)


# Rodapé: a linha laranja ("Conector reto 9") ficava a 5,2 pt do topo do parágrafo e cortava ao meio o texto
# "servfazpi | www.servfaz.com.br", que começa em cerca de -2 pt. A linha sobe para acima do texto.
FOOTER_LINE = 'Conector reto 9'
LINE_OLD_EMU, LINE_NEW_EMU = '66040', '-114300'


def fix_footer(doc):
    """Sobe a linha do rodapé para acima do texto. Idempotente; devolve quantos ajustes fez."""
    changed = 0
    for section in doc.sections:
        footer = section.footer
        if footer.is_linked_to_previous:
            continue
        root = footer._element
        for offset in root.xpath(f'.//wp:anchor[wp:docPr/@name="{FOOTER_LINE}"]/wp:positionV/wp:posOffset'):
            if offset.text == LINE_OLD_EMU:
                offset.text, changed = LINE_NEW_EMU, changed + 1
        for line in root.xpath(f'.//*[local-name()="line"][@id="{FOOTER_LINE}"]'):
            if line.get('from') == '-6pt,5.2pt':
                line.set('from', '-6pt,-9pt')
                line.set('to', '518.4pt,-7.8pt')
                changed += 1
    return changed


def build(origin, out):
    doc = Document(str(origin))
    clear_body(doc)
    clear_metadata(doc)
    numbering = doc.part.numbering_part.element
    for abstract in numbering.findall(qn('w:abstractNum')):
        name = abstract.find(qn('w:name'))
        if name is not None and name.get(qn('w:val')) in (ROMAN_NUMBERING, ALINEA_NUMBERING):
            raise SystemExit(f'a origem já tem a numeração {name.get(qn("w:val"))}: use uma peça, não um timbre.')
    roman = add_abstract(numbering, ROMAN_NUMBERING, 'upperRoman', '%1.', left=567, hanging=567, bold=True)
    add_abstract(numbering, ALINEA_NUMBERING, 'lowerLetter', '%1)', left=709, hanging=357)
    define_styles(doc, add_num(numbering, roman))
    fix_footer(doc)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--origem', required=True, type=Path, help='peça .docx da Servfaz com o timbre')
    parser.add_argument('--saida', type=Path, default=DEFAULT_OUT, help='destino (padrão: assets/timbre-servfaz.docx)')
    args = parser.parse_args(argv)
    print(build(args.origem, args.saida))
    return 0


if __name__ == '__main__':
    sys.exit(main())
