# thirdparty
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

# project
from db import get_session
from services.authentication import get_user_by_username, create_access_token, create_refresh_token


router = APIRouter(tags=["AUTHENTICATION"])

@router.post("/login", response_model=dict)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate user
    """
    user = await get_user_by_username(session=session, username=data.username)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    if not user.verify_password(password=data.password):
        raise HTTPException(status_code=409, detail="Incorrect password")

    response = {
        "access_token": create_access_token(user_id=user.id),
        "refresh_token": create_refresh_token(user_id=user.id),
    }
    return response