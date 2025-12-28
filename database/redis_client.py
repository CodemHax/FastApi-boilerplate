import asyncio

from redis.asyncio import Redis, ConnectionPool

from config.settings import settings

redis_pool = None
lock = asyncio.Lock()

async def create_redis_pool():
    global redis_pool
    async with lock:
        if redis_pool is None:
            pool = ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True, max_connections=10)
            redis_pool = Redis(connection_pool=pool)
    return redis_pool

async def close_redis_pool():
    global redis_pool
    if redis_pool:
        await redis_pool.aclose()
        redis_pool = None

async def get_redis_pool():
    if redis_pool:
        return redis_pool
    return await create_redis_pool()
