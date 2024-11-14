from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu_buttons = [
    [KeyboardButton(text='Сканер штрих-кодов')],
    [KeyboardButton(text='Получить список анализов для плановой госпитализации')],
]
menu = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True)