from venv import logger

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot.filters import AdminFilter

reg_router = Router()


@reg_router.message(Command('start'))
async def start(message: Message, bot: Bot, cache: list[str]):
    await message.answer(str(cache))
    await message.answer('Hello')
    await message.answer_dice(emoji='🎲')


@reg_router.message(F.text == 'saved')
async def get_saved_image(message: Message):
    return message.reply_photo('AgACAgIAAxkBAANMZ5av2t44udBSTSO45GWYCk9dx48AAgfuMRsHlrhIit66RiMwJocBAAMCAANzAAM2BA')


@reg_router.message(F.text == 'echo')
async def echo(message: Message, cache: list[str]):
    cache.append(message.text)
    await message.answer(str(message.from_user.id))
    await message.answer(str(cache))


@reg_router.message(F.photo)
async def echo_image(message: Message):
    logger.info(f'id = {message.photo[0].file_id}')
    await message.reply_photo(message.photo[0].file_id)
