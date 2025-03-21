from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import settings
from queries.models import Base

# Создание асинхронного подключения к базе данных с использованием PostgreSQL
engine = create_async_engine(settings.database_url_asyncpg, echo=False)

# Создание сессии для асинхронных операций с базой данных
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_table():
    """
        Создает все таблицы в базе данных, если они еще не созданы, на основе моделей,
        определенных в файле 'queries/models.py'. Для выполнения используется асинхронное соединение.
        """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_table():
    """Удаляет все таблицы из базы данных, которые были ранее созданы."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
