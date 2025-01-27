from venv import logger

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot.config import admins
from bot.filters import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter(admin_ids=admins))


@admin_router.message(
    Command('admin'),
)
async def admin_panel(message: Message, bot: Bot):
    await message.answer('Admin panel will be here')
    logger.info(f'Admin {message.from_user.id} opened admin panel')
