import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from queries.engine import session_maker
from queries.problems_queries import ProblemsQueries
from telegram_bot.keyboards import create_keyboard
from telegram_bot.states import SearchState

router = Router()


async def get_session():
    """Асинхронная функция для получения сессии с базой данных."""
    async with session_maker() as db:
        return db


# Инициализация сессии базы данных и объекта запросов
db_session = asyncio.run(get_session())
problem = ProblemsQueries(db_session=db_session)


@router.message(F.text == "🔍 Поиск задач")
async def search(message: Message, state: FSMContext):
    """Обработчик команды для начала поиска задач по тегам."""
    # Получаем список всех тегов
    tags = await problem.get_tags()
    # Создаем клавиатуру для выбора тегов
    keyboard = create_keyboard(tags)

    # Устанавливаем состояние для ожидания выбора тега
    await state.set_state(SearchState.waiting_for_tags)
    await message.answer("📚Выберите тему:", reply_markup=keyboard)


@router.message(SearchState.waiting_for_tags)
async def search__by_tags(message: Message, state: FSMContext):
    """Обработчик выбора тега пользователем и переход к выбору сложности."""

    # Сохраняем выбранный тег
    await state.update_data(waiting_for_tags=message.text)

    # Получаем данные состояния
    state_data = await state.get_data()

    # Получаем возможные рейтинги для выбранного тега
    ratings = await problem.get_rating(state_data.get('waiting_for_tags'))
    # Создаем клавиатуру для выбора рейтинга
    keyboard = create_keyboard(ratings)

    # Устанавливаем состояние для ожидания выбора рейтинга
    await state.set_state(SearchState.waiting_for_rating)
    await message.answer("⚖️ Выберите сложность:", reply_markup=keyboard)


@router.message(SearchState.waiting_for_rating)
async def search_by_rating(message: Message, state: FSMContext):
    """Обработчик выбора рейтинга и поиск задач по заданным критериям."""

    # Сохраняем выбранный рейтинг
    await state.update_data(waiting_for_rating=message.text)

    # Получаем данные состояния
    state_data = await state.get_data()
    tag_name = state_data.get('waiting_for_tags')
    rating = int(state_data.get('waiting_for_rating'))

    # Ищем задачи по выбранным тегу и рейтингу
    data_problems = await problem.get_problem_to_criteria(tag_name=tag_name, rating=rating)
    # Отправляем сообщение о начале поиска
    await message.answer('🔍Начинаю поиск задач')

    # Если задачи не найдены, отправляем соответствующее сообщение
    if not data_problems:
        await message.answer('❌Задач по такой теме и сложности нет\n'
                             '🔄Попробуй еще раз /start')
        await state.clear()
        return
    # Отправляем найденные задачи(до 10 штук)
    count = 1
    for data_problem in data_problems:
        if count > 10:
            break

        problem_text = (f"{count})\n"
                        f"🔗 Ссылка: https://codeforces.com/problemset/problem/{data_problem['contest_id']}/{data_problem['index']}\n"
                        f"\n"
                        f"📝 Задача: {data_problem['name']}\n"
                        f"⚖️ Сложность: {data_problem['rating']}\n"
                        f"👥 Сколько раз ее решили: {data_problem['solved_count']}")
        # Отправляем информацию о задаче
        await message.answer(problem_text)
        count += 1

    # Очищаем состояние после завершения поиска
    await state.clear()
