from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from server.models.auth import AuthRequest
from server.services.auth_service import AuthService

router = APIRouter()


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def register_user(
    req: AuthRequest, auth_service: Annotated[AuthService, Depends()]
):
    return auth_service.register_user(req)


@router.post("/auth/sign_in")
async def sign_in_user(
    req: AuthRequest, auth_service: Annotated[AuthService, Depends()]
):
    return auth_service.sign_in_user(req)
