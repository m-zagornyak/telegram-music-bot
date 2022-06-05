from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from data.config import CHANNEL_ID

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Канал', url="https://t.me/channel_musicsurf"),
                                        InlineKeyboardButton(text='Проверить', callback_data='subchannel')
                                    ]
                                ])
