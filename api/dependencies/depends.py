from typing import Callable

from fastapi import Depends
from pymongo.database import Database

from api.config.settings import Settings, get_settings
from api.dependencies.database import get_database
from api.repositories.base import BaseRepository
from api.repositories.stocks import StockMetadataRepository
from api.repositories.storage import StockSeriesRepository
from api.schemas.stock import StockFileType
from api.services.stocks import StockService


def get_repository(
    repo_type: type[BaseRepository],
    series_format: str = None,
) -> Callable[[Database], BaseRepository]:
    """Get a repository as callable."""
    if repo_type is StockMetadataRepository:

        def _get_repo(db: Database = Depends(get_database)) -> BaseRepository:
            return repo_type(db)

        return _get_repo


def get_service(service_type: type[any]) -> Callable:
    """Get a service as callable."""
    if service_type == StockService:

        def _service(
            stock_metadata_repository: BaseRepository = Depends(
                get_repository(StockMetadataRepository)
            ),
            settings: Settings = Depends(get_settings),
        ) -> StockService:
            csv_stock_series_repository = StockSeriesRepository(
                settings.STOCKS_BUCKET, StockFileType.CSV
            )
            excel_stock_series_repository = StockSeriesRepository(
                settings.STOCKS_BUCKET, StockFileType.EXCEL
            )
            json_stock_series_repository = StockSeriesRepository(
                settings.STOCKS_BUCKET, StockFileType.JSON
            )

            return StockService(
                stock_metadata_repository=stock_metadata_repository,
                csv_stock_series_repository=csv_stock_series_repository,
                excel_stock_series_repository=excel_stock_series_repository,
                json_stock_series_repository=json_stock_series_repository,
            )

        return _service
