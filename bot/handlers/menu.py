import logging
from typing import Optional

from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext

from bot.data.users_repository import user_repo
from bot.keyboards.menu_keyb import main_menu_kb, main_menu_options
from data.user_cache import save_watched_cache
from data.user_model import User
from keyboards.menu_keyb import recs_menu_kb, recs_menu_options

menu_router = Router()


class MenuStates(StatesGroup):
    in_action = State()
    in_search = State()


async def load_profile(user: User, message: Message, kb: ReplyKeyboardMarkup):
    await message.answer_photo(
        photo=user.photo_id,
        caption=f'{user.username}, {user.age}, {user.city}\n\n'
                f'{user.bio}',
        reply_markup=kb
    )


@menu_router.message(MenuStates.in_action)
async def action(message: Message, state: FSMContext):
    action_type = message.text.strip()
    logging.info(f'User {message.from_user.id} in action {action_type}')
    if action_type == main_menu_options[0]:
        await default_menu(message, state)
    elif action_type == main_menu_options[1]:
        await load_recommendation(message, state)


async def load_recommendation(message: Message, state: FSMContext):
    user_id = message.from_user.id
    recommended = await user_repo.get_recommendation(user_id)
    if not recommended:
        await message.answer('Вы дошли до конца Internet\n\n'
                             '(больше анкет нет)')
        await default_menu(message, state)
        return
    await load_profile(recommended, message, kb=recs_menu_kb())
    await save_watched_cache(user_id, recommended.user_id)
    await state.set_state(MenuStates.in_search)


@menu_router.message(MenuStates.in_search)
async def process_search(message: Message, state: FSMContext):
    reply = message.text.strip()
    if reply == recs_menu_options[0]:
        await message.answer('Здесь будет логика лайков')
        await message.answer(f'Вы выбрали пользователя {message.from_user.username}')
    elif reply == recs_menu_options[1]:
        await message.answer('Здесь будет логика дизлайков')
    else:
        await default_menu(message, state)
        return
    await load_recommendation(message, state)


# This should be in the end of routers tree
# TODO: maybe replace with a better pattern
@menu_router.message()
async def default_menu(
        message: Message,
        state: FSMContext,
        user: Optional[User] = None):
    from handlers.registration import start_reg
    if not user:
        user = await user_repo.get_user(message.from_user.id)
    if not user:
        logging.info(f'User {message.from_user.id} in menu was not logged in')
        await start_reg(message, state)
        return
    await load_profile(user, message, kb=main_menu_kb())
    await state.set_state(MenuStates.in_action)
