import asyncio
import logging

from aiogram import Bot, Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from handlers import working_with_database
from settings import TOKEN

bot = Bot(token=TOKEN)
router = Router()


@router.message(Command(commands=['start']))
async def command_start_handler(message: Message):
    await message.answer('Hi!!!')


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
