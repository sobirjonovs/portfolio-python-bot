from aiogram.utils import executor
from handlers.user import dp, bot, db, admins
from handlers import admin


async def on_startup(dispatcher):
    db.create(table='users', id="int AUTO_INCREMENT PRIMARY KEY", name="VARCHAR(255) DEFAULT NULL",
              chat_id="VARCHAR(255)", phone="VARCHAR(255) DEFAULT NULL", status="VARCHAR(255) DEFAULT NULL", lang="VARCHAR(255) DEFAULT NULL",
              degree="varchar(255) default null", about="varchar(255)", blocked="int(2) default 0", skills="text null", langs='varchar(255) null'
              )
    db.create(table='projects', id="int AUTO_INCREMENT PRIMARY KEY",
              name="varchar(255) not null", description="text not null", image="varchar(255) null", url="varchar(255) null"
              )
    for admin in admins:
        await bot.send_message(chat_id=admin, text="Bot ishga tushdi")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
