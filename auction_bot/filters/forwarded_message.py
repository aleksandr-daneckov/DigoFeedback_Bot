from aiogram import types

from aiogram.dispatcher.filters import BoundFilter


class IsForwarded(BoundFilter):
    async  def check(self, message: types.message) -> bool:
        if message.forward_from_chat:
            return  message.forward_from_chat.type == types.ChatType.CHANNEL