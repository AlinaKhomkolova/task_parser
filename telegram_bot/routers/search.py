from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from settings import db_config
from src.task_parser.database.handler import DatabaseHandler
from telegram_bot.keyboards import create_keyboard
from telegram_bot.services.problems import Problems
from telegram_bot.states import SearchState

router = Router()

prob = Problems()


@router.message(F.text == "🔍 Поиск задач")
async def search(message: Message, state: FSMContext):
    tags = await prob.get_tags()
    keyboard = create_keyboard(tags)

    await state.set_state(SearchState.waiting_for_tags)
    await message.answer("📚Выберите тему:", reply_markup=keyboard)


@router.message(SearchState.waiting_for_tags)
async def search__by_tags(message: Message, state: FSMContext):
    await state.update_data(waiting_for_tags=message.text)

    state_data = await state.get_data()

    ratings = await prob.get_rating(state_data.get('waiting_for_tags'))
    keyboard = create_keyboard(ratings)

    await state.set_state(SearchState.waiting_for_rating)
    await message.answer("⚖️ Выберите сложность:", reply_markup=keyboard)


@router.message(SearchState.waiting_for_rating)
async def search_by_rating(message: Message, state: FSMContext):
    await state.update_data(waiting_for_rating=message.text)
    db = DatabaseHandler(db_config)
    state_data = await state.get_data()
    tag_name = state_data.get('waiting_for_tags')
    rating = int(state_data.get('waiting_for_rating'))

    data_problems = await Problems.get_problem_to_criteria(db=db, tag_name=tag_name, rating=rating)

    await message.answer('🔍Начинаю поиск задач')
    if data_problems:
        count = 1
        for data_problem in data_problems:
            if count == 11:
                break

            problem_text = (f"{count})\n"
                            f"🔗 Ссылка: https://codeforces.com/problemset/problem/{data_problem['contest_id']}/{data_problem['index']}\n"
                            f"\n"
                            f"📝 Задача: {data_problem['name']}\n"
                            f"⚖️ Сложность: {data_problem['rating']}\n"
                            f"👥 Сколько раз ее решили: {data_problem['solved_count']}")
            await message.answer(problem_text)

            count += 1
    else:
        await message.answer('❌Задач по такой теме и сложности нет\n'
                             '🔄Попробуй еще раз /start')
    await state.clear()
