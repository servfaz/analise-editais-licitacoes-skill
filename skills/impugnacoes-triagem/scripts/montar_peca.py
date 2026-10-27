#!/usr/bin/env python3
"""Peça final da triagem: monta a peça em Markdown a partir do modelo e das minutas aprovadas. Python 3.10+. O contrato
(campos, blocos opcionais, convenções) está em assets/LEIA-ME.md. A conversão da peça em .docx é da skill
gerar-minuta-impugnacao, depois que o analista conferir o texto montado.

  montar     só roda com a peça do tipo confirmada no estado.py (peca --acao confirmar), sem pendências e com o
             modelo modelo-<tipo>.md em assets/. Lê <pasta>/dados-peca.json e o arquivo do representante
             (padrão: files/representante.json, duas pastas acima da pasta do edital, fora do git) e grava
             <pasta>/peca/peca-<tipo>.md (formato único) ou peca-<tipo>-<ID>.md (por ponto).
Para se a peça trouxer marcador de campo não preenchido ou referência interna da triagem (ID ou marcador do
catálogo de fontes): o catálogo não aparece na peça. Nada aqui assina, protocola ou envia.

Uso:
  montar_peca.py montar --pasta DIR --tipo impugnacao|esclarecimento [--representante ARQ] [--data AAAA-MM-DD]
"""
import argparse
import json
import sys
from pathlib import Path

from montagem.montar import assemble
from triagem.comum import Refusal, parse_date


def cmd_assemble(args):
    when = None
    if args.data:
        when = parse_date(args.data)
        if not when:
            raise Refusal(f'data inválida: {args.data} (use AAAA-MM-DD).')
    paths = assemble(args.pasta, args.tipo, args.representante, when)
    return {'montadas': [str(path) for path in paths],
            'proxima_acao': 'apresente cada peça montada ao analista; depois do "ok" dele, gere o .docx de cada uma com a skill gerar-minuta-impugnacao'}


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='comando', required=True, metavar='COMANDO')
    p = sub.add_parser('montar', help='grava a peça em Markdown a partir do modelo e das minutas aprovadas')
    p.add_argument('--pasta', type=Path, required=True, help='pasta do edital')
    p.add_argument('--tipo', required=True, choices=('impugnacao', 'esclarecimento'))
    p.add_argument('--representante', type=Path, help='JSON com nome, cargo e designacao de quem assina')
    p.add_argument('--data', help='data da peça (padrão: hoje)')
    p.set_defaults(handler=cmd_assemble)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        outcome = args.handler(args)
    except Refusal as exc:
        print(f'erro: {exc}', file=sys.stderr)
        return 1
    except OSError as exc:
        print(f'erro: não foi possível ler ou gravar {exc.filename or "um arquivo da peça"}: {exc.strerror or exc}.',
              file=sys.stderr)
        return 1
    print(json.dumps(outcome, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
