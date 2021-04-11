import asyncio
from pathlib import Path

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BotBlocked, RetryAfter

from buttons.admin import keyboard
from filters.for_admin import Admin
from loader import dp, bot
from queries import db
from states.states import ProjectState


@dp.callback_query_handler(Admin(), text="admin_panel")
@dp.message_handler(Command('admin'), Admin())
async def admin_panel(message: types.Message or types.CallbackQuery):
    reply = message if isinstance(message, types.Message) else message.message
    await reply.answer("Assalomu alaykum, Sanjar! Xush kelibsiz. ", reply_markup=keyboard)


@dp.message_handler(text="📤 Ommaviy xabar")
async def message(message: types.message, state):
    await message.answer("Xabarni kiriting")
    await state.set_state('sending_message')


@dp.message_handler(text="✅ Status")
async def status(message: types.Message, state):
    await message.answer("Statusni yozib yuboring")
    await state.set_state('setting_status')


@dp.message_handler(text="📊 Statistika")
async def status(message: types.Message, state):
    users = db.select(table='users', what="COUNT(*) as count")[0]
    blockeds = db.select(table='users', what="COUNT(*) as count", condition={'blocked': 1})[0]
    text = f"<b>📊 Statistika</b>\n\n👥 Foydalanuvchilar: {users['count']}\n❌ Bloklaganlar: {blockeds['count']}"
    await message.answer(text)


@dp.message_handler(text="😎 About me")
async def about(message: types.Message, state):
    await message.answer("Aboutni kiriting")
    await state.set_state('about')


@dp.message_handler(state='about')
async def set_about(message: types.Message, state):
    db.update(table='users', params={'columns': {'about': message.text}, 'condition': {'chat_id': message.chat.id}})
    await message.answer("Saqlandi")
    await state.finish()


@dp.message_handler(text="🎯 Ko'nikmalar")
async def skills(message: types.Message, state):
    await message.answer("Ko'nikmalarni kiriting")
    await state.set_state('skill')


@dp.message_handler(state='skill')
async def add_skills(message: types.Message, state):
    db.update(table='users', params={'columns': {'skills': message.text}, 'condition': {'chat_id': message.chat.id}})
    await message.answer("Saqlandi")
    await state.finish()


@dp.message_handler(text="🇺🇿 Tillar")
async def langs(message: types.Message, state):
    await message.answer("Tillarni kiriting")
    await state.set_state('langs')


@dp.message_handler(state='langs')
async def set_langs(message: types.Message, state):
    db.update(table='users', params={'columns': {'langs': message.text}, 'condition': {'chat_id': message.chat.id}})
    await message.answer("Saqlandi")
    await state.finish()


@dp.message_handler(text="🏫 Daraja")
async def degree(message: types.Message, state):
    await message.answer("Ko'nikmalarni kiriting")
    await state.set_state('degree')


@dp.message_handler(state='degree')
async def set_degree(message: types.Message, state):
    db.update(table='users', params={'columns': {'degree': message.text}, 'condition': {'chat_id': message.chat.id}})
    await message.answer("Saqlandi")
    await state.finish()


@dp.message_handler(text="💻 Proyekt")
async def project(message: types.Message):
    await message.answer("Proyekt nomini kiriting")
    await ProjectState.first()


@dp.message_handler(state=ProjectState.NAME)
async def set_project_name(message: types.Message, state):
    await state.update_data({
        "name": message.text
    })
    await message.answer("Proyekt tavsifini kiriting")
    await ProjectState.next()


@dp.message_handler(state=ProjectState.DESCRIPTION)
async def set_project_description(message: types.Message, state):
    await state.update_data({
        "description": message.text
    })
    await message.answer("Proyekt rasmini kiriting")
    await ProjectState.next()


@dp.message_handler(state=ProjectState.IMAGE, content_types=types.ContentType.PHOTO)
async def set_project_image(message: types.Message, state):
    photo = message.photo[0]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    extension = Path(file.file_path).suffix
    image_name = f"{photo.file_unique_id}{extension}"
    await bot.download_file(file.file_path, f"images/project_images/{image_name}")
    await state.update_data({
        "image": image_name
    })
    await message.answer('URL ni kiriting')
    await ProjectState.next()


@dp.message_handler(state=ProjectState.URL)
async def set_project_description(message: types.Message, state):
    await state.update_data({
        "url": message.text
    })

    settings = await state.get_data()
    db.insert(table='projects', columns=settings.keys(), values=settings.values())
    await message.answer("Saqlandi")
    await state.finish()


@dp.message_handler(state="sending_message")
async def send_message(message, state):
    users = db.select(table='users')
    for u_id, user in enumerate(users):
        try:
            await bot.send_message(chat_id=user['chat_id'], text=message.text)
        except BotBlocked:
            db.update(table='users', params={'columns': {'blocked': 1}, 'condition': {'chat_id': user['chat_id']}})
            continue
        except RetryAfter:
            continue

    return await state.finish()


@dp.message_handler(state="setting_status")
async def set_status(message: types.message, state):
    user_status = message.text
    db.update(table='users', params={'columns': {'status': user_status},
                                     'condition': {'chat_id': message.chat.id}
                                     })
    await message.answer("Status o'rnatildi")
    await state.finish()
