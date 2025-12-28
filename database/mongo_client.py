from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

client = None
db = None

async def init_mongo_client():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    ping_code = await client.admin.command('ping')
    print(ping_code)
    db = client.basecode


async def get_db():
    global db
    if db is None:
        await init_mongo_client()
    return db

async def close_mongo_client():
    global client, db
    if client is not None:
        client.close()
        client = None
        db = None

async def get_client():
    global client
    if client is None:
        await init_mongo_client()
    return client
