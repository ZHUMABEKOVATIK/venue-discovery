from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from .logger_config import logger

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(SQLAlchemyError)
    def general_database_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"[DATABASE ERROR]: {exc}")
        return JSONResponse(
            status_code=500, 
            content={"detail": "Internal database error"}
        )

    @app.exception_handler(Exception)
    def general_server_exception_handler(request: Request, exc: Exception):
        logger.error(f"[SERVER ERROR]: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )