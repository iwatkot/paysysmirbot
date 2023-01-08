import requests
import json

from bs4 import BeautifulSoup
from decouple import config

from datetime_handler import get_today
from logger import write_log

LOG_FILE = 'logs/scrap_log.txt'
RATES_FILE = 'data/rates.json'
CURRENCY_LENGHT = 20
CURRENCIES_NUMBER = 7
RATE_LENGHT = 12
URL = 'https://mironline.ru/support/list/kursy_mir/'


def get_rates():
    return format_data(check_data())


def check_data():
    today = get_today()
    try:
        with open(RATES_FILE, encoding='utf8') as json_f:
            data = json.load(json_f)
        write_log(LOG_FILE, 'FOUND', result="JSON-FILE-FOUND-AND-LOADED")
    except FileNotFoundError:
        write_log(LOG_FILE, 'ERROR', result="JSON-FILE-NOT-FOUND")
        return scrap_data()
    if data['metadata']['date'] == today:
        write_log(LOG_FILE, 'FRESH', result="THE-DATA-IS-NEW")
        return data['content']
    else:
        write_log(LOG_FILE, 'OLDDA', result="THE-DATA-NEEDS-UPDATE")
        return scrap_data()


def scrap_data():
    response = requests.get(URL, headers={"User-Agent": config('USER_AGENT')})
    soup = BeautifulSoup(response.text, 'lxml')
    if str(soup.find('title').text)[:20] == 'Курсы валют ПС «Мир»':
        write_log(LOG_FILE, 'GOODR', result='WEBSITE-RESPONDED-CORRECTLY')
    else:
        write_log(LOG_FILE, 'BADRE', result='WRONG-RESPONSE')
        return None
    items = soup.find('tbody')
    currencies = items.find_all('p', style='text-align: left;')
    rates = items.find_all('p', style='text-align: center;')
    content = {}
    for i in range(1, len(currencies)):
        currency = currencies[i].text.strip()
        rate = rates[i].text.strip().replace(',', '.')
        content[currency] = rate
    if len(content) == CURRENCIES_NUMBER:
        write_log(LOG_FILE, 'CORRD', result='DATA-IS-CORRECT')
    else:
        write_log(LOG_FILE, 'BADDA', result='WRONG-DATA')
        return None
    today = get_today()
    metadata = {
        'date': today,
        'number of items': len(content),
    }
    data = {
        'metadata': metadata,
        'content': content,
    }
    with open(RATES_FILE, 'w', encoding='utf8') as json_f:
        json.dump(data, json_f, indent=2, ensure_ascii=False)
        write_log(LOG_FILE, 'JDUMP', result='DATA-IS-DUMPED-TO-FILE')
    return content


def format_data(raw_data):
    if raw_data is None:
        return 'Сайт ПС Мир не отвечает или возвращает некорректные данные\\.'
    formatted_message = '*Курсы валют актуальны на:* '
    formatted_message += get_today().replace('-', '\\-') + '\n'
    for currency, rate in raw_data.items():
        inversed_rate = str(round(1 / float(rate), 4)).replace('.', '\\.')
        rate = rate.replace('.', '\\.')
        currency = currency + ' ' * (CURRENCY_LENGHT - len(currency))
        rate = rate + ' ' * (RATE_LENGHT - len(rate))
        formatted_message += f'`\n{currency}:  {rate} \\|  {inversed_rate}`'
    return f"{formatted_message}"
