from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db import create_tables, db_add_manufacturer, db_get_all_manufacturers, get_title_manufacturer, \
    db_add_product_without_barcode

router = Router()


class Database(StatesGroup):
    add_manufacturer_1 = State()
    add_manufacturer_2 = State()
    add_manufacturer_finish = State()
    add_product_1 = State()
    add_product_2 = State()
    add_product_3 = State()
    add_product_4 = State()
    add_product_finish = State()


@router.message(Command(commands=['db']))
async def start_db_working(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Создать базу данных', callback_data='db_create'))
    builder.row(InlineKeyboardButton(text='Добавить производителя', callback_data='db_add_manufacturer'))
    builder.row(InlineKeyboardButton(text='Добавить продукт', callback_data='db_add_product'))
    await message.answer('Выберите действие с базой данных', reply_markup=builder.as_markup())


@router.callback_query(F.data == 'db_create')
async def create_db(callback: CallbackQuery):
    answer = create_tables()
    await callback.message.answer(answer)


@router.callback_query(F.data == 'db_add_manufacturer')
async def give_manufacturer_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Какое название производителя?')
    await state.set_state(Database.add_manufacturer_1)


@router.message(Database.add_manufacturer_1)
async def give_manufacturer_address(message: Message, state: FSMContext):
    manufacturer_title = message.text
    await state.update_data(manufacturer_title=manufacturer_title)
    await message.answer('Введите адрес производителя')
    await state.set_state(Database.add_manufacturer_2)


@router.message(Database.add_manufacturer_2)
async def question_about_add_manufacturer(message: Message, state: FSMContext):
    data = await state.get_data()
    manufacturer_title = data.get('manufacturer_title')
    manufacturer_address = message.text
    await state.update_data(manufacturer_address=manufacturer_address)
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Да', callback_data='add_manufacturer'))
    builder.row(InlineKeyboardButton(text='Нет', callback_data='not_add_manufacturer'))
    await message.answer(f'{manufacturer_title} {manufacturer_address}, верно?', reply_markup=builder.as_markup())
    await state.set_state(Database.add_manufacturer_finish)


@router.callback_query(Database.add_manufacturer_finish)
async def add_manufacturer(callback: CallbackQuery, state: FSMContext):
    choose = callback.data
    if choose == 'add_manufacturer':
        manufacturer = await state.get_data()
        manufacturer_title = manufacturer.get('manufacturer_title')
        manufacturer_address = manufacturer.get('manufacturer_address')
        answer = db_add_manufacturer(manufacturer_title=manufacturer_title, address=manufacturer_address)
        await callback.message.answer(answer)
        await state.clear()
    elif choose == 'not_add_manufacturer':
        await callback.message.answer('Введите название производителя')
        await state.set_state(Database.add_manufacturer_1)


@router.callback_query(F.data == 'db_add_product')
async def give_product_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите название продукта')
    await state.set_state(Database.add_product_1)


@router.message(Database.add_product_1)
async def give_product_price(message: Message, state: FSMContext):
    product_title = message.text
    await state.update_data(product_title=product_title)
    await message.answer('Введите цену продукта')
    await state.set_state(Database.add_product_2)


@router.message(Database.add_product_2)
async def give_product_weight(message: Message, state: FSMContext):
    product_price = message.text
    await state.update_data(product_price=product_price)
    await message.answer('Введите вес продукта, если нет веса, то введите 1')
    await state.set_state(Database.add_product_3)


@router.message(Database.add_product_3)
async def select_manufacturer(message: Message, state: FSMContext):
    product_weight = message.text
    await state.update_data(product_weight=product_weight)
    manufacturers = db_get_all_manufacturers()
    builder = InlineKeyboardBuilder()
    for item in manufacturers:
        builder.row(InlineKeyboardButton(text=manufacturers.get(item).get('title'), callback_data=f'{item}'))
    await message.answer('Укажите производителя', reply_markup=builder.as_markup())
    await state.set_state(Database.add_product_4)


@router.callback_query(Database.add_product_4)
async def question_about_add_product(callback: CallbackQuery, state: FSMContext):
    manufacturer_id = callback.data
    await state.update_data(manufacturer_id=manufacturer_id)
    data = await state.get_data()
    product_title = data.get('product_title')
    product_price = data.get('product_price')
    product_weight = data.get('product_weight')
    manufacturer_title = get_title_manufacturer(manufacturer_id=manufacturer_id)
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Да', callback_data='add_product'))
    builder.row(InlineKeyboardButton(text='Нет', callback_data='not_add_product'))
    await callback.message.answer(
        f'Добавить {product_title} {product_price} {product_weight} {manufacturer_title}',
        reply_markup=builder.as_markup()
    )
    await state.set_state(Database.add_product_finish)


@router.callback_query(Database.add_product_finish)
async def add_manufacturer(callback: CallbackQuery, state: FSMContext):
    choose = callback.data
    if choose == 'add_product':
        data = await state.get_data()
        product_title = data.get('product_title')
        product_price = data.get('product_price')
        product_weight = data.get('product_weight')
        manufacturer_id = data.get('manufacturer_id')
        answer = db_add_product_without_barcode(product_name=product_title,
                                                price_product=product_price,
                                                weight_per_unit=product_weight,
                                                manufacturer_id=manufacturer_id)
        await callback.message.answer(answer)
        await state.clear()
    elif choose == 'not_add_product':
        await callback.message.answer('Введите название продукта')
        await state.set_state(Database.add_product_1)

