from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, WebSocket, WebSocketException
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

        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)

        user_id = user.id

        token = self.create_jwt(user_id, req.user.username)
        return {"token": token}

    def sign_in_user(self, req: AuthRequest):
        username = req.user.username
        user = self._db.query(User).filter(User.username == username).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user with this name does not exist",
            )

        if not bcrypt.checkpw(
            req.user.password.encode(), user.hashed_password.encode()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="wrong password"
            )

        return {"token": self.create_jwt(user.id, username)}

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

    @staticmethod
    def verify_jwt(websocket: WebSocket):
        authorization = websocket.headers.get("Authorization")
        if authorization is None:
            return 0, "guest"
        try:
            parts = authorization.split()
            if len(parts) != 2 or parts[0].casefold() != "bearer":
                raise JWTError()

            token = parts[1]
            payload = jwt.decode(
                token, key=HASHING_SECRET_KEY, algorithms=[HASHING_ALGORITHM]
            )

            sub, username = payload.get("sub"), payload.get("username")

            if sub is None or username is None:
                raise JWTError()

            return int(sub), username

        except JWTError:
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION, reason="invalid jwt"
            )
