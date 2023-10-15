from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
from database.requests import *

    
async def region_kb():
    builder = InlineKeyboardBuilder()
    for i in range(1, 8):
        builder.row(InlineKeyboardButton(text=str(i), callback_data=str(f'-{i}-')))
    builder.adjust(3)
    builder.row(InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return builder.as_markup()

async def inline_address(data, tg_id):
    builder_address = InlineKeyboardBuilder()
    address = await output_addresses_db(data, tg_id)
    for adr in sorted(address._fetchiter_impl()):
        builder_address.add(InlineKeyboardButton(text=f'{adr[0]}, {adr[1]}-{adr[2]}', callback_data=str(adr[3])))
    builder_address.adjust(1)
    return builder_address.as_markup()

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')]
    ]
)