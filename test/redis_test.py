import asyncio
import unittest

from bot.config import redis
from data.user_model import Location, User


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


async def _recommendation_list_test_push(user_id: int, *recommended_id: int):
    await redis.rpush(f'rec:{user_id}', *recommended_id)
    await redis.expire(f'rec:{user_id}', 2)


async def _get_recommendation_test(user_id: int):
    res = await redis.lpop(f'rec:{user_id}')
    if res:
        return int(res)


class TestAsyncFunction(unittest.IsolatedAsyncioTestCase):
    async def test_simple_cache(self):
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

    async def test_user_cache(self):
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

    async def test_recommendation_cache(self):
        user_id = 1
        recommended_id = [2, 3, 4]
        await _recommendation_list_test_push(user_id, *recommended_id)
        res = await _get_recommendation_test(user_id)
        self.assertEqual(res, recommended_id[0])
        await _get_recommendation_test(user_id)
        await _get_recommendation_test(user_id)
        res = await _get_recommendation_test(user_id)
        self.assertEqual(res, None)
        await _recommendation_list_test_push(user_id, 1)
        await asyncio.sleep(2.5)
        res = await _get_recommendation_test(user_id)
        self.assertEqual(res, None)

    async def asyncTearDown(self) -> None:
        await redis.flushall()
        await asyncio.sleep(0)


if __name__ == "__main__":
    unittest.main()
