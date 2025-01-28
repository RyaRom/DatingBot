import logging
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.config import user_repo
from bot.keyboards.menu_keyb import main_menu_kb, main_menu_options
from data.users_repository import User

menu_router = Router()


class MenuStates(StatesGroup):
    in_menu = State()
    in_action = State()
    in_search = State()


async def load_profile(user: User, message: Message, state: FSMContext):
    await message.answer_photo(
        photo=user.photo_id,
        caption=f'{user.username}, {user.age}, {user.city}\n\n'
                f'{user.bio}',
        reply_markup=main_menu_kb()
    )
    await state.set_state(MenuStates.in_action)


@menu_router.message(MenuStates.in_action)
async def action(message: Message, state: FSMContext):
    action_type = message.text.strip()
    logging.info(f'User {message.from_user.id} in action {action_type}')
    if action_type == main_menu_options[0]:
        await state.set_state(MenuStates.in_menu)
        await default_menu(message, state)
    elif action_type == main_menu_options[1]:
        await state.set_state(MenuStates.in_search)
        await message.answer(text='search will be here')


# This should be in the end of routers tree
# TODO: maybe replace with a better pattern
@menu_router.message(MenuStates.in_menu)
@menu_router.message()
async def default_menu(message: Message, state: FSMContext):
    from bot.handlers.registration import first_start
    user = await user_repo.get_user(message.from_user.id)
    if not user:
        await first_start(message, state)
        return
    await load_profile(user, message, state)
