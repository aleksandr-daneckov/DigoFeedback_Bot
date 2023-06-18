from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Менеджеры"),
            KeyboardButton(text="Обращения")
        ],
        [
            KeyboardButton(text="Рассылка"),
            KeyboardButton(text="Ответить")
        ]
    ],
    resize_keyboard=True
)