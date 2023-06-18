from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Обращение"),
            KeyboardButton(text="Сотрудничать")
        ]
    ],
    resize_keyboard=True
)

