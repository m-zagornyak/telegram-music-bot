from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart

#from data.config import CHANNEL_ID
#from keyboards.inline import ikb_menu
from loader import (
    dp, 
    bot, 
    check_sub_channel)


@dp.message_handler(CommandStart())
async def help_start(message: types.Message):
 #   if message.chat.type == 'private':
  #      if check_sub_channel(await bot.get_chat_member(user_id=message.from_user.id)):
      #      await message.answer("Вы не подписались на канал", reply_markup=ikb_menu)
 #       else:
            await message.answer(
                f"✋ Приветствою\n📨 Вы можете прислать боту ссылки на\n 🎶 Youtube/Youtube Music🔗 видео\n🧾 По вопросам"
                f"сотруднечесвту к @m_zagornyak\n 🔒 ",
                )
            
"""
@dp.callback_query_handler(text='subchannel')
async def sub_channel_done(message: types.Message, call: CallbackQuery):
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        await call.message.answer(
            f"✋ Приветствою\n📨 Вы можете прислать боту ссылки на\n 🎶 Youtube/Youtube Music видео\n🧾 По вопросам "
            f"сотруднечесвту к @m_zagornyak\n 🔒 Чтобы пользоваться ботом\n 🛎 Подпишись на канал",
            reply_markup=ikb_menu)
    else:
        await call.message.answer("Вы не подписались на канал", reply_markup=ikb_menu)
"""