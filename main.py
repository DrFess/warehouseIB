import asyncio
import logging

from aiogram import Bot, Router, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from handlers import working_with_database
from settings import TOKEN, WEB_APP_URL

bot = Bot(token=TOKEN)
router = Router()


@router.message(Command(commands=['start']))
async def command_start_handler(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Сканер штрих-кода', web_app=WebAppInfo(url=WEB_APP_URL)))
    await message.answer('Добро пожаловать!', reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(F.web_app_data)
async def bare_code_handler(message: Message):
    bare_code = message.web_app_data.data
    await message.answer(f"{bare_code}")


async def main():
    dp = Dispatcher()
    dp.include_routers(
        router,
        working_with_database.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
