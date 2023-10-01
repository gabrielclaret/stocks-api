from typing import List, Tuple

from api.repositories.stocks import StockRepository
from api.schemas.database import SortOptions
from api.schemas.stock import Stock


class StockService:
    """Class that defines a stock service."""

    def __init__(self, stock_repository: StockRepository) -> None:
        self._stock_repository = stock_repository

    def get_by_id(self, id: str) -> Stock:
        """Get a stock with its data by an id."""
        # TODO: adicionar data from storage no stock
        stock = self._stock_repository.get_by_id(id)
        return stock

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
        stocks = self._stock_repository.list(skip, limit, sort)
        return stocks


# import io

# from api.services.serializers import SerializerFactory


# def run():  # noqa
#     serializer_factory = SerializerFactory()
#     serializer_factory.with_format("json")
#     data_serializer = serializer_factory.build()

#     buffered_data = io.BytesIO()
#     with open("infra/data/stocks/json/ADANIPORTS.json", "r") as _fi:
#         buffered_data.write(_fi.read().encode())

#     buffered_data.seek(0)
#     data = data_serializer.serialize(buffered_data)

#     print(data)
