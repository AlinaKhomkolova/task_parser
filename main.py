import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from queries.engine import create_table
from telegram_bot.routers import register_routers


async def get_token():
    dsn = settings.token_for_bot
    bot = Bot(token=dsn)
    return bot


storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def start_celery():
    # asyncio для асинхронного запуска процессов Celery
    process_worker = await asyncio.create_subprocess_exec(
        'celery', '-A', 'src.celery.tasks', 'worker', '--loglevel=info', '-n', 'worker@%h'
    )
    process_beat = await asyncio.create_subprocess_exec(
        'celery', '-A', 'src.celery.tasks', 'beat', '--loglevel=info'
    )


async def start_bot():
    register_routers(dp)
    # await drop_table()
    await create_table()
    await dp.start_polling(await get_token())


# Запуск Celery и бота одновременно
async def main():
    # Запуск Celery в фоновом режиме
    await start_celery()
    await asyncio.gather(start_bot())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
