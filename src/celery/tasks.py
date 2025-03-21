import asyncio
from asyncio import Lock

from config import settings
from queries.engine import session_maker
from src.celery.celery import app
from src.task_parser.api.client import APIClient
from src.task_parser.processors.problem_processor import ProblemProcessor

task_lock = Lock()


@app.task
def fetch_codeforces_data():
    """Парсит данные с Codeforces и обрабатывает их"""
    print('Начинаю выполнение задачи')
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(fetch_data())
    else:
        loop.run_until_complete(fetch_data())


async def fetch_data():
    """Асинхронная логика для выполнения задачи"""
    if task_lock.locked():
        print("Задача все еще выполняется")
        return  # Пропускаем выполнение задачи, если предыдущая еще не завершена.

    async with task_lock:
        try:
            await process()  # Выполнение задачи
            print("Задача выполнена успешно.")
        except Exception as e:
            print(f"Ошибка в задаче fetch_codeforces_data: {e}")


async def process():
    """Основная логика обработки данных"""
    print("Создаю сессию с БД...")
    async with session_maker() as db_session:
        print("Сессия создана!")
        dsn = settings.url_for_parser
        api = APIClient(dsn)
        problem = ProblemProcessor(db_session=db_session, api_client=api)
        await problem.save_tags()
        await problem.save_problems()
        await problem.save_problem_statistics()
        await problem.save_problem_tags()
