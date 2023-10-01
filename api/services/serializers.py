import io
import json
from enum import Enum

import pandas as pd


class Serializer:
    """Serializer service base cass."""

    def serialize(self, data: io.BytesIO) -> pd.DataFrame:
        """Serialize incoming buffered data to a pandas DataFrame."""
        raise NotImplementedError()


class JsonSerializer(Serializer):
    """Serializer class for json."""

    def serialize(self, data: io.BytesIO) -> pd.DataFrame:
        """Serialize incoming buffered data to a pandas DataFrame."""
        json_data = json.load(data)
        return pd.DataFrame(json_data)


class ExcelSerializer(Serializer):
    """Serializer class for excel."""

    def serialize(self, data: io.BytesIO) -> pd.DataFrame:
        """Serialize incoming buffered data to a pandas DataFrame."""
        return pd.read_excel(data)


class CsvSerializer(Serializer):
    """Serializer class for csv."""

    def serialize(self, data: io.BytesIO) -> pd.DataFrame:
        """Serialize incoming buffered data to a pandas DataFrame."""
        return pd.read_csv(data)


class SerializerType(str, Enum):
    """Serializers base model."""

    JSON = "json"
    CSV = "csv"
    EXCEL = "xlsx"


class SerializerFactory:
    """Serializer factory class."""

    def __init__(self) -> None:
        self._serializers = {
            SerializerType.JSON: JsonSerializer,
            SerializerType.CSV: CsvSerializer,
            SerializerType.EXCEL: ExcelSerializer,
        }

    def with_format(self, file_format: SerializerType):  # noqa
        self._format = file_format
        return self

    def build(self) -> Serializer:
        """Build proper instance ."""
        if not self._format:
            raise Exception("no format provided.")

        serializer = self._serializers[self._format]

        return serializer()
