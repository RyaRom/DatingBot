from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

gender_options = ['Парень ♂️', 'Девушка ♀️', 'Не важно']
orientation_options = ['Парней', 'Девушек', 'ВСЕХ']
skip_button = 'Пропустить ❌'

def gender_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=gender_options[0]),
        types.KeyboardButton(text=gender_options[1])
    )
    builder.row(
        types.KeyboardButton(text=gender_options[2]),
    )
    return builder.as_markup(resize_keyboard=True)

def orientation_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=orientation_options[0]),
        types.KeyboardButton(text=orientation_options[1])
    )
    builder.row(
        types.KeyboardButton(text=orientation_options[2]),
    )
    return builder.as_markup(resize_keyboard=True)

def location_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Выбрать местоположение', request_location=True)
    )
    return builder.as_markup(resize_keyboard=True)

# TODO: add skip doxxing option

def skip_button_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=skip_button)
    )
    return builder.as_markup(resize_keyboard=True)

