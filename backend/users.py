from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from config import ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db
from dependencies import get_current_active_user
from models import Token, User
from utils import authenticate_user, create_access_token

router = APIRouter()


@router.post(
    "/token",
    summary="Login For Access Token - Not For Use",
    tags=["Администирование"]
)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/users/me/",
    response_model=User,
    summary="Read Users Me - Not For Use",
    tags=["Администирование"]
)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get(
    "/users/me/items/",
    summary="Read Own Items - Not For Use",
    tags=["Администирование"])
async def read_own_items(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
