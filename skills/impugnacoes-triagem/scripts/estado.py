#!/usr/bin/env python3
"""Máquina de estados da triagem de um edital: impõe os portões da skill impugnacoes-triagem. Python 3.10+.

A fase é derivada dos dados, nesta ordem: documentos, levantamento, selecao, minutas, peca_final, concluido.
O estado fica em <pasta>/estado.json (fonte de verdade); <pasta>/registro.md é regenerado a cada mudança.
A cada turno, rode "status" e faça só a ação de "proxima_acao". Os comandos recusam transições fora de ordem.
Os comandos que gravam usam uma trava por pasta (.estado.lock): chamadas em paralelo esperam a vez.
Cada gravação deixa em <pasta>/.estado.sha256 o sha256 do estado.json e em <pasta>/.estado.gravado.json uma cópia
dele. Se o sha256 não confere (estado.json editado à mão), o status alerta, o validar sai com 1 e os comandos que
gravam recusam até o analista decidir: se ele mantém a alteração, "aceitar-edicao" registra a frase dele e libera, desde
que a alteração (comparada com a cópia) mexa só no título de item ou nos dados do certame.
As frases do analista (--evidencia) têm formato fixo, e o script confere só o formato (triagem/formatos.py): a skill
pede ao analista que digite a frase no formato e nunca converte uma resposta livre. A comparação ignora maiúsculas,
acentos, espaços repetidos, o artigo antes de ID ("a IMP-01") e a pontuação final; vírgula e "e" separam os itens de
uma lista. Toda recusa traz o formato esperado e um exemplo com os dados da triagem.
O estudo é sempre o references/estudo/MANIFEST.json da skill e o modelo da peça, sempre assets/ da skill: não há
opção para apontar outra pasta.

Uso:
  estado.py slug --orgao TXT --modalidade TXT --numero TXT --ano AAAA
  estado.py iniciar --raiz DIR --orgao TXT --modalidade TXT --numero TXT --ano AAAA [--esfera ESFERA] [--slug SLUG]
  estado.py status --pasta DIR
  estado.py documentos --pasta DIR --presentes EDITAL,TR --faltas ETP,PLANILHA,PESQUISA,MINUTA
  estado.py prosseguir --pasta DIR --evidencia "prossigo sem ETP e PESQUISA"     (exatamente as faltas registradas)
  estado.py prazo --pasta DIR --dados prazo.json        (--dados - lê da entrada padrão)
  estado.py itens --pasta DIR --arquivo itens.json      (lista de {id, classe, titulo})
  estado.py decidir --pasta DIR --evidencia "incluo IMP-01, IMP-03 e ESC-02; descarto os demais"
        cláusulas "incluo <IDs>", "descarto <IDs>", "deixo para depois <IDs>" separadas por ";"; "os demais" são os
        pendentes não citados; o item não citado continua pendente
  estado.py minuta --pasta DIR --acao abrir
  estado.py minuta --pasta DIR --id IMP-01 --acao registrar
  estado.py minuta --pasta DIR --evidencia "aprovo IMP-01"     (ou "descarto IMP-01", "ajuste IMP-01: <o que mudar>")
  estado.py reabrir --pasta DIR --evidencia "reabro IMP-01: <motivo>"
  estado.py peca --pasta DIR --acao verificar
  estado.py peca --pasta DIR --acao confirmar --evidencia "confirmo a peça de impugnação em formato único"
        (ou "... de esclarecimento ...", "... em formato por ponto")
  estado.py validar --pasta DIR                         sai com 1 se houver violação (invariante ou edição à mão)
  estado.py aceitar-edicao --pasta DIR --evidencia "aceito a edição do estado: <motivo>"
Instrução do ajuste e motivos têm pelo menos 10 caracteres.
"""
import argparse
import json
import sys
from pathlib import Path

from triagem.comandos import (cmd_decide, cmd_deadline, cmd_documents, cmd_init, cmd_items, cmd_proceed, cmd_reopen,
                              cmd_slug, cmd_status)
from triagem.comum import DOC_CODES, SPHERES, Refusal
from triagem.aceite import cmd_accept_edit
from triagem.invariantes import cmd_validate
from triagem.minutas import cmd_draft
from triagem.peca import cmd_piece
from triagem.persistencia import changing


