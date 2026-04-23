from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.base import Base
from src.db.sessions import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
        
    yield
    await engine.dispose()