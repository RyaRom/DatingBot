from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_menu_options = ['Моя анкета', 'Поиск анкет']


def main_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=main_menu_options[0]),
    )
    builder.row(
        types.KeyboardButton(text=main_menu_options[1]),
    )
    return builder.as_markup(resize_keyboard=True)
