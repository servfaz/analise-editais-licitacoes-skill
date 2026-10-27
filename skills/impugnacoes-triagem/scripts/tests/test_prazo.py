import io
import json
import sys
import tempfile
import unicodedata
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import prazo
from prazo import closed_days, deadline, easter, load_calendar

CALENDAR = load_calendar()
KEYS = {'abertura', 'dias_uteis', 'data_limite', 'data_limite_com_pontos_facultativos', 'dias_desconsiderados',
        'metodo', 'fundamento', 'hoje', 'situacao', 'dias_uteis_restantes', 'feriados_locais_confirmados', 'ato_reri',
        'alertas'}
# Semana sem feriados nem pontos facultativos: abertura numa segunda, data-limite na quarta anterior.
PLAIN_OPENING, PLAIN_LIMIT = date(2026, 3, 9), '2026-03-04'
LOCAL_UNKNOWN = 'feriados locais não informados: conferir o calendário do órgão (art. 183, III)'
LOCAL_NONE = 'analista confirmou que não há feriado local no período'
RERI_ALERT = 'a data de abertura pode ter mudado: conferir no processo da RERI'


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = prazo.main([str(a) for a in args])
    return code, out.getvalue(), err.getvalue()


def ignored(result):
    return [(d['data'], d['tipo']) for d in result['dias_desconsiderados']]


def calendar_json(**sections):
    return json.dumps({'nacionais_fixos': [], 'nacionais_moveis': [], 'pontos_facultativos': [], **sections},
                      ensure_ascii=False)


def urgent(result):
    return [a for a in result['alertas'] if a.startswith('ATENÇÃO')]


class EasterTests(unittest.TestCase):
    def test_known_easter_sundays(self):
        expected = {2024: date(2024, 3, 31), 2025: date(2025, 4, 20), 2026: date(2026, 4, 5), 2027: date(2027, 3, 28)}
        for year, day in expected.items():
            self.assertEqual(easter(year), day)


class CalendarTests(unittest.TestCase):
    def test_default_calendar_has_national_and_facultative_days(self):
        self.assertEqual(len(CALENDAR['nacionais_fixos']), 9)
        self.assertEqual(len(CALENDAR['nacionais_moveis']), 1)
        self.assertEqual(len(CALENDAR['pontos_facultativos']), 7)
        self.assertIn('observacao', CALENDAR)
        days = closed_days(2026, CALENDAR)
        self.assertEqual(days[date(2026, 4, 3)], {'nome': 'Sexta-feira da Paixão', 'tipo': 'nacional'})
        self.assertEqual(days[date(2026, 6, 4)]['tipo'], 'ponto_facultativo')  # Corpus Christi
        self.assertEqual(days[date(2026, 12, 24)]['tipo'], 'ponto_facultativo')

    def test_black_consciousness_day_only_from_2024(self):
        self.assertNotIn(date(2023, 11, 20), closed_days(2023, CALENDAR))
        self.assertEqual(closed_days(2024, CALENDAR)[date(2024, 11, 20)]['tipo'], 'nacional')

    def test_local_holiday_overrides_facultative_day(self):
        days = closed_days(2026, CALENDAR, [(date(2026, 6, 4), 'Feriado municipal fictício'), (date(2027, 1, 2), 'x')])
        self.assertEqual(days[date(2026, 6, 4)], {'nome': 'Feriado municipal fictício', 'tipo': 'local'})
        self.assertNotIn(date(2027, 1, 2), days)

    def test_invalid_calendar_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'cal.json'
            path.write_text(calendar_json(nacionais_fixos=[{'nome': 'Sem data'}]), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'nacionais_fixos'):
                load_calendar(path)
            path.write_text('{', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'não é JSON válido'):
                load_calendar(path)
        with self.assertRaisesRegex(FileNotFoundError, 'calendário não encontrado'):
            load_calendar(Path(tmp) / 'nao-existe.json')


