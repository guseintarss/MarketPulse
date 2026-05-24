from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError

from app.auth import utils as auth_utils
from app.core.models import db_helper
from . import crud
from .schemas import RegisterUser, TokenInfo, UserInfo

http_bearer = HTTPBearer()
router = APIRouter(prefix="/jwt", tags=["jwt"])


async def validate_auth_user(
    username: str,
    password: str,
    session: AsyncSession,
) -> UserInfo:
    user = await crud.get_user_by_username(session=session, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return UserInfo.model_validate(user)


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserInfo:
    username: str | None = payload.get("sub")
    user = await crud.get_user_by_username(session=session, username=username)
    if user:
        return UserInfo.model_validate(user)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


async def get_current_active_user(
    user: UserInfo = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@router.post("/register", response_model=TokenInfo, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: RegisterUser,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    existing = await crud.get_user_by_username(
        session=session, username=user_in.username
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username already exists",
        )
    user = await crud.create_user(
        session=session,
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        is_active=user_in.is_active,
    )
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    access_token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=access_token, token_type="Bearer")


@router.post("/login", response_model=TokenInfo)
async def auth_user_jwt(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await validate_auth_user(
        username=username, password=password, session=session
    )
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    access_token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=access_token, token_type="Bearer")


@router.get("/users/me/", response_model=UserInfo)
async def auth_user_check_self_info(
    user: UserInfo = Depends(get_current_active_user),
):
    return user
