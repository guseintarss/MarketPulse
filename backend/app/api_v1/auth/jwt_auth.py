from users.schemas import UserShema
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import utils as auth_utils
from jwt.exceptions import InvalidTokenError


http_bearer = HTTPBearer()

router = APIRouter(prefix="/jwt", tags=["jwt"])
Bob = UserShema(
    username="Bob",
    password=auth_utils.hash_password("qwerty"),
    email="Bob@gmail.com",
)

users_db: dict[str, UserShema] = {Bob.username: Bob}


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


def auth_user_validate(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_ext = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password "
    )
    if not (user := users_db.get(username)):
        raise unauthed_ext
    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_ext
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> UserShema:
    token = credentials.credentials
    payload = auth_utils.decode_jwt(token)
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserShema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
    )


def get_current_active_user(
    user: UserShema = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")


@router.post("/login", response_model=TokenInfo)
def auth_user_jwt(
    user: UserShema = Depends(auth_user_validate),
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    access_token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
    )


@router.get("/users/me/")
def auth_user_chek_self_info(user: UserShema = Depends(get_current_active_user)):
    return {
        "username": user.username,
        "email": user.email,
    }