class DeadlineTests(unittest.TestCase):
    def test_monday_opening_counts_back_to_previous_wednesday(self):
        result = deadline(PLAIN_OPENING, calendar=CALENDAR)
        self.assertEqual(set(result), KEYS)
        self.assertEqual(result['data_limite'], PLAIN_LIMIT)
        self.assertEqual(result['data_limite_com_pontos_facultativos'], PLAIN_LIMIT)
        self.assertEqual(result['dias_desconsiderados'], [])
        self.assertEqual(result['fundamento'], ['EXT-LEI14133-ART164', 'EXT-LEI14133-ART183'])
        self.assertIn('exclui o próprio dia da abertura', result['metodo'])
        self.assertIsNone(result['hoje'])
        self.assertIsNone(result['situacao'])
        self.assertIsNone(result['dias_uteis_restantes'])
        self.assertIs(result['feriados_locais_confirmados'], False)
        self.assertIs(result['ato_reri'], False)
        json.dumps(result)

    def test_mandatory_alerts(self):
        alerts = ' | '.join(deadline(PLAIN_OPENING, calendar=CALENDAR)['alertas'])
        self.assertIn('conferir o horário-limite no edital', alerts)
        self.assertIn('feriados locais não informados: conferir o calendário do órgão (art. 183, III)', alerts)
        self.assertNotIn('ATENÇÃO', alerts)
        self.assertNotIn('pontos facultativos', alerts)

    def test_good_friday_inside_window(self):
        result = deadline(date(2026, 4, 6), calendar=CALENDAR)
        self.assertEqual(result['data_limite'], '2026-03-31')
        self.assertEqual(result['data_limite_com_pontos_facultativos'], '2026-03-31')
        self.assertEqual(result['dias_desconsiderados'],
                         [{'data': '2026-04-03', 'nome': 'Sexta-feira da Paixão', 'tipo': 'nacional'}])

    def test_carnival_makes_the_two_deadlines_differ(self):
        result = deadline(date(2026, 2, 19), calendar=CALENDAR)
        self.assertEqual(result['data_limite'], '2026-02-11')
        self.assertEqual(result['data_limite_com_pontos_facultativos'], '2026-02-16')
        self.assertEqual(ignored(result), [('2026-02-16', 'ponto_facultativo'), ('2026-02-17', 'ponto_facultativo'),
                                           ('2026-02-18', 'ponto_facultativo')])
        alert = next(a for a in result['alertas'] if 'pontos facultativos listados' in a)
        self.assertIn('11/02/2026', alert)
        self.assertIn('16/02/2026', alert)
        self.assertIn('Quarta-feira de Cinzas', alert)

    def test_black_consciousness_day_changes_the_count_from_2024(self):
        self.assertEqual(deadline(date(2023, 11, 21), calendar=CALENDAR)['data_limite'], '2023-11-16')
        result = deadline(date(2024, 11, 21), calendar=CALENDAR)
        self.assertEqual(result['data_limite'], '2024-11-14')
        self.assertEqual(ignored(result), [('2024-11-15', 'nacional'), ('2024-11-20', 'nacional')])

    def test_local_holiday(self):
        holidays = [(date(2026, 3, 6), 'Aniversário fictício')]
        result = deadline(PLAIN_OPENING, local_holidays=holidays, calendar=CALENDAR)
        self.assertEqual(result['data_limite'], '2026-03-03')
        self.assertEqual(result['data_limite_com_pontos_facultativos'], '2026-03-03')
        self.assertEqual(result['dias_desconsiderados'],
                         [{'data': '2026-03-06', 'nome': 'Aniversário fictício', 'tipo': 'local'}])
        self.assertFalse(any('feriados locais não informados' in a for a in result['alertas']))

    def test_local_holidays_accept_a_generator(self):
        holidays = ((date(2026, 3, 6), nome) for nome in ['Aniversário fictício'])
        result = deadline(PLAIN_OPENING, local_holidays=holidays, calendar=CALENDAR)
        self.assertEqual(result['data_limite'], '2026-03-03')

    def test_year_turn_uses_holidays_of_both_years(self):
        result = deadline(date(2026, 1, 5), calendar=CALENDAR)
        self.assertEqual(result['data_limite'], '2025-12-29')
        self.assertEqual(result['data_limite_com_pontos_facultativos'], '2025-12-30')
        self.assertEqual(ignored(result), [('2025-12-31', 'ponto_facultativo'), ('2026-01-01', 'nacional')])

    def test_custom_business_days_and_validation(self):
        self.assertEqual(deadline(PLAIN_OPENING, business_days=1, calendar=CALENDAR)['data_limite'], '2026-03-06')
        result = deadline(PLAIN_OPENING, business_days=5, calendar=CALENDAR)
        self.assertEqual(result['data_limite'], '2026-03-02')
        self.assertIn('O 5º dia com expediente', result['metodo'])
        with self.assertRaises(ValueError):
            deadline(PLAIN_OPENING, business_days=0, calendar=CALENDAR)

    def test_opening_on_closed_day_is_flagged(self):
        alerts = deadline(date(2026, 4, 3), calendar=CALENDAR)['alertas']
        self.assertTrue(any('cai em dia sem expediente (Sexta-feira da Paixão' in a for a in alerts))
        alerts = deadline(date(2026, 3, 7), calendar=CALENDAR)['alertas']
        self.assertTrue(any('cai em dia sem expediente (sábado)' in a for a in alerts))

    def test_situation_with_today(self):
        cases = [(date(2026, 2, 20), 'no_prazo', 8, False), (date(2026, 3, 2), 'no_prazo', 2, True),
                 (date(2026, 3, 4), 'ultimo_dia', 0, True), (date(2026, 3, 5), 'vencido', 0, True)]
        for today, status, remaining, highlighted in cases:
            with self.subTest(today=today):
                result = deadline(PLAIN_OPENING, today=today, calendar=CALENDAR)
                self.assertEqual(result['hoje'], today.isoformat())
                self.assertEqual(result['situacao'], status)
                self.assertEqual(result['dias_uteis_restantes'], remaining)
                self.assertEqual(any(a.startswith('ATENÇÃO') for a in result['alertas']), highlighted)

    def test_remaining_days_skip_weekend_and_holidays(self):
        result = deadline(date(2026, 1, 5), today=date(2025, 12, 24), calendar=CALENDAR)
        # Depois de 24/12: 25 (Natal), 26 (sexta), 27-28 (fim de semana), 29 (data-limite).
        self.assertEqual(result['dias_uteis_restantes'], 2)
        self.assertEqual(result['situacao'], 'no_prazo')

    def test_expired_only_under_conservative_date(self):
        result = deadline(date(2026, 2, 19), today=date(2026, 2, 13), calendar=CALENDAR)
        self.assertEqual(result['situacao'], 'vencido')
        alert = next(a for a in result['alertas'] if a.startswith('ATENÇÃO'))
        self.assertIn('até 16/02/2026 se o órgão tiver expediente nos pontos facultativos', alert)


