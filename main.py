import asyncio
import logging

from aiogram import Bot, Router, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers import working_with_database
from settings import TOKEN

bot = Bot(token=TOKEN)
router = Router()


@router.message(Command(commands=['start']))
async def command_start_handler(message: Message):
    web_app_url = "https://drfess.github.io/warehouseIB/index.html"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Запустить сканер", web_app=WebAppInfo(url=web_app_url)))
    await message.answer("Нажмите на кнопку ниже, чтобы открыть сканер:", reply_markup=builder.as_markup())


@router.message(F.content_type == ContentType.WEB_APP_DATA)
async def web_app_handler(message: Message):
    await message.answer(message.web_app_data)


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
