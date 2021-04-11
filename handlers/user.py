from pathlib import Path

from aiogram.types import InlineKeyboardMarkup as inline_markup, InlineKeyboardButton as inline_button, \
    ReplyKeyboardRemove, ChatActions
from aiogram.dispatcher.filters import CommandStart, Text
from loader import dp, bot
from aiogram import types
from middlewares.localisation import __
from queries import db
from config import admins

_ = __


@dp.message_handler(CommandStart())
async def entry(message: types.message):
    user = types.User.get_current()
    params = {
        'columns': {
            'chat_id': message.chat.id,
            'name': message.chat.first_name
        },
        'condition': {
            "chat_id": message.chat.id
        }
    }
    db.insertOrUpdate(table='users', params=params)
    translated_text = __(
        "<b>Assalomu alaykum! Xush kelibsiz!</b> \nSobirjonov Sanjarbek'ning portfolio botiga xush kelibsiz."
    )

    inline_keyboard = inline_markup(
        inline_keyboard=[
            [
                inline_button(text=_("🎯 Ko'nikmalar"), callback_data='skills'),
                inline_button(text=_("🏫 Ma'lumoti"), callback_data='degree'),
            ],
            [
                inline_button(text=_("💻 Ishlari"), callback_data='projects_0'),
                inline_button(text=_("🇺🇿 Tillar"), callback_data='langs'),
            ],
            [
                inline_button(text=_("✅ Status"), callback_data='status'),
                inline_button(text=_("😎 Haqimda"), callback_data='about_me'),
            ],
            [
                inline_button(text=_("⚙️ Tilni almashtirish"), callback_data='change_lang'),
                inline_button(text=_("👮️ Admin panel"), callback_data='admin_panel')
            ] if user.id in admins else [inline_button(text=_("⚙️ Tilni almashtirish"), callback_data='change_lang'), ]
        ]
    )
    await message.answer_chat_action(ChatActions.TYPING)
    await message.answer(translated_text, reply_markup=inline_keyboard)


@dp.callback_query_handler(text='change_lang')
async def languages(callback: types.CallbackQuery):
    languages_list = inline_markup(
        inline_keyboard=[
            [
                inline_button(text="🇺🇿 O'zbekcha", callback_data='uz'),
                inline_button(text="🇷🇺 Русский", callback_data='ru'),
                inline_button(text="🇬🇧 English", callback_data='en')
            ]
        ]
    )
    page = _("— Bo'lim")
    text = f'<b>{page}</b>' + ": " + _("⚙️ Tilni almashtirish")
    await callback.message.answer(text=text, reply_markup=languages_list)


@dp.callback_query_handler(Text(equals=['uz', 'ru', 'en']))
async def set_language(callback: types.CallbackQuery):
    db.update(table='users',
              params={'columns': {'lang': callback.data}, 'condition': {'chat_id': callback.message.chat.id}})
    await callback.answer("OK")


@dp.callback_query_handler(text="status")
async def showStatus(callback: types.CallbackQuery):
    status = db.select(table='users', what="status", condition={'chat_id': admins[0]}, one=True)
    await callback.answer(status['status'])


@dp.callback_query_handler(Text(contains="projects"))
async def projects(callback: types.CallbackQuery):
    page_data = callback.data.split('_')[1]
    offset = 1
    project = db.select(table='projects', limit=f"{page_data},{offset}", one=True)
    projects = db.select(table='projects', what="COUNT(*) as count", one=True)
    path = Path(__file__).parent.parent.joinpath("images/project_images")
    pagination = inline_markup()
    next_p = 1
    next_p += int(page_data)
    current = (next_p + 1) - 1
    indicator = f"{current} / {projects['count']}"
    if next_p >= projects['count']:
        next_p = int(page_data)

    pagination.row_width = 3
    page = _("— Bo'lim")
    text = f'<b>{page}</b>' + ": " + _("💻 Ishlari")
    if project is not None:
        pagination.add(
            inline_button(text="♻️", callback_data=f"projects_0"),
            inline_button(text=indicator, callback_data="indicator"),
            inline_button(text=">", callback_data=f"projects_{next_p}"),
            inline_button(text=__('🔙 Orqaga'), callback_data="back"),
            inline_button(text=f"🔗 {_('Havola')}", url=project['url'])
        )
        text += f"\n\n<b>• {_('Nomi')}:</b> {project['name']}\n<b>• {_('Tavsifi')}:</b> {project['description']}\n<b>• {_('Havola')}:</b> {project['url']}\n"

        await callback.message.answer_photo(
            photo=open(path / project['image'], 'rb'),
            caption=text,
            reply_markup=pagination
        )
    else:
        await callback.message.delete()
        text += f"\n\n{_('Topilmadi')}"
        pagination.add(
            inline_button(text=__('🔙 Orqaga'), callback_data="back")
        )
        await callback.message.answer(text, reply_markup=pagination)


@dp.callback_query_handler(text="skills")
async def skills(callback: types.CallbackQuery):
    about_text = db.select(table='users', what="skills", condition={'chat_id': admins[0]}, one=True)
    await callback.message.delete()
    back = inline_markup(
        inline_keyboard=[
            [
                inline_button(text=__('🔙 Orqaga'), callback_data="back")
            ]
        ]
    )
    page = _("— Bo'lim")
    text = f'<b>{page}</b>' + ": " + _("🎯 Ko'nikmalar")
    await callback.message.answer(text=f"{text}\n\n{__('Topilmadi') if about_text['skills'] is None else about_text['skills']}", reply_markup=back)


@dp.callback_query_handler(text="degree")
async def skills(callback: types.CallbackQuery):
    about_text = db.select(table='users', what="degree", condition={'chat_id': admins[0]}, one=True)
    await callback.message.delete()
    back = inline_markup(
        inline_keyboard=[
            [
                inline_button(text=__('🔙 Orqaga'), callback_data="back")
            ]
        ]
    )
    page = _("— Bo'lim")
    text = f'<b>{page}</b>' + ": " + _("🏫 Ma'lumoti")
    await callback.message.answer(text=f"{text}\n\n{__('Topilmadi') if about_text['degree'] is None else about_text['degree']}", reply_markup=back)


@dp.callback_query_handler(text="about_me")
async def about(callback: types.CallbackQuery):
    about_text = db.select(table='users', what="about", condition={'chat_id': admins[0]}, one=True)
    await callback.message.delete()
    back = inline_markup(
        inline_keyboard=[
            [
                inline_button(text=__('🔙 Orqaga'), callback_data="back")
            ]
        ]
    )
    page = _("— Bo'lim")
    text = f'<b>{page}</b>' + ": " + _("😎 Haqimda")
    await callback.message.answer(text=f"{text}\n\n{__('Topilmadi') if about_text['about'] is None else about_text['about']}", reply_markup=back)


@dp.callback_query_handler(text="langs")
async def about(callback: types.CallbackQuery):
    about_text = db.select(table='users', what="langs", condition={'chat_id': admins[0]}, one=True)
    await callback.message.delete()
    back = inline_markup(
        inline_keyboard=[
            [
                inline_button(text=__('🔙 Orqaga'), callback_data="back")
            ]
        ]
    )
    page = _("— Bo'lim")
    text = f'<b>{page}</b>' + ": " + _("🇺🇿 Tillar")
    await callback.message.answer(text=f"{text}\n\n{__('Topilmadi') if about_text['langs'] is None else about_text['langs']}", reply_markup=back)


@dp.callback_query_handler(text="back")
async def back(callback: types.CallbackQuery):
    await callback.message.delete()
    return await entry(callback.message)

