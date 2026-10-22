from fastapi import FastAPI

from db.db import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()
