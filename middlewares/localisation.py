from pathlib import Path
from typing import Tuple, Any

from aiogram import types
from babel import Locale

from loader import dp
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from queries import db

domain = 'portfolio'
base_path = Path(__file__).parent.parent
locale_path = base_path.joinpath('locales')


class LanguageMiddleware(I18nMiddleware):
    async def get_user_locale(self, action, message) -> str:
        user = types.User.get_current()
        user_lang = db.select(table='users', what='lang', condition={"chat_id": user['id']})
        if user_lang and user_lang[0]['lang'] is not None:
            return user_lang[0]['lang']
        else:
            return user['language_code']


i18n = LanguageMiddleware(domain=domain, path=locale_path)
dp.setup_middleware(i18n)

__ = i18n.gettext
