import os

from aiogram.types import MessageEntity
from dotenv import load_dotenv

load_dotenv()
bot_key = os.getenv('BOT_KEY')
admins = [int(admin) for admin in os.getenv('ADMINS').split(', ')]
