from typing import Optional
import logging

from config import user_repo, redis
from data.users_repository import User


async def get_user_cached(user_id: int) -> Optional[User]:
    user = await redis.get(f'data:{user_id}')
    if user:
        logging.info(f'User {user_id} found in cache')
        return User.model_validate_json(user)

async def save_user_to_cache(user: User, ttl: int = 60 * 60 * 2) -> None:
    await redis.set(f'data:{user.user_id}', user.model_dump_json(), ex=ttl)