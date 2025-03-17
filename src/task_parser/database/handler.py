from typing import Optional

import asyncpg
from psycopg2 import Error, OperationalError


class DatabaseHandler:
    """Отвечает за подключение к базе данных и выполнение SQL-запросов."""

    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        """Устанавливает соединение с базой данных"""
        try:
            dsn = f"postgresql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['dbname']}"
            self.conn = await asyncpg.connect(dsn)
            print('Подключение к базе данных успешно')
        except OperationalError as e:
            print(f'Ошибка подключения к базе данных: {e}')

    async def close(self):
        """Закрывает соединение с базой данных"""
        if self.conn:
            await self.conn.close()
            print('Соединение с базой данных закрыто')

    async def execute_query(self, query: str, params: Optional[tuple] = None):
        """Выполняет SQL-запрос без возврата данных (INSERT, UPDATE, DELETE)."""
        try:
            await self.conn.execute(query, *params)
            # self.conn.commit()
        except Error as e:
            # self.conn.rollback()
            print(f"Ошибка выполнения запроса: {e}")

    async def fetch_query(self, query: str, params: Optional[tuple] = None):
        """Выполняет SQL-запрос и возвращает данные (SELECT)."""
        try:
            if params is None:
                params = ()
            result = await self.conn.fetch(query, *params)
            return result
        except Exception as e:
            print(f"Ошибка выполнения SELECT-запроса: {e}")
            return []

    async def fetch_one(self, query: str, params: Optional[tuple] = None):
        """Выполняет SQL-запрос и возвращает одну запись."""
        try:
            result = await self.conn.fetchrow(query, *params)
            return result
        except Exception as e:
            print(f"Ошибка выполнения SELECT-запроса: {e}")
            return None
