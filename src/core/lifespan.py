from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.base import Base
from src.db.sessions import engine
from .auto_admin import auto_create_admin
from src.models import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)

    await auto_create_admin()
        
    yield
    await engine.dispose()