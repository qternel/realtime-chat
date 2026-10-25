from typing import Annotated

from pydantic import BaseModel, Field


class UserCredentials(BaseModel):
    username: Annotated[str, Field(min_length=1)]
    password: Annotated[str, Field(min_length=1)]


class AuthRequest(BaseModel):
    user: UserCredentials
