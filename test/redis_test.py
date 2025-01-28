import asyncio
import unittest

from bot.config import redis
from data.users_repository import User, Location


# get cached lol
async def _watch_profile_test(user_id: int, id_watched: int, ttl: int = 5):
    await redis.sadd(f'watched:{user_id}', id_watched)
    await redis.expire(f'watched:{user_id}', ttl)


async def _get_ids_to_skip_test(user_id: int):
    ids = await redis.smembers(f'watched:{user_id}')
    return ids

async def _add_user_to_cache_test(user: User, ttl: int = 5):
    await redis.set(f'data:{user.user_id}', user.model_dump_json(), ex=ttl)

async def _get_user_from_cache_test(user_id: int):
    user = await redis.get(f'data:{user_id}')
    return User.model_validate_json(user)

class TestAsyncFunction(unittest.IsolatedAsyncioTestCase):
    async def _test_simple_cache(self):
        user_id = 1
        id_watched = [2, 3, 4]
        for id_ in id_watched:
            await _watch_profile_test(user_id, id_)
        res = await _get_ids_to_skip_test(user_id)
        res = set(map(int, res))
        self.assertEqual(res, set(id_watched))
        await asyncio.sleep(6)
        res = await _get_ids_to_skip_test(user_id)
        self.assertEqual(res, set())

    async def _test_user_cache(self):
        user = User(
            user_id=1,
            username='test',
            age=18,
            gender=1,
            orientation=1,
            city='test',
            photo_id='test',
            location=Location(type='Point', coordinates=[111.111, 222.222])
        )
        await _add_user_to_cache_test(user)
        res = await _get_user_from_cache_test(user.user_id)
        print(res)
        self.assertEqual(res, user)


if __name__ == "__main__":
    unittest.main()
