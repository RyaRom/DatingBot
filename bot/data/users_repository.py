from typing import Optional
import logging

from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel

from data.user_cache import get_user_cached, save_user_to_cache


class Location(BaseModel):
    type: str = 'Point'
    coordinates: list[float]


class User(BaseModel):
    user_id: int
    username: str
    age: int
    gender: int  # 0 - male, 1 - female, 2 - other
    orientation: int  # 0 - male, 1 - female, 2 - all
    city: str
    photo_id: str
    # gridfs_photo_id: str  # TODO: Add local gridfs in db
    bio: Optional[str] = None
    location: Optional[Location] = None


class UserRepository:
    def __init__(self, user_collection: AsyncIOMotorCollection):
        self.connection = user_collection

    async def get_user(self, user_id: int) -> Optional[User]:
        cached = await get_user_cached(user_id)
        if cached:
            return cached

        userdata = await self.connection.find_one({'user_id': user_id})
        if userdata:
            user = User(**userdata)
            await save_user_to_cache(user)
            return user
        return None

    async def save_user(self, user: User):
        logging.info(f'User {user.user_id} saved in db')
        await self.connection.insert_one(user.model_dump())