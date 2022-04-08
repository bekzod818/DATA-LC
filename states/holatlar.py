from aiogram.dispatcher.filters.state import StatesGroup, State


class DATA(StatesGroup):
    category = State()
    course = State()
    about = State()
    teacher = State()
    about_teacher = State()