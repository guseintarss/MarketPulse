from app.users import crud
from app.users.schemas import CreateUser
from fastapi import APIRouter


router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/")
def create_users(user: CreateUser):
    return crud.create_user(user_in=user)


@router.get("/hello")
def hello():
    return {"hello": "hello"}
