import os

from dotenv import load_dotenv

load_dotenv()

HASHING_ALGORITHM = os.getenv("HASHING_ALGORITHM")
HASHING_SECRET_KEY = os.getenv("HASHING_SECRET_KEY")
DB_URL = "sqlite:///./realtime-chat.db"
