import asyncio
import logging

from aiogram import Bot, Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from handlers import working_with_database
from settings import TOKEN

bot = Bot(token=TOKEN)
router = Router()


@router.message(Command(commands=['start']))
async def command_start_handler(message: Message):
    web_app_url = "https://username.github.io/your-repo/scanner.html"  # Укажи свою ссылку
    keyboard = InlineKeyboardMarkup()
    web_app_button = InlineKeyboardButton("Запустить сканер", web_app=WebAppInfo(url=web_app_url))
    keyboard.add(web_app_button)

    await message.answer("Нажмите на кнопку ниже, чтобы открыть сканер:", reply_markup=keyboard)


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
