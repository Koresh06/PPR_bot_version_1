from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def kb_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Добавить запись'))
    builder.add(KeyboardButton(text='Вывод адресов'))
    builder.add(KeyboardButton(text='Описание'))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
