from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_manager = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎁 Создать лот"),
            KeyboardButton(text="🗂 Мои лоты")
        ],
        [
            KeyboardButton(text="⚙ Настройки"),
            KeyboardButton(text="🙋‍♂️ Помощь")
        ],
        [
            KeyboardButton(text="➕ Добавить лоты"),
            KeyboardButton(text="👥 Кол-во пользователей")
        ]
    ],
    resize_keyboard=True
)