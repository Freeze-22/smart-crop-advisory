import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "hackathon-secret-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///crop_advisory.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "hackathon-secret-key")
