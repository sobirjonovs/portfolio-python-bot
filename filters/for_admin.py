from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from config import admins


class Admin(BoundFilter):
    async def check(self, message):
        user_id = message.chat.id if hasattr(message, 'chat') else message.message.chat.id
        return user_id in admins
