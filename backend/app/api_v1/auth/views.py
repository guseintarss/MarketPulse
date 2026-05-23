from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from typing import Annotated


router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBasic()


@router.get("/basic-auth")
def basic_auth_credantials(
    credantials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "hi1",
        "username": credantials.username,
        "password": credantials.password,
    }
