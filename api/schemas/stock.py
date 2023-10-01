from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class Stock(BaseModel):
    """Stock base model."""

    id: Optional[str]
    company_name: str
    industry: str
    symbol: str
    series: str
    isin_code: str
    created_at: Optional[datetime]
    last_updated: Optional[datetime]

    @classmethod
    def from_dict(cls, data: Dict):  # noqa
        data["id"] = data["_id"]
        return Stock(**data)


class StockListing(BaseModel):
    """Stock base model."""

    stocks: List[Stock]
    skip: int
    limit: int
    total: int
