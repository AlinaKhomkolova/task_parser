from aiogram.fsm.state import State, StatesGroup


class SearchState(StatesGroup):
    """Класс состояний для управления процессом поиска задач."""
    waiting_for_tags = State()
    waiting_for_rating = State()
