from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.helper import HelperMode


class ProjectState(StatesGroup):
    mode = HelperMode.lowercase

    NAME = State()
    DESCRIPTION = State()
    IMAGE = State()
    URL = State()
