import asyncio
import json

from aiogram import Bot, Dispatcher, executor, types
from decouple import config

from script import get_rates
from logger import write_log

LOG_FILE = 'logs/message_log.txt'
MESSAGES_FILE = 'templates/messages.json'
TOKEN = config('TOKEN')
with open(MESSAGES_FILE, encoding='utf8') as json_f:
    messages = json.load(json_f)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    write_log(LOG_FILE, 'START', user_id=user_id, user_name=user_name)
    await message.reply(messages['WELCOME_MSG'].format(user_name))
    rates = get_rates()
    await asyncio.sleep(1)
    await bot.send_message(user_id, rates, parse_mode='MarkdownV2')
    await asyncio.sleep(3)
    await bot.send_message(user_id, messages['USE_RATES_MSG'])
    await asyncio.sleep(3)
    await bot.send_message(user_id, messages['USE_NOTIFY_MSG'])


@dp.message_handler(commands=["rates"])
async def rates_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    write_log(LOG_FILE, 'RATES', user_id=user_id, user_name=user_name)
    rates = get_rates()
    await bot.send_message(user_id, rates, parse_mode='MarkdownV2')


@dp.message_handler(commands=["notify"])
async def notify_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    write_log(LOG_FILE, 'NOTIF', user_id=user_id, user_name=user_name)
    await message.reply(messages['SUBSCRIBED_MSG'])
    while True:
        await asyncio.sleep(60*60*24)
        rates = get_rates()
        await bot.send_message(user_id, rates, parse_mode='MarkdownV2')


if __name__ == "__main__":
    executor.start_polling(dp)
