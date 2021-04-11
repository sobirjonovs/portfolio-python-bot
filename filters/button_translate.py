from aiogram import types
from localize import _
from aiogram.dispatcher.filters import BoundFilter


class ButtonTranslate(BoundFilter):
    def __init__(self, key):
        self.key = key

    async def check(self, message: types.Message) -> bool:
        return _(self.key) == message.text


t = ButtonTranslate
