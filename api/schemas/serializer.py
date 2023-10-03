from enum import Enum


class SerializerType(str, Enum):
    """Serializers base model."""

    JSON = "json"
    CSV = "csv"
    EXCEL = "xlsx"
