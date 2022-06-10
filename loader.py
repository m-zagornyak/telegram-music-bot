import os
import json

from aiogram import (
    Bot,
    types,
    Dispatcher
)

from data.config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)

LANGS_FILE = json.load(open(r'utils/langs.json'))
LANG = os.environ.get('BOT_LANG')

dp = Dispatcher(bot)

try:
    os.mkdir("tmp")
except FileExistsError:
    pass

try:
    os.mkdir("tmp/yt/")
except FileExistsError:
    pass


def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False

