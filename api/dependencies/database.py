from pymongo import MongoClient
from pymongo.database import Database

from api.config.settings import get_settings

_mongo = None


def get_mongo() -> MongoClient:
    """Get MongoClient instance."""
    global _mongo
    if not _mongo:
        _mongo = MongoClient(get_settings().MONGO_URI, connect=False)
    return _mongo


def get_database() -> Database:
    """Get current database client instance."""
    _mongo = get_mongo()
    return _mongo[get_settings().MONGO_DATABASE]


def close_connection() -> None:
    """Close current database client connection."""
    get_mongo().close()
