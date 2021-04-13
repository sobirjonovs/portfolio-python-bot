from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

fsm = MemoryStorage()
bot: Bot = Bot(token="1783680365:AAGXuo2xlp8pME6ELng1xGuWerDpIQuXDXw", parse_mode='HTML')
dp = Dispatcher(bot, storage=fsm)
