from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

fsm = MemoryStorage()
bot: Bot = Bot(token="TOKEN", parse_mode='HTML')
dp = Dispatcher(bot, storage=fsm)
