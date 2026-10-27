#!/usr/bin/env python3
"""Calcula a data-limite para impugnar ou pedir esclarecimento (Lei 14.133, arts. 164 e 183). Python 3.10+.

Conta para trás a partir da abertura, só em dias com expediente. Só alerta; nunca bloqueia.
Os feriados nacionais e pontos facultativos ficam em feriados.json, ao lado do script.

Uso:
  prazo.py --abertura 2026-04-06                            resumo legível
  prazo.py --abertura 2026-04-06 --hoje 2026-03-30 --json   resultado em JSON (para "estado.py prazo --dados -")
  prazo.py --abertura 2026-04-06 --feriado-local 2026-04-02:Aniversário da cidade
  prazo.py --abertura 2026-04-06 --sem-feriado-local        o analista confirmou que não há feriado local no período
  prazo.py --abertura 2026-04-06 --ato-reri                 há ato da RERI no material: a abertura pode ter mudado

--feriado-local (repetido para cada feriado) e --sem-feriado-local se excluem. Num recálculo, repita todas as
opções: o registro novo substitui o anterior no estado.
"""
import argparse
import json
import re
import sys
import unicodedata
from datetime import date, timedelta
from functools import partial
from pathlib import Path

DEFAULT_CALENDAR = Path(__file__).resolve().parent / 'feriados.json'
FOUNDATION = ['EXT-LEI14133-ART164', 'EXT-LEI14133-ART183']
SECTIONS = {'nacionais_fixos': 'nacional', 'nacionais_moveis': 'nacional', 'pontos_facultativos': 'ponto_facultativo'}
# A Páscoa cai entre 22/03 e 25/04: com estes deslocamentos, a data nunca sai do ano (fora disso, sumiria da contagem).
EASTER_OFFSETS = range(-80, 251)
# Em datas coincidentes vale o tipo mais forte: feriado local fecha o órgão mesmo num ponto facultativo.
RANK = {'ponto_facultativo': 0, 'local': 1, 'nacional': 2}
KINDS = {'nacional': 'feriado nacional', 'local': 'feriado local', 'ponto_facultativo': 'ponto facultativo'}
SITUATIONS = {'no_prazo': 'no prazo', 'ultimo_dia': 'último dia', 'vencido': 'vencido'}
WEEKDAYS = ('segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo')
ISO_DATE = re.compile(r'\d{4}-\d{2}-\d{2}')
LOCAL_UNKNOWN = 'feriados locais não informados: conferir o calendário do órgão (art. 183, III)'
LOCAL_NONE = 'analista confirmou que não há feriado local no período'
RERI_ALERT = 'a data de abertura pode ter mudado: conferir no processo da RERI'
LOCAL_CONFLICT = ('--feriado-local e --sem-feriado-local se excluem: use --feriado-local AAAA-MM-DD:nome para cada '
                  'feriado local informado, ou só --sem-feriado-local se o analista confirmou que não há nenhum no '
                  'período')


