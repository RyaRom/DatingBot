from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel


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
    gridfs_photo_id: str # TODO: Add local gridfs in db
    bio: Optional[str] = None
    location: Optional[Location] = None


class UserRepository:
    def __init__(self, user_collection: AsyncIOMotorCollection):
        self.connection = user_collection

    async def is_exist(self, user_id: int) -> bool:
        userdata = await self.connection.find_one({'user_id': user_id})
        return userdata is not None

    async def get_user(self, user_id: int) -> Optional[User]:
        userdata = await self.connection.find_one({'user_id': user_id})
        if userdata:
            return User(**userdata)
        return None

    async def update_user(self, user: User):
        pass

#TODO: finish user repository