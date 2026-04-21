from .config import settings
from .exception_handler import setup_exception_handlers
from .lifespan import lifespan as life_span
from .middleware import cors_middleware
from .logger_config import logger
from .exceptions import BadRequestException, NotFoundException

from fastapi import FastAPI

def general_settings(app: FastAPI):
    cors_middleware(app)
    setup_exception_handlers(app)