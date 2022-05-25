from aiogram import executor
from handlers import dp

from utils.settings.notify_admins import on_startup_notify
from utils.settings.set_bot_commands import set_default_commands

async def on_startup(dp):
    await on_startup_notify(dp)

    await set_default_commands(dp)

    print('Бот в сети')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
