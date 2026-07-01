import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "research_engine_secret_key")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "sqlite:///data/papers.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    DEBUG = os.getenv("DEBUG", "True") == "True"