from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.requests import *
from keyboards.kb_inline import *
from keyboards.kb_reply import *
from filters.filter_bot import *
from lexicon import LEXICON

router = Router()


class Register_address(StatesGroup):
    region = State()
    street = State()
    house = State()
    flat = State()
    full_name = State()
    telephone = State()
    violations = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await add_new_user(message.from_user.id)
    if user:
        await message.answer(f'<b>Доброго времени суток</b> {message.from_user.first_name}', reply_markup=await kb_menu())
    else:
        await state.set_state(Register_address.region)
        await state.update_data(user=message.from_user.id)
        await message.answer(f'Доброго времени суток, {message.from_user.first_name}\nНа данный момент Вы еще не работали с данный ботом, давайте запишем Ваш первый адрес обследования\nДля начала укажите ЖЭС обследуемого адреса:', reply_markup=await region_kb())   


@router.message(F.text == 'Описание')
async def cmd_description(message: Message):
    await message.answer(
        'Бот предназначен для записи посещенных адресов с указанием данных:\n<i>- контакты собственника/жильца (адрес, ФИО, телефон);</i>\n<i>- выявленные нарушения</i>\n<i>- срок устранения нарушений</i>\n<i>- принятые меры реагирования</i>\n\n<b>Для работы с ботов выберите одну из команд в меню</b> ⤵️'
    )

#Отмена
@router.callback_query(F.data == 'cancel')
async def cmd_cancel(callback: CallbackQuery, state: FSMContext):
    try:
        callback.message.delete()
    except:
        print('error 1')
    try:
        await state.clear()
    except:
        print('error 2')
    await callback.message.answer(text=f'Доброго времени суток {callback.from_user.first_name}', reply_markup=await kb_menu())
    await callback.answer()
    
    
#Запись адреса в БД
@router.message(UpdateRecord())
async def cmd_update_record(message: Message, state: FSMContext):
    await state.set_state(Register_address.region)
    await state.update_data(user=message.from_user.id)
    await message.answer('<i>Укажите номер ЖЭС:</i>', reply_markup=await region_kb())
        

@router.callback_query(Register_address.region)
async def reg_region(callback: CallbackQuery, state: FSMContext):
    await state.update_data(region=callback.data)
    await callback.answer()
    await callback.message.answer(text='<i>Укажите улицу:</i>', reply_markup=cancel)
    region = await state.get_data()
    if await set_region_db(region):
        print('Регион добавлен')
    else:
        print('Ошибка!')
    await state.set_state(Register_address.street)


@router.message(Register_address.street)
async def reg_street(message: Message, state: FSMContext):
    await state.update_data(street=message.text)
    await message.answer('<i>Укажите номер дома:</i>', reply_markup=cancel)
    await state.set_state(Register_address.house)


@router.message(Register_address.house)
async def reg_street(message: Message, state: FSMContext):
    await state.update_data(house=message.text)
    await message.answer('<i>Укажите номер квартиры:</i>', reply_markup=cancel)
    await state.set_state(Register_address.flat)


@router.message(Register_address.flat)
async def reg_street(message: Message, state: FSMContext):
    await state.update_data(flat=message.text)
    await message.answer('<i>Укажите ФИО:</i>', reply_markup=cancel)
    await state.set_state(Register_address.full_name)


@router.message(Register_address.full_name)
async def reg_street(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer('<i>Укажите номер телефона:</i>', reply_markup=cancel)
    await state.set_state(Register_address.telephone)


@router.message(Register_address.telephone)
async def reg_flat(message: Message, state: FSMContext):
    await state.update_data(telephone=message.text)
    await message.answer('<i>Описание нарушений:</i>', reply_markup=cancel)
    address = await state.get_data()
    get_address_data = await set_address_db(address)
    if get_address_data:
        await state.update_data(address=get_address_data)
        print('Адрес добавлен')
    else:
        print('Ошибка!')
    await state.set_state(Register_address.violations)


@router.message(Register_address.violations)
async def reg_violations(message: Message, state: FSMContext):
    await state.update_data(violations=message.text)
    violations = await state.get_data()
    if await set_violations_db(violations):
        await message.answer('✅ <b>Адрес успешно добавлен</b>')
    else:
        await message.answer('❌ <b>Произошла ошибка</b>')
    await state.clear()


# Вывод данных из БД

@router.message(Output_addresses())
async def cmd_output_addresses(message: Message):
    await message.answer('<i>Укажите номер ЖЭС:</i>', reply_markup=await region_kb())
    
    
@router.callback_query(F.data.in_(LEXICON.reg_nomer()))
async def region_output(callback: CallbackQuery):
    try:
        address = await output_addresses_db(callback.data, callback.from_user.id)
        count = 0
        for _ in address._fetchiter_impl():
            count += 1
        if count > 0:
            await callback.message.answer(text=f'<b><i>Адреса ЖЭС №{callback.data[1]}</i></b>', reply_markup= await inline_address(callback.data, callback.from_user.id))
            await callback.answer(text=f'Выбран ЖЭС №{callback.data[1]}')
        else:
            await callback.message.answer(f'<b><i>Адресов в ЖЭС №{callback.data[1]}</i></b>- <u>не найдено</u>')
            await callback.answer()
    except:
        await callback.message.answer('❌ <b>Произошла ошибка</b>')
        

@router.callback_query(IsDigitCallbackData())
async def violations_output(callback: CallbackQuery):
    inform = await full_information_output_db(callback.data, callback.from_user.id)
    await callback.message.answer(f'<b>Данные по выбранному адресу</b>\n\nАдрес: ул.<i><u>{inform[0][0]}, д.{inform[0][1]}, кв.{inform[0][2]}</u></i>\nФИО: <i><u>{inform[0][3]}</u></i>\nТелефон: <i><u>{inform[0][4]}</u></i>\n\n<b>Нарушения:</b> <tg-spoiler>{inform[1]}</tg-spoiler>')
    await callback.answer()
    
    
@router.message()
async def send_echo(message: Message):
    await message.answer(text='🤨 Не понимаю')