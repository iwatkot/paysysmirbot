import requests
import json
import logging

from bs4 import BeautifulSoup
from decouple import config

from datetime import date

RATES_FILE = 'data/rates.json'
CURRENCY_LENGHT = 20
CURRENCIES_NUMBER = 7
RATE_LENGHT = 8
URL = 'https://mironline.ru/support/list/kursy_mir/'


def get_rates():
    return format_data(check_data())


def check_data():
    try:
        with open(RATES_FILE, encoding='utf8') as json_f:
            data = json.load(json_f)
        logging.info(f"{RATES_FILE} found successfully.")
    except FileNotFoundError:
        logging.error(f"{RATES_FILE} not found!")
        return scrap_data()
    if data['metadata']['date'] == str(date.today()):
        logging.info("Data in the file is up to date.")
        return data['content']
    else:
        logging.warning("Data in the file is outdated.")
        return scrap_data()


def scrap_data():
    response = requests.get(URL, headers={"User-Agent": config('USER_AGENT')})
    soup = BeautifulSoup(response.text, 'lxml')
    if str(soup.find('title').text)[:20] == 'Курсы валют ПС «Мир»':
        logging.info('The website responded correctly.')
    else:
        logging.warning('The response from the website was incorrect.')
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
        logging.info('Executed data is correct.')
    else:
        logging.warning('Executed data in incorrect.')
        return None
    metadata = {
        'date': str(date.today()),
        'number of items': len(content),
    }
    data = {
        'metadata': metadata,
        'content': content,
    }
    with open(RATES_FILE, 'w', encoding='utf8') as json_f:
        json.dump(data, json_f, indent=2, ensure_ascii=False)
        logging.info(f'Data is successfully dumped to the {RATES_FILE}.')
    return content


def format_data(raw_data):
    if raw_data is None:
        return 'Сайт ПС Мир не отвечает или возвращает некорректные данные\\.'
    formatted_message = '*Курсы валют актуальны на:* '
    formatted_message += str(date.today()).replace('-', '\\-') + '\n'
    for currency, rate in raw_data.items():
        inversed_rate = str(round(1 / float(rate), 4)).replace('.', '\\.')
        rate = str(round(float(rate), 4)).replace('.', '\\.')
        currency = currency + ' ' * (CURRENCY_LENGHT - len(currency))
        rate = rate + ' ' * (RATE_LENGHT - len(rate))
        formatted_message += f'`\n{currency}: {rate} \\| {inversed_rate}`'
    return f"{formatted_message}"
