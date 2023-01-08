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
    # The main function, returns formatted data.
    return format_data(check_data())


def check_data():
    try:
        # Opening JSON file if it's exists.
        with open(RATES_FILE, encoding='utf8') as json_f:
            data = json.load(json_f)
        logging.info(f"{RATES_FILE} found successfully.")
    except FileNotFoundError:
        # Launching scraping if file doesn't exists.
        logging.error(f"{RATES_FILE} not found!")
        return scrap_data()
    if data['metadata']['date'] == str(date.today()):
        # Checking if the data in the JSON file is up to date.
        logging.info("Data in the file is up to date.")
        return data['content']
    else:
        # If data in the file is outdated launching scraping.
        logging.warning("Data in the file is outdated.")
        return scrap_data()


def scrap_data():
    # Returns 'raw' data: dictionary with currencies and exchange rates
    # along with the metadata (date and number of entries).
    # Making request to the site using 'User-Agent' from an external file.
    response = requests.get(URL, headers={"User-Agent": config('USER_AGENT')})
    # Using beautifulsoup4 and 'lxml' parser to handle the response data.
    soup = BeautifulSoup(response.text, 'lxml')
    if str(soup.find('title').text)[:20] == 'Курсы валют ПС «Мир»':
        # Checking if the data from website is correct.
        logging.info('The website responded correctly.')
    else:
        logging.warning('The response from the website was incorrect.')
        return None
    # Finding the tag, which contains target data (exchange rates).
    items = soup.find('tbody')
    # Extracting list of currencies and exchange rates.
    currencies = items.find_all('p', style='text-align: left;')
    rates = items.find_all('p', style='text-align: center;')
    # Preparing en empty dict for data.
    content = {}
    for i in range(1, len(currencies)):
        # Working from item #1, because items #0 contain headlines.
        currency = currencies[i].text.strip()
        rate = rates[i].text.strip().replace(',', '.')
        content[currency] = rate
    if len(content) == CURRENCIES_NUMBER:
        # Checking if the number of extracted currencies is correct.
        logging.info('Executed data is correct.')
    else:
        logging.warning('Executed data in incorrect.')
        return None
    # Generating metadata dict for storing additional information.
    metadata = {
        'date': str(date.today()),
        'number of items': len(content),
    }
    data = {
        'metadata': metadata,
        'content': content,
    }
    # Dumping data to the JSON file.
    with open(RATES_FILE, 'w', encoding='utf8') as json_f:
        json.dump(data, json_f, indent=2, ensure_ascii=False)
        logging.info(f'Data is successfully dumped to the {RATES_FILE}.')
    return content


def format_data(raw_data):
    if raw_data is None:
        # In case of function was called with None argument returning error.
        return 'Сайт ПС Мир не отвечает или возвращает некорректные данные\\.'
    formatted_message = '*Курсы валют актуальны на:* '
    formatted_message += str(date.today()).replace('-', '\\-') + '\n'
    for currency, rate in raw_data.items():
        # Calculating and rounding the inversed exchange rate (1 / x).
        inversed_rate = str(round(1 / float(rate), 4)).replace('.', '\\.')
        # Rounding the exchange rate.
        rate = str(round(float(rate), 4)).replace('.', '\\.')
        # Adding whitespaces to the strings, so all strings will have
        # the same width and the message will look better with monospace font.
        currency = currency + ' ' * (CURRENCY_LENGHT - len(currency))
        rate = rate + ' ' * (RATE_LENGHT - len(rate))
        formatted_message += f'`\n{currency}: {rate} \\| {inversed_rate}`'
    return f"{formatted_message}"
