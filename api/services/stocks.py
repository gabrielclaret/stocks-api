from typing import List, Tuple

from api.repositories.stocks import StockMetadataRepository
from api.repositories.storage import StockSeriesRepository
from api.schemas.database import SortOptions
from api.schemas.stock import (
    STOCK_SERIES_COLUMNS_RENAMER,
    Stock,
    StockFileType,
    StockSeries,
)
from api.services.serializers import SerializerFactory


class StockService:
    """Class that defines a stock service."""

    def __init__(
        self,
        stock_metadata_repository: StockMetadataRepository,
        csv_stock_series_repository: StockSeriesRepository,
        excel_stock_series_repository: StockSeriesRepository,
        json_stock_series_repository: StockSeriesRepository,
    ) -> None:
        self._stock_metadata_repository = stock_metadata_repository
        self._csv_stock_series_repository = csv_stock_series_repository
        self._excel_stock_series_repository = excel_stock_series_repository
        self._json_stock_series_repository = json_stock_series_repository

        self._series_repository = {
            StockFileType.CSV: self._csv_stock_series_repository,
            StockFileType.EXCEL: self._excel_stock_series_repository,
            StockFileType.JSON: self._json_stock_series_repository,
        }

    def get_by_id(self, id: str) -> Tuple[Stock, StockSeries]:
        """Get a stock with its series given stock id."""
        stock = self._stock_metadata_repository.get_by_id(id)

        series_repository: StockSeriesRepository = self._series_repository[
            stock.file_format
        ]

        serializer_factory = SerializerFactory()
        serializer_factory.with_format(stock.file_format)
        data_serializer = serializer_factory.build()

        stock_series_blob_name = f"{stock.symbol}.{stock.file_format}"

        buffered_data = series_repository.download_as_buffer(
            stock_series_blob_name
        )

        data = data_serializer.serialize(
            buffered_data, STOCK_SERIES_COLUMNS_RENAMER
        )

        return stock, StockSeries.from_dataframe(data)

    def _format_sort(self, sort_input: str) -> List[Tuple]:
        order = SortOptions.ASCENDING.value
        if "-" in sort_input:
            order = SortOptions.DESCENDING.value
            sort_input = sort_input.replace("-", "")

        return [(sort_input, order)]

    def list_metadata(self, skip: int, limit: int, sort_input: str) -> Stock:
        """List stock metadata."""
        # TODO: voltar erro caso input de sort for errado

        sort = self._format_sort(sort_input)
        stocks = self._stock_metadata_repository.list(skip, limit, sort)
        return stocks
