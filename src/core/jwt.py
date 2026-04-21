import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from .config import settings


def create_token(data: dict, expires_delta: timedelta, secret_key: str, token_type: str) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    to_encode.update({
        "exp": now + expires_delta,
        "iat": now,
        "token_type": token_type,
    })
    return jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)


def create_access_token(data: dict) -> str:
    return create_token(
        data=data,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        secret_key=settings.SECRET_KEY_ACCESS,
        token_type="access",
    )


def create_refresh_token(data: dict) -> str:
    return create_token(
        data=data,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        secret_key=settings.SECRET_KEY_REFRESH,
        token_type="refresh",
    )


def verify_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_ACCESS, algorithms=[settings.ALGORITHM])
        if payload.get("token_type") != "access":
            return None
        return payload
    except (InvalidTokenError, ExpiredSignatureError):
        return None


def verify_refresh_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_REFRESH, algorithms=[settings.ALGORITHM])
        if payload.get("token_type") != "refresh":
            return None
        return payload
    except (InvalidTokenError, ExpiredSignatureError):
        return None