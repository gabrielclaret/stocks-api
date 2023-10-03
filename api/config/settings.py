import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Global Settings for api."""

    API_V1_PREFIX: str = "/api/v1"

    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE")
    MONGO_URI: str = os.getenv("MONGO_URI")

    STOCKS_BUCKET: str = os.getenv("STOCKS_BUCKET")


def get_settings() -> Settings:
    """Get instance of settings."""
    return Settings()
