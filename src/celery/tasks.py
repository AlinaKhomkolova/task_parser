import asyncio

from src.celery.celery import app
from src.task_parser.api.client import APIClient
from src.task_parser.config import settings
from src.task_parser.database.handler import DatabaseHandler
from src.task_parser.processors.problem_processor import ProblemProcessor


@app.task
def fetch_codeforces_data():
    """Парсит данные с Codeforces и обрабатывает их"""
    try:
        async def process():
            db = DatabaseHandler()
            dsn = await settings.url_for_parser
            api = APIClient(dsn)
            problem = ProblemProcessor(db_handler=db, api_client=api)

            async with db:
                await problem.save_problems()
                await problem.save_tags()
                await problem.save_problem_statistics()
                await problem.save_problem_tags()

        asyncio.run(process())
        print("Задача выполнена успешно.")
    except Exception as e:
        print(f"Ошибка в задаче fetch_codeforces_data: {e}")
