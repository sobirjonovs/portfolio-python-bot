from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

fsm = MemoryStorage()
bot: Bot = Bot(token="1743968934:AAEVSxDotf3R7Sf0oD-_5XLGFXQtLDvsi9E", parse_mode='HTML')
dp = Dispatcher(bot, storage=fsm)
