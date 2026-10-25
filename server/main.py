from fastapi import FastAPI

from db.db import Base, engine
from server.api import auth, chat

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
