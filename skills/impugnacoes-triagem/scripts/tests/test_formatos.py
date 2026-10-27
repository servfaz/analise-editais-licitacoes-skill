"""Formatos fixos das frases do analista: o que segue o formato passa, o resto é recusado com o formato esperado e um
exemplo preenchido com os dados da triagem. Nada aqui interpreta texto livre."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from triagem import formatos
from triagem.comandos import new_item
from triagem.comum import KINDS, Refusal

# Itens fictícios.
IDS = ('IMP-01', 'IMP-03', 'IMP-20', 'ESC-01', 'ESC-02')


def make_items(decided=()):
    items = [new_item(item_id, KINDS[item_id[:3]], f'Ponto fictício {item_id}') for item_id in IDS]
    for item in items:
        if item['id'] in decided:
            item.update(decisao='incluir', evidencia=f'incluo {item["id"]}')
    return items


def plan_ids(plan):
    return [(decision, [item['id'] for item in targets]) for decision, targets in plan]


class FormatTestCase(unittest.TestCase):
    def refused(self, call, *args, contains):
        with self.assertRaises(Refusal) as raised:
            call(*args)
        message = str(raised.exception)
        for part in [contains] if isinstance(contains, str) else contains:
            self.assertIn(part, message)
        self.assertIn('Formato esperado:', message)
        self.assertIn('não converta uma resposta livre', message)
        return message


class ProsseguirTests(FormatTestCase):
    def test_accepted_variations(self):
        for phrase in ('prossigo sem ETP e PESQUISA', 'Prossigo sem o ETP e a pesquisa.', 'PROSSIGO  SEM  etp, pesquisa!',
                       'prossigo sem PESQUISA, ETP', 'prossigo sem ETP, PESQUISA e ETP'):
            with self.subTest(phrase=phrase):
                self.assertEqual(formatos.parse_proceed(phrase, ['ETP', 'PESQUISA']), ' '.join(phrase.split()))

    def test_refused_with_example_of_the_missing_documents(self):
        example = 'Exemplo com os dados desta triagem: "prossigo sem ETP e PESQUISA"'
        cases = [('pode seguir', 'não está no formato do prosseguir'), ('ok', 'não está no formato'),
                 ('não tenho ETP nem pesquisa, pode seguir', 'não está no formato'),
                 ('prossigo sem ETP?', '"ETP?" não é código de documento'), ('não prossigo sem ETP', 'não está no formato'),
                 ('prossigo sem ETP', 'não cita PESQUISA'), ('prossigo sem ETP, PESQUISA e TR', 'cita TR, que não falta'),
                 ('prossigo sem ETP e RERI', '"RERI" não é código de documento'),
                 ('prossigo sem os documentos', 'não é código de documento')]
        for phrase, message in cases:
            with self.subTest(phrase=phrase):
                self.refused(formatos.parse_proceed, phrase, ['ETP', 'PESQUISA'], contains=[message, example])


class DecidirTests(FormatTestCase):
    def test_clauses_ids_and_the_rest(self):
        cases = [
            ('incluo IMP-01, IMP-03 e ESC-02; descarto os demais',
             [('incluir', ['IMP-01', 'IMP-03', 'ESC-02']), ('descartar', ['IMP-20', 'ESC-01'])]),
            ('Incluo a IMP-1 ; deixo para depois o ESC-1.', [('incluir', ['IMP-01']), ('avaliar_depois', ['ESC-01'])]),
            ('descarto os demais; incluo IMP-20', [('descartar', ['IMP-01', 'IMP-03', 'ESC-01', 'ESC-02']),
                                                   ('incluir', ['IMP-20'])]),
            ('deixo para depois demais', [('avaliar_depois', list(IDS[:3]) + ['ESC-01', 'ESC-02'])]),
            ('INCLUO IMP-01; INCLUO IMP-03', [('incluir', ['IMP-01']), ('incluir', ['IMP-03'])]),
            ('incluo todos', [('incluir', list(IDS[:3]) + ['ESC-01', 'ESC-02'])]),
            ('descarto IMP-01; incluo todas', [('descartar', ['IMP-01']), ('incluir', ['IMP-03', 'IMP-20', 'ESC-01', 'ESC-02'])]),
        ]
        for phrase, expected in cases:
            with self.subTest(phrase=phrase):
                evidence, plan = formatos.parse_decide(phrase, make_items())
                self.assertEqual((evidence, plan_ids(plan)), (' '.join(phrase.split()), expected))

    def test_the_rest_are_only_the_pending_not_cited(self):
        _, plan = formatos.parse_decide('descarto os demais', make_items(decided=('IMP-01', 'ESC-02')))
        self.assertEqual(plan_ids(plan), [('descartar', ['IMP-03', 'IMP-20', 'ESC-01'])])
        _, plan = formatos.parse_decide('deixo para depois IMP-01', make_items(decided=('IMP-01',)))
        self.assertEqual(plan_ids(plan), [('avaliar_depois', ['IMP-01'])])  # decidido sem minuta pode mudar

    def test_example_shown_in_a_refusal_is_itself_accepted(self):
        def item(item_id, decision):
            data = new_item(item_id, KINDS[item_id[:3]], 'Item')
            data['decisao'] = decision
            return data
        for decisions in (('pendente',) * 3, ('incluir', 'descartar', 'avaliar_depois')):
            with self.subTest(decisoes=decisions):
                items = [item(item_id, d) for item_id, d in zip(('IMP-01', 'IMP-02', 'ESC-01'), decisions)]
                message = self.refused(formatos.parse_decide, 'pode incluir', items, contains='Exemplo')
                example = message.split('Exemplo com os dados desta triagem: "', 1)[1].split('"', 1)[0]
                formatos.parse_decide(example, items)

    def test_refused_phrases(self):
        cases = [('incluo tudo', 'não está no formato do decidir'), ('inclui IMP-01', 'não está no formato'),
                 ('incluo IMP-01 e descarto IMP-03', 'não está no formato'), ('incluo IMP-01;', None),
                 ('ok', 'não está no formato'), ('incluo IMP-01;; descarto IMP-03', 'não está no formato'),
                 ('incluo IMP 01', 'não está no formato'), ('incluo PENDENTES', 'não está no formato'),
                 ('incluo IMP-07', 'IMP-07 não está registrado'),
                 ('incluo IMP-01; descarto IMP-1', 'IMP-01 aparece mais de uma vez'),
                 ('incluo IMP-01, IMP-01', 'IMP-01 aparece mais de uma vez'),
                 ('incluo os demais; descarto os demais', '"os demais" aparece em mais de uma cláusula'),
                 ('incluo IMP-01, IMP-03, IMP-20, ESC-01 e ESC-02; descarto os demais', 'não tem a que se referir')]
        for phrase, message in cases:
            with self.subTest(phrase=phrase):
                if message is None:  # o ";" final é pontuação final
                    formatos.parse_decide(phrase, make_items())
                    continue
                self.refused(formatos.parse_decide, phrase, make_items(), contains=message)

    def test_example_uses_the_pending_items(self):
        expected = [((), '"incluo IMP-01; descarto IMP-03; deixo para depois os demais"'),
                    (IDS[:3] + ('ESC-01',), '"incluo ESC-02"'),
                    (IDS[:3], '"incluo ESC-01; descarto ESC-02"')]
        for decided, example in expected:
            with self.subTest(decided=decided):
                self.refused(formatos.parse_decide, 'ok', make_items(decided), contains=example)

    def test_recorded_phrase_is_checked_per_item(self):
        phrase = 'incluo IMP-01 e ESC-02; descarto os demais'
        formatos.check_decided(phrase, 'IMP-01', 'incluir')
        formatos.check_decided(phrase, 'IMP-20', 'descartar')
        for item_id, decision in (('IMP-01', 'descartar'), ('IMP-20', 'incluir'), ('IMP-20', 'avaliar_depois')):
            with self.subTest(item_id=item_id, decision=decision), self.assertRaises(Refusal):
                formatos.check_decided(phrase, item_id, decision)


class MinutaTests(FormatTestCase):
    def test_accepted_actions(self):
        cases = [('aprovo IMP-20', 'aprovar'), ('Aprovo a IMP-20.', 'aprovar'), ('APROVO imp-20!', 'aprovar'),
                 ('descarto o IMP-20', 'descartar'), ('ajuste IMP-20: cite a página 3 do TR', 'ajustar'),
                 ('Ajuste a IMP-20 : troque o pedido subsidiário', 'ajustar')]
        for phrase, action in cases:
            with self.subTest(phrase=phrase):
                self.assertEqual(formatos.parse_draft(phrase, 'IMP-20'), (action, ' '.join(phrase.split())))
        self.assertEqual(formatos.parse_draft('aprovo IMP-1', 'IMP-01')[0], 'aprovar')

    def test_refused_with_the_id_in_review(self):
        example = '"aprovo IMP-20" ou "ajuste IMP-20: cite a página do TR no pedido" ou "descarto IMP-20"'
        cases = [('aprovo', 'não está no formato da decisão sobre a minuta'), ('ok', 'não está no formato'),
                 ('aprovo todas', 'não está no formato'), ('aprovo IMP-20?', 'não está no formato'),
                 ('aprovo IMP-20, mas troque o pedido', 'não está no formato'),
                 ('não aprovo IMP-20', 'não está no formato'), ('ajuste: troque o pedido', 'não está no formato'),
                 ('aprovo IMP-20 e IMP-01', 'um ID só'), ('aprovo IMP-01', 'cita IMP-01, mas a minuta em revisão é IMP-20'),
                 ('ajuste IMP-20: curto', 'menos de 10 caracteres'), ('ajuste IMP-20:', 'menos de 10 caracteres')]
        for phrase, message in cases:
            with self.subTest(phrase=phrase):
                self.refused(formatos.parse_draft, phrase, 'IMP-20', contains=[message, example])


class ReabrirPecaAceiteTests(FormatTestCase):
    def test_reopen(self):
        items, evidence = formatos.parse_reopen('Reabro a IMP-01 e o ESC-2: mudei de ideia sobre isso.',
                                                make_items(('IMP-01',)))
        self.assertEqual(([item['id'] for item in items], evidence),
                         (['IMP-01', 'ESC-02'], 'Reabro a IMP-01 e o ESC-2: mudei de ideia sobre isso.'))
        example = '"reabro IMP-01: mudei de ideia sobre este ponto"'
        for phrase, message in (('reabro IMP-01', 'não está no formato do reabrir'),
                                ('reabre IMP-01: mudei de ideia', 'não está no formato'),
                                ('reabro IMP-01: engano', 'menos de 10 caracteres'),
                                ('reabro IMP-09: mudei de ideia sobre isso', 'IMP-09 não está registrado')):
            with self.subTest(phrase=phrase):
                self.refused(formatos.parse_reopen, phrase, make_items(('IMP-01',)), contains=[message, example])

    def test_piece(self):
        for phrase, expected in (('confirmo a peça de impugnação em formato único', ('impugnacao', 'unico')),
                                 ('Confirmo peça de esclarecimento em formato por ponto.', ('esclarecimento', 'por_ponto')),
                                 ('CONFIRMO A PECA DE IMPUGNACAO EM FORMATO UNICO', ('impugnacao', 'unico'))):
            with self.subTest(phrase=phrase):
                self.assertEqual(formatos.parse_piece(phrase)[:2], expected)
        for phrase in ('confirmo', 'confirmo a peça única', 'confirmo a peça de impugnação',
                       'confirmo a peça de impugnação em formato único?', 'pode gerar a peça de impugnação',
                       'confirmo a peça de impugnação em formato misto'):
            with self.subTest(phrase=phrase):
                self.refused(formatos.parse_piece, phrase, ['esclarecimento'],
                             contains=['não está no formato da confirmação da peça',
                                       '"confirmo a peça de esclarecimento em formato único"'])

    def test_accept(self):
        phrase = 'Aceito a edição do estado: corrigi o título do ESC-02'
        self.assertEqual(formatos.parse_accept(phrase), phrase)
        self.assertEqual(formatos.parse_accept('aceito edicao do estado: corrigi o título'),
                         'aceito edicao do estado: corrigi o título')
        example = f'"{formatos.ACCEPT_EXAMPLE}"'
        for phrase, message in (('aceito a edição', 'não está no formato do aceite'), ('mantém', 'não está no formato'),
                                ('aceito a edição do estado: ok', 'menos de 10 caracteres'),
                                ('não aceito a edição do estado: não fui eu', 'não está no formato')):
            with self.subTest(phrase=phrase):
                self.refused(formatos.parse_accept, phrase, contains=[message, example])


if __name__ == '__main__':
    unittest.main()
