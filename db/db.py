from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from constants import DB_URL

connect_args = {"check_same_thread": False}  # sqlite3

engine = create_engine(DB_URL, connect_args=connect_args)
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
