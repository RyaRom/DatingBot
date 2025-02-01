from typing import Optional
import logging

from motor.motor_asyncio import AsyncIOMotorCollection

from config import users
from data.user_cache import get_user_cache, save_user_cache, get_recommendation_cache, save_recommendations_cache, \
    get_watched_cache
from data.user_model import User


class UserRepository:
    def __init__(self, user_collection: AsyncIOMotorCollection):
        self.connection = user_collection

    async def get_user(self, user_id: int) -> Optional[User]:
        cached = await get_user_cache(user_id)
        if cached:
            return cached

        userdata = await self.connection.find_one({'user_id': user_id})
        if userdata:
            user = User(**userdata)
            await save_user_cache(user)
            return user
        return None

    async def save_user(self, user: User) -> None:
        logging.info(f'User {user.user_id} saved in db')
        await save_user_cache(user)
        await self.connection.insert_one(user.model_dump())

    async def get_recommendation(self, user_id: int) -> Optional[User]:
        rec_id = await get_recommendation_cache(user_id)
        if rec_id:
            return await self.get_user(rec_id)
        user = await self.get_user(user_id)
        if not user:
            logging.error(f'Attempt to get recommendation for non-existent user {user_id}')
            return None
        excluded_ids = await get_watched_cache(user_id)
        recs = await self.recommend(user, excluded_ids=excluded_ids)
        if not recs:
            return None
        rec_user = recs.pop()
        await save_recommendations_cache(user_id, *(user.user_id for user in recs))
        return rec_user

    # big ass operation
    # TODO More robust recommendation system
    async def recommend(
            self,
            user: User,
            excluded_ids: list[int],
            limit: int = 15,
            age_range: int = 5) -> list[User]:
        excluded_ids.append(user.user_id)
        recs = self.connection.aggregate(
            [
                {'$geoNear': {
                    'near': {'type': 'Point', 'coordinates': user.location.coordinates},
                    'spherical': True,
                    'distanceField': 'distance'
                }},
                {'$match': {'user_id': {'$nin': excluded_ids},
                            'age': {'$gte': user.age - age_range, '$lte': user.age + age_range},
                            '$and': [{
                                '$or': [{'gender': user.orientation}, {'gender': 2}]
                            }, {
                                '$or': [{'orientation': user.gender}, {'orientation': 2}]
                            }]
                            }},
                {'$sample': {'size': limit}}
            ]
        )
        recs_list = await recs.to_list()
        logging.info(f'Recommendations for {user.user_id}: {recs_list}')
        return [User(**user) for user in recs_list]


user_repo = UserRepository(users)
