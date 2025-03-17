import asyncio
import subprocess

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from settings import TOKEN
from telegram_bot.routers import register_routers

bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    register_routers(dp)
    await dp.start_polling(bot)


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
