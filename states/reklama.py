from aiogram.dispatcher.filters.state import StatesGroup, State


class ADV(StatesGroup):
    image = State()
    content = State()
    confirm = State()
