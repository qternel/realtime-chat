from sqlalchemy import Column, Integer, String

from db.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True)
    hashed_password = Column(String)
