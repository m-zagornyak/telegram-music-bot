from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Помощь')
        ]   
    ],
    resize_keyboard=True
    
)