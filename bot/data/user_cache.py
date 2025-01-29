import logging
from typing import Optional

from config import redis
from data.user_model import User


async def get_user_cache(user_id: int) -> Optional[User]:
    user = await redis.get(f'data:{user_id}')
    if user:
        logging.info(f'User {user_id} found in cache')
        return User.model_validate_json(user)


async def save_user_cache(user: User, ttl: int = 60 * 60 * 2) -> None:
    await redis.set(f'data:{user.user_id}', user.model_dump_json(), ex=ttl)


async def get_recommendation_cache(user_id: int) -> Optional[int]:
    res = await redis.lpop(f'rec:{user_id}')
    if res:
        return int(res)


async def save_recommendations_cache(
        user_id: int,
        *recommended_id: int,
        ttl: int = 60 * 60 * 24 * 14):
    if not recommended_id:
        return
    logging.info(f'User {user_id} saved recommendations {recommended_id}')
    await redis.rpush(f'rec:{user_id}', *recommended_id)
    await redis.expire(f'rec:{user_id}', ttl)

# Probably doesn't need expiration time so users would newer be able to see the same profile
async def save_watched_cache(
        user_id: int,
        id_watched: int,
        ttl: int = 60 * 60 * 24 * 7) -> None:
    await redis.sadd(f'watched:{user_id}', id_watched)
    await redis.expire(f'watched:{user_id}', ttl)

async def get_watched_cache(user_id: int) -> list[int]:
    watched = await redis.smembers(f'watched:{user_id}')
    return list(map(int, watched))
