import os

from dotenv import load_dotenv

from api.config.settings import Settings


def get_settings() -> Settings:
    """Get current settings for test."""
    if os.path.exists(os.path.join(os.getcwd(), ".env-tests")):
        os.environ["APP_PATH"] = os.getcwd()
        load_dotenv(os.path.join(os.getcwd(), ".env-tests"), override=True)

    _settings = Settings()

    _settings.API_V1_PREFIX: str = "/api/v1"

    _settings.MONGO_DATABASE: str = os.getenv("MONGO_DATABASE")
    _settings.MONGO_URI: str = os.getenv("MONGO_URI")

    _settings.STOCKS_BUCKET: str = os.getenv("STOCKS_BUCKET")

    return _settings
