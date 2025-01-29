import os
import re
from aioredis import Redis

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

name_regex = re.compile(r"[ а-яА-ЯёЁa-zA-Z]{2,100}")
age_regex = re.compile(r"\d{1,3}")

load_dotenv()
bot_key = os.getenv('BOT_KEY')
admins = [int(admin) for admin in os.getenv('ADMINS').split(', ')]

client = AsyncIOMotorClient(os.getenv('MAIN_DB_URL'))
db = client['bot_dating']
users = db['user_data']

redis = Redis.from_url(os.getenv('REDIS_URL'))

# TODO: Make a mongo storage for temp data in fsm
# TODO: Change polling to webhook
# TODO: Advanced filters with kinks and stuff
