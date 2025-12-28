from fastapi import FastAPI
from config.settings import settings
from routers.auth import auth_router
from utlis.lifecycle import lifespan
app = FastAPI(title=settings.app_name ,lifespan=lifespan, version="0.0.1")

app.include_router(auth_router)