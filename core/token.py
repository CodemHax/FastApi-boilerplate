from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from config.settings import settings as Config


o2auth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, Config.JWT_SECRET_KEY, Config.JWT_ALGORITHM)
    return jwt_token

def decode(token: str):
    try:
        decoded_token = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        if decoded_token.get("exp") >= datetime.now(timezone.utc).timestamp():
            return decoded_token
        else:
            return None
    except JWTError:
        return None


async def get_current_user(token: str = Depends(o2auth_schema)):
    try:
        if token is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        payload = decode(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        username = payload.get("sub")
        if username is None:
               raise HTTPException(status_code=401,detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return username

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=int(Config.JWT_REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire, "type": "refresh"})
    jwt_token = jwt.encode(to_encode, Config.JWT_SECRET_KEY, Config.JWT_ALGORITHM)
    return jwt_token

def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        if payload.get("type") == "refresh" and payload.get("exp") >= datetime.now(timezone.utc).timestamp():
            return payload
        return None
    except JWTError:
        return None
