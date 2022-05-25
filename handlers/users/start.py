from aiogram import types

from loader import dp, bot
from keyboards.inline import ikb_menu

@dp.message_handler(commands=['start', 'help'])
async def help_start(message: types.Message):
    await message.answer(f"✋ Приветствою\n📨 Вы можете прислать боту ссылки на\n 🎶 Youtube/Youtube Music🔗 видео\n🧾 По вопросам сотруднечесвту к @m_zagornyak\n 🔒 Чтобы пользоваться ботом\n 🛎 Подпишись на канал", reply_markup=ikb_menu)
    



"""@dp.message_handler(commands=['help', 'start'])
async def help_start(event: types.Message):
    bot_info = await bot.get_me()
    bot_name = bot_info.first_name.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
    bot_username = bot_info.username.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
    msg = "Hey, I'm *{}*\n".format(bot_name)
    msg += "_You can use me in inline mode :_\n"
    msg += "@{} \\(album\\|track\\|artist\\) \\<search\\>\n".format(bot_username)
    msg += "Or just send an *Deezer* album or track *link* \\!"
    await event.answer(msg, parse_mode="MarkdownV2")"""