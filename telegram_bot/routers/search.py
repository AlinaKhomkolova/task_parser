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
    async with session_maker() as db:
        return db


db_session = asyncio.run(get_session())
problem = ProblemsQueries(db_session=db_session)


@router.message(F.text == "🔍 Поиск задач")
async def search(message: Message, state: FSMContext):
    tags = await problem.get_tags()
    keyboard = create_keyboard(tags)

    await state.set_state(SearchState.waiting_for_tags)
    await message.answer("📚Выберите тему:", reply_markup=keyboard)


@router.message(SearchState.waiting_for_tags)
async def search__by_tags(message: Message, state: FSMContext):
    await state.update_data(waiting_for_tags=message.text)

    state_data = await state.get_data()

    ratings = await problem.get_rating(state_data.get('waiting_for_tags'))
    keyboard = create_keyboard(ratings)

    await state.set_state(SearchState.waiting_for_rating)
    await message.answer("⚖️ Выберите сложность:", reply_markup=keyboard)


@router.message(SearchState.waiting_for_rating)
async def search_by_rating(message: Message, state: FSMContext):
    await state.update_data(waiting_for_rating=message.text)
    state_data = await state.get_data()
    tag_name = state_data.get('waiting_for_tags')
    rating = int(state_data.get('waiting_for_rating'))

    data_problems = await problem.get_problem_to_criteria(tag_name=tag_name, rating=rating)

    await message.answer('🔍Начинаю поиск задач')
    if not data_problems:
        await message.answer('❌Задач по такой теме и сложности нет\n'
                             '🔄Попробуй еще раз /start')
        await state.clear()
        return

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
        await message.answer(problem_text)
        count += 1

    await state.clear()
