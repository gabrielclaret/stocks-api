import csv
import importlib
import os
from datetime import datetime
from typing import Dict, List, Optional

from bson import ObjectId
from dotenv.main import load_dotenv
from freezegun import freeze_time
from pydantic import BaseModel
from pymongo.collection import Collection

import tests.integration.settings as settings

COLLECTION_NAME = "stocks"
STOCK_METADATA = "tests/integration/data/stock_metadata.csv"


class Stock(BaseModel):
    """Stock base model."""

    id: Optional[str]
    company_name: str
    industry: str
    symbol: str
    series: str
    isin_code: str
    file_format: str
    created_at: Optional[datetime]
    last_updated: Optional[datetime]

    @classmethod
    def from_dict(cls, data: Dict):  # noqa
        data["id"] = str(data["_id"])
        return Stock(**data)


def set_envs_for_tests() -> None:
    """Set environment variables for test."""
    if os.path.exists(os.path.join(os.getcwd(), ".env-tests")):
        os.environ["APP_PATH"] = os.getcwd()
        load_dotenv(os.path.join(os.getcwd(), ".env-tests"), override=True)
        importlib.reload(settings)


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


@freeze_time("2023-10-04")
def insert_document(collection: Collection, doc: Dict) -> Stock:
    """Insert a document in mongo."""
    doc["created_at"] = datetime.now()
    doc["last_updated"] = datetime.now()
    result = collection.insert_one(doc)
    inserted_doc = _get_by_id(collection, result.inserted_id)
    return Stock.from_dict(inserted_doc)
