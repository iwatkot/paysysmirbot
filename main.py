import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, executor, types
from decouple import config

from script import get_rates

LOG_FILE = 'logs/main_log.txt'
MESSAGES_FILE = 'templates/messages.json'
TOKEN = config('TOKEN')

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")

# Loading messages templates from JSON file.
with open(MESSAGES_FILE, encoding='utf8') as json_f:
    messages = json.load(json_f)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


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


@dp.message_handler(commands=["notify"])
async def notify_handler(message: types.Message):
    # Handles the '/notify' command.
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    write_log(message, user_id, user_name)
    # Sending message that user successfully subscribed to notifications.
    await message.reply(messages['SUBSCRIBED_MSG'])
    while True:
        # Waiting for 24 hours (in seconds).
        await asyncio.sleep(60*60*24)
        rates = get_rates()
        # Sending message with exchange rates.
        await bot.send_message(user_id, rates, parse_mode='MarkdownV2')


if __name__ == "__main__":
    executor.start_polling(dp)
