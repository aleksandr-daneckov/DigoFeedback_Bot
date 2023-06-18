from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_close = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Закрыть ❌")
        ]
    ],
    resize_keyboard=True
)