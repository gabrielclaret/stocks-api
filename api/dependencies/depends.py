from typing import Callable

from fastapi import Depends
from pymongo.database import Database

from api.dependencies.database import get_database
from api.repositories.base import BaseRepository
from api.repositories.stocks import StockRepository
from api.services.stocks import StockService


def get_repository(
    repo_type: type[BaseRepository],
) -> Callable[[Database], BaseRepository]:
    """Get a repository as callable."""
    if repo_type is StockRepository:

        def _get_repo(db: Database = Depends(get_database)) -> BaseRepository:
            return repo_type(db)

        return _get_repo


def get_service(service_type: type[any]) -> Callable:
    """Get a service as callable."""
    if service_type == StockService:

        def _service(
            stock_repository: BaseRepository = Depends(
                get_repository(StockRepository)
            ),
        ) -> StockService:
            return StockService(
                stock_repository=stock_repository,
            )

        return _service
