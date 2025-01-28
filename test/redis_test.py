import asyncio
import unittest

from bot.config import redis


# get cached lol
async def watch_profile(user_id: int, id_watched: int, ttl: int = 5):
    await redis.sadd(f'watched:{user_id}', id_watched)
    await redis.expire(f'watched:{user_id}', ttl)


async def get_ids_to_skip(user_id: int):
    ids = await redis.smembers(f'watched:{user_id}')
    return ids


class TestAsyncFunction(unittest.IsolatedAsyncioTestCase):
    async def test_simple_cache(self):
        user_id = 1
        id_watched = [2, 3, 4]
        for id_ in id_watched:
            await watch_profile(user_id, id_)
        res = await get_ids_to_skip(user_id)
        res = set(map(int, res))
        self.assertEqual(res, set(id_watched))
        await asyncio.sleep(6)
        res = await get_ids_to_skip(user_id)
        self.assertEqual(res, set())


if __name__ == "__main__":
    unittest.main()
