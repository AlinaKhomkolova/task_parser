import logging
from typing import Optional

import asyncpg
from psycopg2 import Error, OperationalError

from src.task_parser.database.config import settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseHandler:
    """Отвечает за подключение к базе данных и выполнение SQL-запросов."""

    def __init__(self):
        # self.db_config = db_config
        self.conn = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        """Устанавливает соединение с базой данных"""
        try:
            dsn = await settings.database_url_postgres
            self.conn = await asyncpg.connect(dsn)
            logger.info('Подключение к базе данных успешно')
        except OperationalError as e:
            logger.error(f'Ошибка подключения к базе данных: {e}')

    async def close(self):
        """Закрывает соединение с базой данных"""
        if self.conn:
            await self.conn.close()
            logger.info('Соединение с базой данных закрыто')

    async def execute_query(self, query: str, params: Optional[tuple] = None):
        """Выполняет SQL-запрос без возврата данных (INSERT, UPDATE, DELETE)."""
        try:
            await self.conn.execute(query, *params)
        except Error as e:
            logger.error(f"Ошибка выполнения запроса: {e}")

    async def fetch_query(self, query: str, params: Optional[tuple] = None):
        """Выполняет SQL-запрос и возвращает данные (SELECT)."""
        try:
            if params is None:
                params = ()
            result = await self.conn.fetch(query, *params)
            return result
        except Exception as e:
            logger.error(f"Ошибка выполнения SELECT-запроса: {e}")
            return []

    async def fetch_one(self, query: str, params: Optional[tuple] = None):
        """Выполняет SQL-запрос и возвращает одну запись."""
        try:
            result = await self.conn.fetchrow(query, *params)
            return result
        except Exception as e:
            logger.error(f"Ошибка выполнения SELECT-запроса: {e}")
            return None
