from aiogram import Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

router = Router()

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='❓ Помощь'),
        KeyboardButton(text='🔍 Поиск задач'),
    ]
], resize_keyboard=True)


@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer(
        "Привет! Я бот для поиска задач. 🤖 Выбери, что хочешь сделать: 🧩",
        reply_markup=main_keyboard
    )
