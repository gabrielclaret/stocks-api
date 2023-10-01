from typing import Dict, List

import pymongo
from bson import ObjectId, errors
from dotenv import load_dotenv
from fastapi.exceptions import ValidationException
from pymongo.database import Database

from api.repositories.base import BaseRepository
from api.schemas.stock import Stock

load_dotenv()


class StockRepository(BaseRepository):
    """Stocks repository class."""

    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self._collection_name = "stocks"
        self._stock_collection = db[self._collection_name]

    def _create_stock_from_mongo(self, stock_dict: Dict) -> Stock:
        stock_dict["id"] = str(stock_dict["_id"])

        return Stock(**stock_dict)

    def create(self, stock: Stock) -> Stock:
        """Insert a Stock."""
        src_stock = stock.model_dump()
        src_stock.pop("id")

        result = self._stock_collection.insert_one(src_stock)

        return self.get_by_id(id=str(result.inserted_id))

    def get_by_id(self, id: str) -> Stock:
        """List a Stock by id.

        Parameters:
        id (string): stock identifier.
        """
        try:
            doc = self._stock_collection.find_one({"_id": ObjectId(id)})
        except errors.InvalidId:
            raise ValidationException(
                "The Id entered is not a valid ObjectId."
            )

        if doc:
            return self._create_stock_from_mongo(doc)

        return None

    def list(
        self,
        skip: int,
        limit: int,
        sort: List[tuple],
    ) -> List[Stock]:
        """List stocks by skip, limit and sort.

        Parameters:
        limit (int): limit of projects per page.
        skip (int): number of projects to skip.
        sort(List[tuple]): sort by
        """
        count = self._stock_collection.count_documents({})

        if skip > count or skip < 0:
            raise ValidationException("Invalid Skip value.")

        if limit < 0 or limit > 100:
            raise ValidationException("Invalid Limit value.")

        docs = (
            self._stock_collection.find({}).skip(skip).limit(limit).sort(sort)
        )

        result = []
        for doc in docs:
            result.append(self._create_stock_from_mongo(doc))

        return result, count

    def get_by_filter(
        self,
        filter: dict,
        sort: List[tuple] = [("created", pymongo.DESCENDING)],
    ) -> Stock:
        """Get a Stock using a filter specified by a dict.

        Parameters:
        filter (dict): query filter
        sort (list[tuple]): query sort
        """
        doc = self._stock_collection.find_one(filter, sort=sort)

        if doc:
            return self._create_stock_from_mongo(doc)

        return None

    def list_all(
        self,
        filter: dict,
        sort: List[tuple] = [("last_updated", pymongo.DESCENDING)],
    ) -> List[Stock]:
        """List a stock using a filter specified by a dict.

        Parameters:
        filter (dict): query filter
        sort (list[tuple]): query sort
        """
        docs = self._stock_collection.find(filter).sort(sort)

        result = []
        for doc in docs:
            result.append(self._create_stock_from_mongo(doc))

        return result
