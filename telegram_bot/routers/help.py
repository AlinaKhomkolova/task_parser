from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "❓ Помощь")
async def help_command(message: Message):
    await message.answer("Для поиска задач выберите категорию: 📚 Тему или ⚖️ Сложность.")
