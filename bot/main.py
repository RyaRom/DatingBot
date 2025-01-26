import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import bot_key
from bot.handlers.registration import reg_router
from bot.handlers.admin import admin_router


async def main():
    bot = Bot(
        token=bot_key,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(reg_router, admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), cache = [])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
