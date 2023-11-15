from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.filters import Command

from keyboards.admin_inline_kb import *
from database.requests import *
from filters.filter_bot import IsDigitCheckTg_id
import config

admin = Router()

@admin.message(Command(commands='admin'))
async def check_admin(message: Message):
    if message.from_user.id == config.ADMIN_ID:
        await message.answer(text='🖐 <b>привет Хозяин</b> 😄', reply_markup=admin_kb_menu)
    else:
        await message.answer('Вы не являетесь администратором')
        
@admin.callback_query(F.data == 'users')
async def users(callback: CallbackQuery):
    await callback.message.answer(f'<b>Пользователи</b> ✳️', reply_markup=await users_output_db())
    await callback.answer()
    

@admin.callback_query(IsDigitCheckTg_id())
async def bk_user(callback: CallbackQuery):
    await update_block(callback.data)
    await callback.message.edit_text('Пользователи', reply_markup=await users_output_db())
    await callback.answer()
        