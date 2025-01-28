import re
import logging
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot.config import user_repo, name_regex, age_regex
from bot.handlers.menu import MenuStates, load_profile
from bot.keyboards.registration_keyb import gender_options, gender_kb, orientation_kb, orientation_options, location_kb, \
    skip_button_kb, skip_button
from data.users_repository import User

reg_router = Router()


class RegStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_gender = State()
    waiting_for_orientation = State()
    waiting_for_location = State()
    waiting_for_bio = State()
    waiting_for_city = State()
    waiting_for_photo = State()


@reg_router.message(Command('start'))
async def first_start(message: Message, state: FSMContext):
    logging.info(f'User {message.from_user.id} started registration')

    await message.answer(text='Введите имя')
    await state.set_state(RegStates.waiting_for_name)


@reg_router.message(RegStates.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    name = message.text.strip()

    logging.info(f'User {message.from_user.id} entered name {name}')

    if not re.match(name_regex, name):
        await message.answer(text='Некорректное имя. Введите еще раз')
        return
    user = {'user_id': message.from_user.id, 'username': name}
    await state.update_data(user_obj=user)
    await message.answer(text='Введите возраст')
    await state.set_state(RegStates.waiting_for_age)


@reg_router.message(RegStates.waiting_for_age)
async def get_age(message: Message, state: FSMContext):
    age = message.text.strip()

    logging.info(f'User {message.from_user.id} entered age {age}')

    if not re.match(age_regex, age):
        await message.answer(text='Некорректный возраст. Введите еще раз')
        return
    data = await state.get_data()
    user = data['user_obj']
    user['age'] = int(age)
    await state.update_data(user_obj=user)
    await message.answer(
        text='Введите пол',
        reply_markup=gender_kb()
    )
    await state.set_state(RegStates.waiting_for_gender)


@reg_router.message(RegStates.waiting_for_gender)
async def get_gender(message: Message, state: FSMContext):
    gender = message.text.strip()

    logging.info(f'User {message.from_user.id} entered gender {gender}')

    if gender not in gender_options:
        await message.answer(
            text='Некорректный пол. Введите еще раз',
            reply_markup=gender_kb()
        )
        return
    data = await state.get_data()
    user = data['user_obj']
    if gender == gender_options[0]:
        user['gender'] = 0
    elif gender == gender_options[1]:
        user['gender'] = 1
    elif gender == gender_options[2]:
        user['gender'] = 2
    await state.update_data(user_obj=user)
    await message.answer(
        text='Кого вы ищите?',
        reply_markup=orientation_kb()
    )
    await state.set_state(RegStates.waiting_for_orientation)


@reg_router.message(RegStates.waiting_for_orientation)
async def get_orientation(message: Message, state: FSMContext):
    orientation = message.text.strip()

    logging.info(f'User {message.from_user.id} entered orientation {orientation}')

    if orientation not in orientation_options:
        await message.answer(
            text='Некорректный ответ. Введите еще раз',
            reply_markup=orientation_kb()
        )
        return
    data = await state.get_data()
    user = data['user_obj']
    if orientation == orientation_options[0]:
        user['orientation'] = 0
    elif orientation == orientation_options[1]:
        user['orientation'] = 1
    else:
        user['orientation'] = 2
    await state.update_data(user_obj=user)
    await message.answer(
        text='Для поиска людей рядом можно выбрать местоположение',
        reply_markup=location_kb()
    )
    await state.set_state(RegStates.waiting_for_location)


@reg_router.message(RegStates.waiting_for_location)
async def get_location(message: Message, state: FSMContext):
    location = message.location
    if location:
        logging.info(f'User {message.from_user.id} sent location {location.latitude} {location.longitude}')

        data = await state.get_data()
        user = data['user_obj']
        user['location'] = {'type': 'Point', 'coordinates': [location.longitude, location.latitude]}
        await state.update_data(user_obj=user)

    await message.answer(
        text='Напиши что нибудь о себе',
        reply_markup=skip_button_kb()
    )
    await state.set_state(RegStates.waiting_for_bio)


@reg_router.message(RegStates.waiting_for_bio)
async def get_bio(message: Message, state: FSMContext):
    bio = message.text.strip()

    logging.info(f'User {message.from_user.id} entered bio {bio}')

    if bio != skip_button:
        data = await state.get_data()
        user = data['user_obj']
        user['bio'] = bio
        await state.update_data(user_obj=user)

    await message.answer(
        text='Напиши свой город',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RegStates.waiting_for_city)


# TODO: Add fav song or smth like that feature here


@reg_router.message(RegStates.waiting_for_city)
async def get_city(message: Message, state: FSMContext):
    city = message.text.strip()

    logging.info(f'User {message.from_user.id} entered city {city}')

    data = await state.get_data()
    user = data['user_obj']
    user['city'] = city
    await state.update_data(user_obj=user)

    await message.answer(
        text='Отправь фотографию для профиля',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RegStates.waiting_for_photo)


# TODO: Add video instead of photo option / multiple photos

@reg_router.message(F.photo, RegStates.waiting_for_photo)
async def get_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id

    logging.info(f'User {message.from_user.id} entered photo. id = {photo}')

    data = await state.get_data()
    user = data['user_obj']
    user['photo_id'] = photo
    try:
        user = User.model_validate(user)
    except Exception as e:
        logging.error(e)
        await message.reply(text='Some error occurred in your data. Try again')
        await first_start(message, state)
        return

    await state.update_data(user_obj=None)
    await user_repo.save_user(user)
    await state.set_state(MenuStates.in_menu)
    await load_profile(user, message)
