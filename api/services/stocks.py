import logging
from typing import List, Tuple

from fastapi.exceptions import ValidationException

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
from api.utils import api_errors


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

    def get(self, id: str) -> Tuple[Stock, StockSeries]:
        """Get a stock and its series given a stock id."""
        stock = self._stock_metadata_repository.get_by_id(id)

        if not stock:
            api_errors.raise_error_response(
                api_errors.NotFound, detail=f"Stock with id [{id}] not found."
            )

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

    def _is_valid_sort_input(self, sort_input: str) -> bool:
        for field in Stock.fields():
            if field in sort_input:
                return True

        return False

    def list(self, skip: int, limit: int, sort_input: str) -> Stock:
        """List stock metadata."""
        sort = self._format_sort(sort_input)

        if not self._is_valid_sort_input(sort_input):
            logging.error(f"Invalid query parameter 'sort' [{sort}].")
            api_errors.raise_error_response(
                api_errors.ErrorInvalidQueryParameters,
                detail="Invalid query parameter 'sort'.",
            )

        try:
            stocks, total = self._stock_metadata_repository.list(
                skip, limit, sort
            )
        except ValidationException:
            api_errors.raise_error_response(
                api_errors.ErrorInvalidQueryParameters,
            )
        except Exception as e:
            logging.error(
                f"There was an error listing from database. Error [{e}]."
            )
            api_errors.raise_error_response(api_errors.ErrorInternal)

        logging.info(f"Total stock metadata [{total}].")

        return stocks, total
