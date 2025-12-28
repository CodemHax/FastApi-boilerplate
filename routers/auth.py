import json

from starlette.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.authmodel import RegisterModel
from database.login_db import register, username_in_db, email_in_db, get_password, get_user_info
from core.auth_utlis import hashing_password, verify_password
from core.token import create_token, get_current_user, create_refresh_token, verify_refresh_token
from database.redis_client import get_redis_pool

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/register")
async def register_user(model: RegisterModel):
    existing_user = await username_in_db(model.username) or await email_in_db(model.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or Email already exists")
    hash_password = hashing_password(model.password)
    await register(model.username, hash_password, model.email)
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={"success": True,"msg": f"User {model.username} registered successfully."})


@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    existing_user = await username_in_db(form_data.username)
    if existing_user:
        password_in_db = await get_password(form_data.username)
        if verify_password(form_data.password, password_in_db):
            access_token = create_token({"sub": form_data.username})
            refresh_token = create_refresh_token({"sub": form_data.username})
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password.")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username.")


@auth_router.get("/profile")
async def profile(username: str = Depends(get_current_user)):
    cc_key = f"user:{username}"
    redis_pool = await get_redis_pool()
    get_info = await redis_pool.get(cc_key)
    if get_info:
        return JSONResponse(status_code=status.HTTP_200_OK,content={"success": True,"msg": f"User cached {username} profile.", "data": json.loads(get_info)})
    else:
        get_info = await get_user_info(username)
        await redis_pool.set(cc_key, json.dumps(get_info), ex=60)
    return JSONResponse(status_code=status.HTTP_200_OK,content={"success": True,"msg": f"User {username} profile.", "data": get_info})


@auth_router.post("/refresh")
async def refresh_access_token(refresh_token: str):
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    username = payload.get("sub")
    new_access_token = create_token({"sub": username})
    return {"access_token": new_access_token, "token_type": "bearer"}
