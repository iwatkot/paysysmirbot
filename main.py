import asyncio
import json
import logging
import aiocron
import sys

from aiogram import Bot, Dispatcher, executor, types
from decouple import config

from script import get_rates
from script import scrap_data

LOG_FILE = 'logs/main_log.txt'
MESSAGES_FILE = 'templates/messages.json'
TOKEN = config('TOKEN')

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# Loading messages templates from JSON file.
with open(MESSAGES_FILE, encoding='utf8') as json_f:
    messages = json.load(json_f)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@aiocron.crontab('0 */3 * * *')
async def update_data():
    logging.info('Starting scheduled data update.')
    scrap_data()


def write_log(message, user_id, user_name):
    # Writes an entry of user interaction to the log file.
    logging.info(f"{message['text']} user_id:{user_id} user_name:{user_name}")


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    # Handles the '/start' command.
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    write_log(message, user_id, user_name)
    # Sending welcome message to the user (with reply).
    await message.reply(messages['WELCOME_MSG'].format(user_name))
    rates = get_rates()
    await asyncio.sleep(2)
    # Sending message with exchange rates.
    await bot.send_message(user_id, rates, parse_mode='MarkdownV2')
    await asyncio.sleep(3)
    # Sending messages with tips about other commands (/rates, /notify).
    await bot.send_message(user_id, messages['USE_RATES_MSG'])
    await asyncio.sleep(3)
    await bot.send_message(user_id, messages['USE_NOTIFY_MSG'])


@dp.message_handler(commands=["rates"])
async def rates_handler(message: types.Message):
    # Handles the '/rates' command.
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    write_log(message, user_id, user_name)
    rates = get_rates()
    # Sending message with exchange rates.
    await bot.send_message(user_id, rates, parse_mode='MarkdownV2')


if __name__ == "__main__":
    executor.start_polling(dp)