def certame_args(parser):
    parser.add_argument('--orgao', required=True, help='órgão ou ente (ex.: "Secretaria de Saúde de X")')
    parser.add_argument('--modalidade', required=True, help='modalidade (ex.: PE, CC)')
    parser.add_argument('--numero', required=True, help='número do certame')
    parser.add_argument('--ano', required=True, help='ano com 4 dígitos')


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='comando', required=True, metavar='COMANDO')
    folder = argparse.ArgumentParser(add_help=False)
    folder.add_argument('--pasta', type=Path, required=True, help='pasta do edital')

    p = sub.add_parser('slug', help='imprime o slug da pasta do edital')
    certame_args(p)
    p.set_defaults(handler=cmd_slug)
    p = sub.add_parser('iniciar', help='cria a pasta do edital')
    certame_args(p)
    p.add_argument('--raiz', type=Path, required=True, help='pasta onde ficam as triagens')
    p.add_argument('--esfera', choices=SPHERES)
    p.add_argument('--slug', help='slug próprio (padrão: orgao-modalidade-numero-ano)')
    p.set_defaults(handler=cmd_init)
    p = sub.add_parser('status', parents=[folder], help='fase, próxima ação e alertas')
    p.set_defaults(handler=cmd_status)
    p = sub.add_parser('documentos', parents=[folder], help='registra o portão documental')
    p.add_argument('--presentes', default='', help=f'códigos separados por vírgula: {",".join(DOC_CODES)}')
    p.add_argument('--faltas', default='', help='códigos que faltam, separados por vírgula')
    p.add_argument('--esfera', choices=SPHERES)
    p.set_defaults(handler=changing(cmd_documents))
    p = sub.add_parser('prosseguir', parents=[folder], help='registra a decisão de seguir sem os documentos que faltam')
    p.add_argument('--evidencia', required=True, help='frase do analista: "prossigo sem <códigos>"')
    p.set_defaults(handler=changing(cmd_proceed))
    p = sub.add_parser('prazo', parents=[folder], help='guarda o JSON de "prazo.py --json"')
    p.add_argument('--dados', required=True, help='arquivo JSON ou - para ler da entrada padrão')
    p.set_defaults(handler=changing(cmd_deadline))
    p = sub.add_parser('itens', parents=[folder], help='registra (ou acrescenta) os itens do levantamento')
    p.add_argument('--arquivo', required=True, help='JSON com a lista de {id, classe, titulo} (ou -)')
    p.set_defaults(handler=changing(cmd_items))
    p = sub.add_parser('decidir', parents=[folder], help='registra a seleção do analista (todas as cláusulas)')
    p.add_argument('--evidencia', required=True,
                   help='frase do analista: "incluo <IDs>; descarto <IDs>; deixo para depois <IDs>" ("os demais")')
    p.set_defaults(handler=changing(cmd_decide))
    p = sub.add_parser('minuta', parents=[folder], help='abre, registra e decide a minuta em revisão')
    p.add_argument('--acao', choices=('abrir', 'registrar'), help='sem --acao, a frase de --evidencia decide')
    p.add_argument('--id', help='ID da minuta em revisão')
    p.add_argument('--evidencia', help='frase do analista: "aprovo <ID>", "descarto <ID>" ou "ajuste <ID>: ..."')
    p.set_defaults(handler=changing(cmd_draft))
    p = sub.add_parser('reabrir', parents=[folder], help='volta itens para a seleção (o analista mudou de ideia)')
    p.add_argument('--evidencia', required=True, help='frase do analista: "reabro <IDs>: <motivo>"')
    p.set_defaults(handler=changing(cmd_reopen))
    p = sub.add_parser('peca', parents=[folder], help='verifica ou confirma a peça final (a peça sai pelo montar_peca.py)')
    p.add_argument('--acao', required=True, choices=('verificar', 'confirmar'))
    p.add_argument('--evidencia', help='frase do analista (confirmar): "confirmo a peça de impugnação|esclarecimento '
                                       'em formato único|por ponto"')
    p.set_defaults(handler=cmd_piece)
    p = sub.add_parser('validar', parents=[folder], help='confere os invariantes; sai com 1 se houver violação')
    p.set_defaults(handler=cmd_validate)
    p = sub.add_parser('aceitar-edicao', parents=[folder],
                       help='registra que o analista mantém o estado.json alterado fora do estado.py')
    p.add_argument('--evidencia', required=True, help='frase do analista: "aceito a edição do estado: <motivo>"')
    p.set_defaults(handler=changing(cmd_accept_edit, intact=False))
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        outcome = args.handler(args)
    except Refusal as exc:
        print(f'erro: {exc}', file=sys.stderr)
        return 1
    except OSError as exc:
        target = exc.filename or 'um arquivo da triagem'
        print(f'erro: não foi possível ler ou gravar {target}: {exc.strerror or exc}. Confira o caminho e as '
              'permissões e rode de novo.', file=sys.stderr)
        return 1
    if isinstance(outcome, dict):
        print(json.dumps(outcome, ensure_ascii=False, indent=2))
        return 0
    return outcome


if __name__ == '__main__':
    sys.exit(main())
