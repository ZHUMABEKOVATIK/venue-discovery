from contextlib import asynccontextmanager
from fastapi import FastAPI
from ..db.base import Base
from ..db.sessions import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    # async with engine.begin() as connect:
    #     await connect.run_sync(Base.metadata.create_all)
        
    yield
    # await engine.dispose()