class CliTests(unittest.TestCase):
    def test_json_output(self):
        code, out, err = run('--abertura', '2026-04-06', '--hoje', '2026-03-30', '--feriado-local',
                             '2026-04-02:Feriado fictício', '--json')
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertEqual(set(result), KEYS)
        self.assertEqual(result['data_limite'], '2026-03-30')
        self.assertEqual(result['situacao'], 'ultimo_dia')
        self.assertIn({'data': '2026-04-02', 'nome': 'Feriado fictício', 'tipo': 'local'},
                      result['dias_desconsiderados'])

    def test_readable_summary(self):
        code, out, _ = run('--abertura', '2026-02-19', '--feriado-local', '2026-02-12')
        self.assertEqual(code, 0)
        self.assertIn('Data-limite para impugnar ou pedir esclarecimento: 10/02/2026 (terça-feira)', out)
        self.assertIn('Data-limite se houver expediente nos pontos facultativos: 16/02/2026 (segunda-feira)', out)
        self.assertIn('12/02/2026 (quinta-feira): feriado local (feriado local)', out)
        self.assertIn('Situação não calculada', out)
        self.assertIn('Analista confirmou que não há feriado local no período: não', out)
        self.assertIn('Ato da RERI no material: não', out)
        self.assertIn('Alertas:', out)

    def test_invalid_dates_exit_with_1(self):
        for args in (['--abertura', '2026-02-30'], ['--abertura', '06/04/2026'], ['--abertura', '20260406'],
                     ['--abertura', '2026-04-06', '--hoje', 'ontem'],
                     ['--abertura', '2026-04-06', '--feriado-local', '2026-13-01:x']):
            with self.subTest(args=args):
                code, out, err = run(*args)
                self.assertEqual(code, 1)
                self.assertEqual(out, '')
                self.assertTrue(err.startswith('erro: data inválida'), err)

    def test_invalid_business_days_and_calendar_exit_with_1(self):
        code, _, err = run('--abertura', '2026-04-06', '--dias', '0')
        self.assertEqual(code, 1)
        self.assertIn('pelo menos 1', err)
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = run('--abertura', '2026-04-06', '--calendario', Path(tmp) / 'x.json')
        self.assertEqual(code, 1)
        self.assertIn('calendário não encontrado', err)

    def test_custom_calendar_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'cal.json'
            path.write_text(calendar_json(nacionais_fixos=[{'mes': 3, 'dia': 6, 'nome': 'Feriado de teste'}]),
                            encoding='utf-8')
            code, out, _ = run('--abertura', '2026-03-09', '--calendario', path, '--json')
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)['data_limite'], '2026-03-03')

    def test_calendar_errors_exit_with_1_in_portuguese(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'cal.json'
            for content, expected in (('{}', 'falta a seção "nacionais_fixos"'),
                                      (calendar_json(nacionais_fixos=[{'mes': 2, 'dia': 30, 'nome': 'X'}]),
                                       'nacionais_fixos[0] tem dia 30 no mês 2'),
                                      ('[' * 200000, 'aninhamento profundo demais')):
                with self.subTest(expected=expected):
                    path.write_text(content, encoding='utf-8')
                    code, out, err = run('--abertura', '2026-03-09', '--calendario', path, '--json')
                    self.assertEqual(code, 1)
                    self.assertEqual(out, '')
                    self.assertTrue(err.startswith(f'erro: calendário {path}'), err)
                    self.assertIn(expected, err)

    def test_count_out_of_supported_dates_exits_with_1(self):
        for args in (['--abertura', '0001-01-03'], ['--abertura', '0001-01-10', '--dias', '30']):
            with self.subTest(args=args):
                code, out, err = run(*args)
                self.assertEqual(code, 1)
                self.assertEqual(out, '')
                self.assertTrue(err.startswith('erro: a contagem saiu do intervalo de datas suportado'), err)

    def test_repeated_local_holiday_is_listed_once(self):
        code, out, err = run('--abertura', '2026-03-09', '--feriado-local', '2026-03-06:A', '--feriado-local',
                             '2026-03-06:A', '--json')
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)['dias_desconsiderados'],
                         [{'data': '2026-03-06', 'nome': 'A', 'tipo': 'local'}])


