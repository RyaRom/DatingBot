import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import bot_key, client
from bot.handlers.registration import reg_router
from bot.handlers.admin import admin_router

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(
    token=bot_key,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
async def main():
    dp.include_routers(admin_router, reg_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
