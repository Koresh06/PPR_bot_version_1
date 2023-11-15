from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.requests import *


admin_kb_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Пользователи', callback_data='users')]
    ]
)

async def users_output_db():
    info_users = await users_output()
    
    
    builder = InlineKeyboardBuilder()
    for user in info_users:
        check = await check_block(user)
        if check:
            builder.add(InlineKeyboardButton(text=f'🟢 {await first_name(user)}', callback_data=str(user)))
        else:
            builder.add(InlineKeyboardButton(text=f'🔴 {await first_name(user)}', callback_data=str(user)))
    builder.adjust(1)
    return builder.as_markup()