class CalendarValidationTests(unittest.TestCase):
    def load(self, content, encoding='utf-8'):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'cal.json'
            path.write_bytes(content.encode(encoding) if isinstance(content, str) else content)
            return load_calendar(path)

    def assert_rejected(self, content, *expected):
        with self.assertRaises(ValueError) as caught:
            self.load(content)
        message = str(caught.exception)
        self.assertTrue(message.startswith('calendário '), message)
        for text in expected:
            self.assertIn(text, message)

    def test_misspelled_or_missing_section_is_rejected(self):
        content = json.dumps({'nacionais_fixo': [], 'nacionais_moveis': [], 'pontos_facultativos': []})
        self.assert_rejected(content, 'seção desconhecida "nacionais_fixo"', 'nacionais_fixos')
        self.assert_rejected('{}', 'falta a seção "nacionais_fixos"')
        self.assert_rejected(json.dumps({'nacionais_fixos': [], 'nacionais_moveis': []}),
                             'falta a seção "pontos_facultativos"')
        self.assert_rejected(calendar_json(nacionais_moveis={}), '"nacionais_moveis" deve ser uma lista')
        self.assertEqual(self.load(calendar_json(observacao='nota'))['observacao'], 'nota')

    def test_bad_entries_are_rejected_with_section_and_index(self):
        cases = [
            (dict(nacionais_fixos=[{'mes': True, 'dia': 6, 'nome': 'X'}]), 'nacionais_fixos[0] tem mes true'),
            (dict(nacionais_fixos=[{'mes': 1, 'dia': True, 'nome': 'X'}]), 'nacionais_fixos[0] tem dia true'),
            (dict(nacionais_fixos=[{'mes': 1, 'dia': 1, 'nome': 'A'}, {'mes': 13, 'dia': 1, 'nome': 'X'}]),
             'nacionais_fixos[1] tem mes 13; use 1 a 12'),
            (dict(nacionais_fixos=[{'mes': 2, 'dia': 30, 'nome': 'X'}]), 'nacionais_fixos[0] tem dia 30 no mês 2'),
            (dict(nacionais_fixos=[{'mes': 4, 'dia': 31, 'nome': 'X'}]), 'nacionais_fixos[0] tem dia 31 no mês 4'),
            (dict(nacionais_fixos=[{'mes': 11, 'dia': 20, 'nome': 'X', 'desde': '2024'}]),
             'nacionais_fixos[0] tem desde "2024"'),
            (dict(nacionais_fixos=[{'mes': 11, 'dia': 20, 'nome': 'X', 'desde': None}]),
             'nacionais_fixos[0] tem desde null'),
            (dict(nacionais_fixos=[{'mes': 11, 'nome': 'X'}]), 'nacionais_fixos[0] precisa de "mes" e "dia"'),
            (dict(nacionais_moveis=[{'offset_pascoa': 290, 'nome': 'X'}]), 'nacionais_moveis[0] tem offset_pascoa 290'),
            (dict(nacionais_moveis=[{'offset_pascoa': -81, 'nome': 'X'}]), 'use um inteiro de -80 a 250'),
            (dict(nacionais_moveis=[{'offset_pascoa': 10 ** 10, 'nome': 'X'}]), 'nacionais_moveis[0] tem offset'),
            (dict(pontos_facultativos=[{'offset_pascoa': False, 'nome': 'X'}]),
             'pontos_facultativos[0] tem offset_pascoa false'),
            (dict(pontos_facultativos=['X']), 'pontos_facultativos[0] deve ser um objeto'),
        ]
        for sections, expected in cases:
            with self.subTest(expected=expected):
                self.assert_rejected(calendar_json(**sections), expected)

    def test_offsets_at_the_limits_stay_in_the_year(self):
        # Páscoa mais cedo (22/03/2285) e mais tarde (25/04/2038): os limites caem em 01/01 e 31/12.
        calendar = self.load(calendar_json(nacionais_moveis=[{'offset_pascoa': -80, 'nome': 'Início'},
                                                             {'offset_pascoa': 250, 'nome': 'Fim'}]))
        self.assertIn(date(2285, 1, 1), closed_days(2285, calendar))
        self.assertIn(date(2038, 12, 31), closed_days(2038, calendar))

    def test_non_utf8_file_is_rejected_and_bom_is_accepted(self):
        content = calendar_json(nacionais_fixos=[{'mes': 1, 'dia': 1, 'nome': 'Confraternização'}])
        self.assert_rejected(content.encode('latin-1'), 'não está em UTF-8')
        self.assertEqual(self.load(content, 'utf-8-sig')['nacionais_fixos'][0]['nome'], 'Confraternização')

    def test_deeply_nested_json_is_rejected(self):
        self.assert_rejected('[' * 200000, 'não é JSON válido: aninhamento profundo demais')

    def test_february_29_counts_only_in_leap_years(self):
        calendar = self.load(calendar_json(nacionais_fixos=[{'mes': 2, 'dia': 29, 'nome': 'Feriado de teste'}]))
        self.assertEqual(closed_days(2028, calendar),
                         {date(2028, 2, 29): {'nome': 'Feriado de teste', 'tipo': 'nacional'}})
        self.assertEqual(closed_days(2026, calendar), {})
        self.assertEqual(deadline(date(2028, 3, 2), calendar=calendar)['data_limite'], '2028-02-25')
        self.assertEqual(deadline(date(2026, 3, 9), today=date(2025, 12, 1), calendar=calendar)['data_limite'],
                         PLAIN_LIMIT)


