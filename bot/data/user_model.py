from typing import Optional

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
    # gridfs_photo_id: str  # TODO: Add local gridfs in db
    bio: Optional[str] = None
    location: Optional[Location] = None
