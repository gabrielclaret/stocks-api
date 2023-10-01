import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Global Settings for api."""

    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE")
    MONGO_URI: str = os.getenv("MONGO_URI")


def get_settings() -> Settings:
    """Get instance of settings."""
    return Settings()
