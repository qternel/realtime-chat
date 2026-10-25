from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from constants import HASHING_ALGORITHM, HASHING_SECRET_KEY
from db.db import get_db
from db.models import User
from server.models.auth import AuthRequest


class AuthService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self._db = db

    def register_user(self, req: AuthRequest):
        if self._db.query(User).filter(User.username == req.user.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user with this name already exists",
            )
        hashed_password = bcrypt.hashpw(req.user.password.encode(), bcrypt.gensalt())

        user = User(
            username=req.user.username, hashed_password=hashed_password.decode()
        )

        user_id = user.id

        self._db.add(user)
        self._db.commit()

        token = self.create_jwt(user_id, req.user.username)
        return {"token": token}

    @staticmethod
    def create_jwt(id: int, username: str):
        claims = {}
        claims.update({"sub": id})
        claims.update({"username": username})

        exp = datetime.now(timezone.utc) + timedelta(minutes=60 * 24)
        claims.update({"exp": exp})

        token = jwt.encode(
            claims=claims, key=HASHING_SECRET_KEY, algorithm=HASHING_ALGORITHM
        )

        return token
