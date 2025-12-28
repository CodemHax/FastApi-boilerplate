import pytest
import sys
import os
from database.mongo_client import init_mongo_client, get_db, get_client, close_mongo_client
from database.redis_client import create_redis_pool, close_redis_pool


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



@pytest.mark.asyncio
async def test_mongo_connection():

    await init_mongo_client()
    client = await get_client()
    assert client is not None

    ping_result = await client.admin.command('ping')
    assert ping_result.get('ok') == 1.0

    await close_mongo_client()


@pytest.mark.asyncio
async def test_get_db():
    db = await get_db()
    assert db is not None

    await close_mongo_client()


@pytest.mark.asyncio
async def test_redis_connection():
    redis = await create_redis_pool()
    assert redis is not None

    pong = await redis.ping()
    assert pong is True

    await close_redis_pool()
