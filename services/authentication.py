# stdlib
from datetime import datetime, timedelta

# thirdparty
import jwt
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# project
from db import get_session
from models import User

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user_id: int):
    payload_access = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(days=7),
    }

    access_token = jwt.encode(payload_access, "secret-garage")
    return access_token


def create_refresh_token(user_id: int):
    payload_refresh = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(days=30),
    }

    access_token = jwt.encode(payload_refresh, "secret-garage")
    return access_token


async def get_current_user(session: AsyncSession = Depends(get_session), token: str = Depends(OAUTH2_SCHEME)):
    try:
        payload = jwt.decode(token, "secret-garage", "HS256")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_id(session=session, user_id=payload["user_id"])

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user


async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).filter(User.id == user_id))

    return result.scalar()



async def get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(select(User).filter(User.username == username))

    return result.scalar()


