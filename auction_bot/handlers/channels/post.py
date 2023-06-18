import logging

from aiogram import types
from loader import dp

@dp.channel_post_handler(content_types=types.ContentTypes.ANY)
async def new_post(message: types.Message):
    logging.info(f'Опубликовано новое сообщение в канале {message.chat.title}.\nmessage.text')
