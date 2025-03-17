from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_keyboard(items):
    keyboard = [[KeyboardButton(text=str(item))] for item in items]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
