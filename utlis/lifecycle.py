from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import mongo_client ,redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup")
    await mongo_client.init_mongo_client()
    await redis_client.create_redis_pool()
    yield
    await redis_client.close_redis_pool()
    await mongo_client.close_mongo_client()
    print("shutdown")
