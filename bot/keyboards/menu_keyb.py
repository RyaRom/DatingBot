from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_menu_options = ['Моя анкета', 'Поиск анкет']
recs_menu_options = ['👍', '👎', 'Меню']


def main_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=main_menu_options[0]),
    )
    builder.row(
        types.KeyboardButton(text=main_menu_options[1]),
    )
    return builder.as_markup(resize_keyboard=True)

def recs_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=recs_menu_options[0]),
        types.KeyboardButton(text=recs_menu_options[1]),
    )
    builder.row(
        types.KeyboardButton(text=recs_menu_options[2]),
    )
    return builder.as_markup(resize_keyboard=True)