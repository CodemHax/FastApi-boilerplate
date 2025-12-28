import logging
from fastapi import HTTPException
from database.mongo_client import get_db

logger = logging.getLogger(__name__)


async def get_collections_db():
    db = await get_db()
    return db["login"]


async def register(username: str, password: str, gmail: str) -> bool:
    if username is not None and password is not None and gmail is not None:
        try:
            collections_db = await get_collections_db()
            await collections_db.insert_one({"username": username, "password": password, "gmail": gmail})
            return True
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            return False
    else:
        return False


async def username_in_db(username: str) -> bool:
    if username is not None:
        collections_db = await get_collections_db()
        exists_user = await collections_db.find_one({"username": username})
        if exists_user:
            return True
        else:
            return False
    else:
        return False


async def get_password(username: str) -> str:
    if username is not None and await username_in_db(username):
        collections_db = await get_collections_db()
        user = await collections_db.find_one({"username": username})
        return user['password']
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def email_in_db(gmail: str) -> bool:
    if gmail is not None:
        collections_db = await get_collections_db()
        exists_user = await collections_db.find_one({"gmail": gmail})
        if exists_user:
            return True
        else:
            return False
    else:
        return False


async def get_user_info(username: str) -> dict:
    if username is not None and await username_in_db(username):
        collections_db = await get_collections_db()
        user = await collections_db.find_one({"username": username})
        return {"username": user["username"], "gmail": user["gmail"]}
    return {}
