import io
import json
from typing import Dict

import pandas as pd

from api.schemas.serializer import SerializerType


class Serializer:
    """Serializer service base class."""

    def serialize(
        self, data: io.BytesIO, columns_renamer: Dict = None
    ) -> pd.DataFrame:
        """Serialize incoming buffered data to a pandas DataFrame."""
        raise NotImplementedError()


class JsonSerializer(Serializer):
    """Serializer class for json."""

    def serialize(
        self, data: io.BytesIO, columns_renamer: Dict = None
    ) -> pd.DataFrame:
        """Serialize incoming buffered data to a pandas DataFrame."""
        json_data = json.load(data)
        json_dataframe = pd.DataFrame(json_data)

        if columns_renamer:
            json_dataframe = json_dataframe.rename(columns=columns_renamer)

        return json_dataframe


class ExcelSerializer(Serializer):
    """Serializer class for excel."""

    def serialize(
        self, data: io.BytesIO, columns_renamer: Dict = None
    ) -> pd.DataFrame:
        """Serialize incoming buffered data to a pandas DataFrame."""
        excel_dataframe = pd.read_excel(data)

        if columns_renamer:
            excel_dataframe = excel_dataframe.rename(columns=columns_renamer)

        return excel_dataframe


class CsvSerializer(Serializer):
    """Serializer class for csv."""

    def serialize(
        self, data: io.BytesIO, columns_renamer: Dict = None
    ) -> pd.DataFrame:
        """Serialize incoming buffered data to a pandas DataFrame."""
        csv_dataframe = pd.read_csv(data)

        if columns_renamer:
            csv_dataframe = csv_dataframe.rename(columns=columns_renamer)

        return csv_dataframe


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
        """Build instance."""
        if not self._format:
            raise Exception("no format provided.")

        serializer = self._serializers[self._format]

        return serializer()