class ReviewFixTests(unittest.TestCase):
    def test_count_beyond_supported_dates_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, 'intervalo de datas suportado'):
            deadline(date(1, 1, 3), calendar=CALENDAR)

    def test_urgency_alerts_name_the_reference_date_not_today(self):
        # O resultado fica gravado no estado e é relido em outra data: o texto não pode depender de quando é lido.
        cases = [(date(2026, 3, 2), 'da data de referência (02/03/2026) até a data-limite (04/03/2026), há só 2'),
                 (date(2026, 3, 4), 'a data de referência (04/03/2026) é o último dia'),
                 (date(2026, 3, 5), 'prazo vencido na data de referência (05/03/2026)')]
        for today, expected in cases:
            with self.subTest(today=today):
                alerts = urgent(deadline(PLAIN_OPENING, today=today, calendar=CALENDAR))
                self.assertEqual(len(alerts), 1)
                self.assertIn(expected, alerts[0])
                self.assertNotIn('hoje', alerts[0])
                self.assertNotIn('restam', alerts[0])

    def test_local_holiday_from_another_year_keeps_the_local_alert(self):
        result = deadline(PLAIN_OPENING, local_holidays=[(date(2025, 3, 6), 'Feriado fictício')], calendar=CALENDAR)
        self.assertEqual(result['data_limite'], PLAIN_LIMIT)
        alerts = ' | '.join(result['alertas'])
        self.assertIn('feriados locais não informados', alerts)
        self.assertIn('feriados locais de ano fora da contagem (2026) não alteraram o prazo: '
                      '06/03/2025 Feriado fictício; conferir o ano', alerts)

    def test_local_holidays_of_both_years_of_a_year_turn_count_as_informed(self):
        holidays = [(date(2025, 12, 30), 'Feriado fictício'), (date(2026, 1, 2), 'Outro feriado fictício')]
        result = deadline(date(2026, 1, 7), local_holidays=holidays, calendar=CALENDAR)
        self.assertFalse(any('feriados locais' in a for a in result['alertas']))
        result = deadline(date(2026, 1, 7), local_holidays=holidays + [(date(2027, 1, 4), 'X')], calendar=CALENDAR)
        self.assertIn('feriados locais de ano fora da contagem (2025 e 2026) não alteraram o prazo: 04/01/2027 X; '
                      'conferir o ano', result['alertas'])

    def test_local_holiday_names_are_nfc_and_not_repeated(self):
        nfd = unicodedata.normalize('NFD', 'Aniversário fictício')
        holidays = [(date(2026, 3, 6), nfd), (date(2026, 3, 6), 'Aniversário fictício')]
        result = deadline(PLAIN_OPENING, local_holidays=holidays, calendar=CALENDAR)
        self.assertEqual(result['dias_desconsiderados'],
                         [{'data': '2026-03-06', 'nome': 'Aniversário fictício', 'tipo': 'local'}])
        self.assertTrue(unicodedata.is_normalized('NFC', result['dias_desconsiderados'][0]['nome']))
        days = closed_days(2026, CALENDAR, [(date(2026, 3, 6), 'A'), (date(2026, 3, 6), 'A'), (date(2026, 3, 6), 'B')])
        self.assertEqual(days[date(2026, 3, 6)]['nome'], 'A / B')