def easter(year):
    """Domingo de Páscoa pelo algoritmo gregoriano anônimo (Meeus/Jones/Butcher)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    n = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * n) // 451
    month, day = divmod(h + n - 7 * m + 114, 31)
    return date(year, month, day + 1)


def is_int(value):
    return type(value) is int  # bool é subclasse de int: true no JSON não pode virar mês 1


def show(value):
    return json.dumps(value, ensure_ascii=False)


def entry_problem(entry):
    """Motivo pelo qual o item do calendário é inválido, ou None."""
    if not isinstance(entry, dict):
        return 'deve ser um objeto com nome e data (mes e dia, ou offset_pascoa)'
    if not isinstance(entry.get('nome'), str):
        return 'precisa de "nome" em texto'
    if 'desde' in entry and not is_int(entry['desde']):
        return f'tem desde {show(entry["desde"])}; use o ano como número inteiro, por exemplo 2024'
    if 'offset_pascoa' in entry:
        offset = entry['offset_pascoa']
        if is_int(offset) and offset in EASTER_OFFSETS:
            return None
        return (f'tem offset_pascoa {show(offset)}; use um inteiro de {EASTER_OFFSETS[0]} a {EASTER_OFFSETS[-1]} '
                '(dias contados do Domingo de Páscoa, sem sair do ano)')
    if 'mes' not in entry or 'dia' not in entry:
        return 'precisa de "mes" e "dia", ou de "offset_pascoa"'
    month, day = entry['mes'], entry['dia']
    if not is_int(month) or not 1 <= month <= 12:
        return f'tem mes {show(month)}; use 1 a 12'
    if not is_int(day):
        return f'tem dia {show(day)}; use um número inteiro'
    try:
        date(2000, month, day)  # ano bissexto: 29/02 passa e vale só nos anos bissextos
    except ValueError:
        return f'tem dia {day} no mês {month}, data que não existe'
    return None


def calendar_problem(calendar):
    if not isinstance(calendar, dict):
        return f'o conteúdo deve ser um objeto JSON com as seções {", ".join(SECTIONS)}'
    unknown = [key for key in calendar if key not in SECTIONS and key != 'observacao']
    if unknown:
        return f'seção desconhecida {show(unknown[0])}; use {", ".join(SECTIONS)} ou observacao'
    for section in SECTIONS:
        if section not in calendar:
            return f'falta a seção "{section}" (use [] se ela não tiver itens)'
        if not isinstance(calendar[section], list):
            return f'"{section}" deve ser uma lista'
        for index, entry in enumerate(calendar[section]):
            problem = entry_problem(entry)
            if problem:
                return f'{section}[{index}] {problem}'
    return None


def load_calendar(path=None):
    path = Path(path) if path else DEFAULT_CALENDAR
    if not path.is_file():
        raise FileNotFoundError(f'calendário não encontrado: {path}')
    try:
        text = path.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        raise ValueError(f'calendário {path} não está em UTF-8: salve o arquivo nessa codificação') from None
    try:
        calendar = json.loads(text)
    except RecursionError:
        raise ValueError(f'calendário {path} não é JSON válido: aninhamento profundo demais') from None
    except ValueError as exc:
        raise ValueError(f'calendário {path} não é JSON válido: {exc}') from None
    problem = calendar_problem(calendar)
    if problem:
        raise ValueError(f'calendário {path}: {problem}')
    return calendar


def entry_date(entry, year, easter_day):
    if 'offset_pascoa' in entry:
        return easter_day + timedelta(days=entry['offset_pascoa'])
    try:
        return date(year, entry['mes'], entry['dia'])
    except ValueError:
        return None  # 29/02 em ano não bissexto


def mark(days, day, name, kind):
    current = days.get(day)
    if current is None or RANK[kind] > RANK[current['tipo']]:
        days[day] = {'nome': name, 'tipo': kind}
    elif RANK[kind] == RANK[current['tipo']] and name not in current['nome'].split(' / '):
        current['nome'] += f' / {name}'


def closed_days(year, calendar, local_holidays=()):
    """Dias sem expediente do ano, fora os fins de semana: {date: {'nome', 'tipo'}}."""
    days, easter_day = {}, easter(year)
    for section, kind in SECTIONS.items():
        for entry in calendar.get(section, []):
            day = entry_date(entry, year, easter_day)
            if day and year >= entry.get('desde', year):
                mark(days, day, entry['nome'], kind)
    for day, name in local_holidays:
        if day.year == year:
            mark(days, day, name, 'local')
    return days


def closed_lookup(calendar, local_holidays):
    """Consulta por data, montando o calendário de cada ano na primeira vez (a janela pode virar o ano)."""
    years = {}

    def lookup(day):
        if day.year not in years:
            years[day.year] = closed_days(day.year, calendar, local_holidays)
        return years[day.year].get(day)
    return lookup


def is_open(day, lookup, facultative_open=False):
    if day.weekday() >= 5:
        return False
    info = lookup(day)
    return info is None or (facultative_open and info['tipo'] == 'ponto_facultativo')


def count_back(opening, business_days, open_day):
    day, found = opening, 0
    while found < business_days:
        day -= timedelta(days=1)
        found += open_day(day)
    return day


def days_between(start, end):
    """Dias depois de start e antes de end."""
    return [start + timedelta(days=i) for i in range(1, (end - start).days)]


def count_open(today, limit, open_day):
    """Dias com expediente depois de hoje até a data-limite, inclusive."""
    return sum(open_day(today + timedelta(days=i)) for i in range(1, (limit - today).days + 1))


def situation(today, limit):
    if today is None:
        return None
    if today < limit:
        return 'no_prazo'
    return 'ultimo_dia' if today == limit else 'vencido'


def method(business_days):
    return (f'Contagem regressiva (art. 183): parte da data de abertura, exclui o próprio dia da abertura e conta '
            'para trás só os dias com expediente, pulando sábados, domingos, feriados nacionais e feriados locais '
            'informados. Na data_limite, os pontos facultativos também são pulados (dia sem expediente); na '
            f'data_limite_com_pontos_facultativos, eles contam como dias com expediente. O {business_days}º dia com '
            f'expediente encontrado é o último dia para protocolar (art. 164: até {business_days} dias úteis antes '
            'da abertura).')


def br(iso):
    return f'{date.fromisoformat(iso):%d/%m/%Y}'


def long_date(iso):
    return f'{br(iso)} ({WEEKDAYS[date.fromisoformat(iso).weekday()]})'


def days_label(count):
    return f'{count} dia útil' if count == 1 else f'{count} dias úteis'


def closed_reason(day, lookup):
    if day.weekday() >= 5:
        return WEEKDAYS[day.weekday()]
    info = lookup(day)
    return f"{info['nome']}, {KINDS[info['tipo']]}" if info else None


def urgency(result):
    # Estes textos ficam gravados no estado e são relidos depois: citam a data de referência, nunca "hoje".
    status, limit = result['situacao'], br(result['data_limite'])
    lenient = result['data_limite_com_pontos_facultativos']
    if status == 'vencido':
        text = (f"ATENÇÃO: prazo vencido na data de referência ({br(result['hoje'])}); o último dia para protocolar "
                f'foi {limit}')
        if result['hoje'] <= lenient:
            text += f'; só cabe protocolar até {br(lenient)} se o órgão tiver expediente nos pontos facultativos'
        return [text]
    if status == 'ultimo_dia':
        return [f'ATENÇÃO: a data de referência ({limit}) é o último dia para protocolar']
    if status == 'no_prazo' and result['dias_uteis_restantes'] <= 2:
        return [f"ATENÇÃO: da data de referência ({br(result['hoje'])}) até a data-limite ({limit}), há só "
                f"{days_label(result['dias_uteis_restantes'])}"]
    return []


def local_alerts(result, has_local):
    if result['feriados_locais_confirmados']:
        return [LOCAL_NONE]
    return [] if has_local else [LOCAL_UNKNOWN]


def alerts(result, opening_closed, has_local, other_year):
    items = ['conferir o horário-limite no edital: ele pode fixar hora para o protocolo no último dia']
    items += local_alerts(result, has_local)
    if other_year:
        first, last = result['data_limite'][:4], result['abertura'][:4]
        span = first if first == last else f'{first} e {last}'
        listed = '; '.join(f'{day:%d/%m/%Y} {name}' for day, name in other_year)
        items.append(f'feriados locais de ano fora da contagem ({span}) não alteraram o prazo: {listed}; '
                     'conferir o ano')
    limit, lenient = result['data_limite'], result['data_limite_com_pontos_facultativos']
    if limit != lenient:
        names = '; '.join(f"{br(d['data'])} {d['nome']}" for d in result['dias_desconsiderados']
                          if d['tipo'] == 'ponto_facultativo')
        items.append(f'a data-limite depende do expediente nos pontos facultativos listados ({names}): '
                     f'{br(limit)} se o órgão não tiver expediente neles, {br(lenient)} se tiver; '
                     'na dúvida, vale a data mais cedo')
    if opening_closed:
        items.append(f"a abertura ({br(result['abertura'])}) cai em dia sem expediente ({opening_closed}): "
                     'conferir a data no edital e se houve retificação')
    if result['ato_reri']:
        items.append(RERI_ALERT)
    return items + urgency(result)


def deadline(opening, business_days=3, local_holidays=(), today=None, calendar=None, *, no_local_holidays=False,
             reri_act=False):
    """no_local_holidays: o analista confirmou que não há feriado local no período; reri_act: há ato da RERI."""
    if business_days < 1:
        raise ValueError(f'o número de dias úteis deve ser pelo menos 1 (recebido: {business_days})')
    # Sem repetição e em NFC: num recálculo a lista pode voltar inteira, e o nome pode vir colado em NFD.
    local_holidays = tuple(dict.fromkeys((day, unicodedata.normalize('NFC', name)) for day, name in local_holidays))
    if no_local_holidays and local_holidays:
        raise ValueError(LOCAL_CONFLICT)
    lookup = closed_lookup(load_calendar() if calendar is None else calendar, local_holidays)
    strict = partial(is_open, lookup=lookup)
    try:
        limit = count_back(opening, business_days, strict)
        lenient = count_back(opening, business_days, partial(is_open, lookup=lookup, facultative_open=True))
    except OverflowError:
        raise ValueError('a contagem saiu do intervalo de datas suportado: confira a abertura e o número de dias '
                         'úteis') from None
    result = {
        'abertura': opening.isoformat(),
        'dias_uteis': business_days,
        'data_limite': limit.isoformat(),
        'data_limite_com_pontos_facultativos': lenient.isoformat(),
        'dias_desconsiderados': [{'data': day.isoformat(), 'nome': info['nome'], 'tipo': info['tipo']}
                                 for day in days_between(limit, opening)
                                 if day.weekday() < 5 and (info := lookup(day))],
        'metodo': method(business_days),
        'fundamento': list(FOUNDATION),
        'hoje': today.isoformat() if today is not None else None,
        'situacao': situation(today, limit),
        'dias_uteis_restantes': count_open(today, limit, strict) if today is not None else None,
        'feriados_locais_confirmados': bool(no_local_holidays),
        'ato_reri': bool(reri_act),
    }
    years = range(limit.year, opening.year + 1)
    other_year = [(day, name) for day, name in local_holidays if day.year not in years]
    has_local = len(other_year) < len(local_holidays)
    result['alertas'] = alerts(result, closed_reason(opening, lookup), has_local, other_year)
    return result


def yes_no(value):
    return 'sim' if value else 'não'


def summary(result):
    lines = [f"Abertura: {long_date(result['abertura'])}",
             f"Data-limite para impugnar ou pedir esclarecimento: {long_date(result['data_limite'])}"]
    if result['data_limite_com_pontos_facultativos'] != result['data_limite']:
        lines.append('Data-limite se houver expediente nos pontos facultativos: '
                     f"{long_date(result['data_limite_com_pontos_facultativos'])}")
    lines.append(f"Prazo: até {days_label(result['dias_uteis'])} antes da abertura ({', '.join(result['fundamento'])})")
    if result['dias_desconsiderados']:
        lines.append('Dias sem expediente pulados na contagem, além dos fins de semana:')
        lines += [f"  - {long_date(d['data'])}: {d['nome']} ({KINDS[d['tipo']]})"
                  for d in result['dias_desconsiderados']]
    if result['hoje']:
        lines.append(f"Hoje: {long_date(result['hoje'])}; situação: {SITUATIONS[result['situacao']]}; "
                     f"dias úteis restantes: {result['dias_uteis_restantes']}")
    else:
        lines.append('Situação não calculada: informe --hoje AAAA-MM-DD.')
    lines.append('Analista confirmou que não há feriado local no período: '
                 f"{yes_no(result['feriados_locais_confirmados'])}")
    lines.append(f"Ato da RERI no material: {yes_no(result['ato_reri'])}")
    lines.append(f"Método: {result['metodo']}")
    lines.append('Alertas:')
    lines += [f'  - {alert}' for alert in result['alertas']]
    return '\n'.join(lines)


def parse_date(text, option):
    error = ValueError(f'data inválida em {option}: "{text}" (use AAAA-MM-DD, por exemplo 2026-04-06)')
    if not ISO_DATE.fullmatch(text):
        raise error
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise error from None


def parse_local(text):
    day, _, name = text.partition(':')
    return parse_date(day.strip(), '--feriado-local'), name.strip() or 'feriado local'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--abertura', required=True, metavar='AAAA-MM-DD', help='data de abertura do certame')
    parser.add_argument('--feriado-local', action='append', default=[], metavar='AAAA-MM-DD[:nome]',
                        help='feriado estadual ou municipal do órgão; repita a opção para cada um')
    parser.add_argument('--sem-feriado-local', action='store_true',
                        help='o analista confirmou que não há feriado local no período (exclui --feriado-local)')
    parser.add_argument('--ato-reri', action='store_true',
                        help='há ato da RERI no material: alerta que a data de abertura pode ter mudado')
    parser.add_argument('--hoje', metavar='AAAA-MM-DD', help='data de referência para a situação do prazo')
    parser.add_argument('--calendario', type=Path, metavar='ARQUIVO.json',
                        help='JSON de feriados (padrão: feriados.json ao lado do script)')
    parser.add_argument('--dias', type=int, default=3, metavar='N',
                        help='dias úteis antes da abertura (padrão: 3, art. 164)')
    parser.add_argument('--json', action='store_true', help='imprime o resultado em JSON')
    args = parser.parse_args(argv)
    try:
        opening = parse_date(args.abertura, '--abertura')
        today = parse_date(args.hoje, '--hoje') if args.hoje is not None else None
        local_holidays = [parse_local(item) for item in args.feriado_local]
        result = deadline(opening, args.dias, local_holidays, today, load_calendar(args.calendario),
                          no_local_holidays=args.sem_feriado_local, reri_act=args.ato_reri)
    except (OSError, ValueError, TypeError) as exc:
        print(f'erro: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else summary(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
