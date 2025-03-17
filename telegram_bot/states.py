from aiogram.fsm.state import State, StatesGroup


class SearchState(StatesGroup):
    waiting_for_tags = State()
    waiting_for_rating = State()