class ConfirmationOptionTests(unittest.TestCase):
    def test_no_local_holiday_replaces_the_local_alert(self):
        result = deadline(PLAIN_OPENING, calendar=CALENDAR, no_local_holidays=True)
        self.assertEqual(result['data_limite'], PLAIN_LIMIT)
        self.assertIs(result['feriados_locais_confirmados'], True)
        self.assertIs(result['ato_reri'], False)
        self.assertIn(LOCAL_NONE, result['alertas'])
        self.assertNotIn(LOCAL_UNKNOWN, result['alertas'])
        self.assertNotIn(RERI_ALERT, result['alertas'])

    def test_no_local_holiday_option_in_json_and_summary(self):
        code, out, err = run('--abertura', PLAIN_OPENING, '--sem-feriado-local', '--json')
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertEqual(set(result), KEYS)
        self.assertIs(result['feriados_locais_confirmados'], True)
        self.assertIs(result['ato_reri'], False)
        self.assertEqual(result['alertas'][1:], [LOCAL_NONE])
        code, out, err = run('--abertura', PLAIN_OPENING, '--sem-feriado-local')
        self.assertEqual(code, 0, err)
        self.assertIn('Analista confirmou que não há feriado local no período: sim', out)
        self.assertIn('Ato da RERI no material: não', out)
        self.assertIn(f'  - {LOCAL_NONE}', out)
        self.assertNotIn('feriados locais não informados', out)

    def test_reri_act_adds_its_alert_and_keeps_the_local_one(self):
        result = deadline(PLAIN_OPENING, calendar=CALENDAR, reri_act=True)
        self.assertEqual(result['data_limite'], PLAIN_LIMIT)
        self.assertIs(result['ato_reri'], True)
        self.assertIs(result['feriados_locais_confirmados'], False)
        self.assertEqual(result['alertas'].count(RERI_ALERT), 1)
        self.assertIn(LOCAL_UNKNOWN, result['alertas'])
        self.assertNotIn(LOCAL_NONE, result['alertas'])

    def test_reri_act_option_in_json_and_summary(self):
        code, out, err = run('--abertura', PLAIN_OPENING, '--feriado-local', '2026-03-06:Feriado fictício',
                             '--ato-reri', '--json')
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertIs(result['ato_reri'], True)
        self.assertIs(result['feriados_locais_confirmados'], False)
        self.assertEqual(result['data_limite'], '2026-03-03')
        self.assertIn(RERI_ALERT, result['alertas'])
        self.assertFalse(any('feriados locais' in a or 'feriado local' in a for a in result['alertas']))
        code, out, err = run('--abertura', PLAIN_OPENING, '--ato-reri')
        self.assertEqual(code, 0, err)
        self.assertIn('Ato da RERI no material: sim', out)
        self.assertIn('Analista confirmou que não há feriado local no período: não', out)
        self.assertIn(f'  - {RERI_ALERT}', out)

    def test_both_options_together_keep_urgency_last(self):
        code, out, err = run('--abertura', PLAIN_OPENING, '--hoje', '2026-03-03', '--sem-feriado-local', '--ato-reri',
                             '--json')
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertIs(result['feriados_locais_confirmados'], True)
        self.assertIs(result['ato_reri'], True)
        alerts = result['alertas']
        self.assertEqual(alerts[1:3], [LOCAL_NONE, RERI_ALERT])
        self.assertNotIn(LOCAL_UNKNOWN, alerts)
        self.assertEqual(len(alerts), 4)
        self.assertTrue(alerts[-1].startswith('ATENÇÃO'), alerts)
        code, out, err = run('--abertura', PLAIN_OPENING, '--sem-feriado-local', '--ato-reri')
        self.assertEqual(code, 0, err)
        self.assertIn('Analista confirmou que não há feriado local no período: sim', out)
        self.assertIn('Ato da RERI no material: sim', out)

    def test_no_local_holiday_conflicts_with_informed_local_holiday(self):
        for holiday in ('2026-03-06:Feriado fictício', '2025-03-06:Feriado de outro ano'):
            with self.subTest(holiday=holiday):
                code, out, err = run('--abertura', PLAIN_OPENING, '--sem-feriado-local', '--feriado-local', holiday,
                                     '--json')
                self.assertEqual(code, 1)
                self.assertEqual(out, '')
                self.assertTrue(err.startswith('erro: --feriado-local e --sem-feriado-local se excluem'), err)
                self.assertIn('só --sem-feriado-local se o analista confirmou', err)
        with self.assertRaisesRegex(ValueError, 'se excluem'):
            deadline(PLAIN_OPENING, local_holidays=[(date(2026, 3, 6), 'X')], calendar=CALENDAR,
                     no_local_holidays=True)


if __name__ == '__main__':
    unittest.main()
