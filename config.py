import os
import secrets

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydb")
    SECRET_KEY = secrets.token_hex(16)
