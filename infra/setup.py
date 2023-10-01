import csv
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection

COLLECTION_NAME = "stocks"
STOCK_METADATA = "infra/data/stock_metadata.csv"


class Stock(BaseModel):
    """Stock base model."""

    id: Optional[str]
    company_name: str
    industry: str
    symbol: str
    series: str
    isin_code: str
    format: str
    created_at: Optional[datetime]
    last_updated: Optional[datetime]

    @classmethod
    def from_dict(cls, data: Dict):  # noqa
        data["id"] = str(data["_id"])
        return Stock(**data)


def serialize_csv(csv_path: str) -> List[Dict]:
    """Serialize csv to a Dict."""
    csv_file = open(csv_path, "r")
    reader = csv.DictReader(csv_file)

    serialized_obj = []
    for line in reader:
        serialized_obj.append(line)

    return serialized_obj


def _get_by_id(collection: Collection, doc_id: str) -> Dict:
    return collection.find_one({"_id": ObjectId(doc_id)})


def insert_document(collection: Collection, doc: Dict) -> Stock:
    """Insert a document in mongo."""
    doc["created_at"] = datetime.now()
    doc["last_updated"] = datetime.now()
    result = collection.insert_one(doc)
    inserted_doc = _get_by_id(collection, result.inserted_id)
    return Stock.from_dict(inserted_doc)


if __name__ == "__main__":
    mongo_client = MongoClient(os.getenv("MONGO_URI"), connect=False)
    database = mongo_client.get_database(os.getenv("MONGO_DATABASE"))
    logging.info("creating collections...")

    try:
        database.create_collection(COLLECTION_NAME)
    except Exception:
        pass

    global mongo_collection
    mongo_collection = database.get_collection(COLLECTION_NAME)

    stock_metadata = serialize_csv(STOCK_METADATA)

    logging.info("inserting stocks...")
    for stock in stock_metadata:
        _stock = insert_document(mongo_collection, stock)

        logging.info(f"inserted stock with id [{_stock.id}]")
