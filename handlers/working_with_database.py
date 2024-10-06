from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db import create_tables

router = Router()


@router.message(Command(commands=['db']))
async def start_db_working(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Создать базу данных', callback_data='db_create'))
    await message.answer('Выберите действие с базой данных', reply_markup=builder.as_markup())


@router.callback_query(F.data == 'db_create')
async def start_create_db(callback: CallbackQuery):
    await callback.message.answer('Какое название таблицы?')


@router.message()
async def create_table(message: Message):
    table_name = message.text
    answer = create_tables(table_name=table_name)
    await message.answer(answer)
