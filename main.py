import asyncio
import subprocess

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from telegram_bot.queries.engine import create_table, drop_table
from telegram_bot.routers import register_routers


async def get_token():
    dsn = settings.token_for_bot
    bot = Bot(token=dsn)
    return bot


storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    register_routers(dp)
    await drop_table()
    await create_table()
    await dp.start_polling(await get_token())


def run_celery():
    subprocess.Popen(['celery', '-A', 'src.celery.tasks', 'worker', '--loglevel=info'])
    subprocess.Popen(['celery', '-A', 'src.celery.tasks', 'beat', '--loglevel=info'])


# Запуск Celery и бота одновременно
async def run_celery_and_bot():
    # Запуск Celery в фоновом режиме
    run_celery()
    await main()


if __name__ == '__main__':
    try:
        asyncio.run(run_celery_and_bot())
    except KeyboardInterrupt:
        print('Exit')
