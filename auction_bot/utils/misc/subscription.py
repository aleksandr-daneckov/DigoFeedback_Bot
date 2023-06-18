from typing import Union

from aiogram import Bot


async  def check(user_id, channel: Union[int, str], member=None):
    bot = Bot.get_current()
    await  bot.get_chat_member(chat_id=channel, user_id=user_id)
    return member.is_chat_member()