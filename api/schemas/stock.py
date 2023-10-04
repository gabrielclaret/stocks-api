from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

import pandas as pd
from numpy import nan
from pydantic import BaseModel

STOCK_SERIES_COLUMNS_RENAMER = {
    "Date": "date",
    "Symbol": "symbol",
    "Series": "series",
    "Prev Close": "previous_close",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Last": "last",
    "Close": "close",
    "VWAP": "vwap",
    "Volume": "volume",
    "Turnover": "turnover",
    "Trades": "trades",
    "Deliverable Volume": "deliverable_volume",
    "%Deliverble": "deliverable_percent",
}


class Stock(BaseModel):
    """Stock representation."""

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
        data["id"] = data["_id"]
        return Stock(**data)

    @classmethod
    def fields(cls) -> List[str]:
        """Return all fields from Stock base model."""
        return list(cls.__fields__)


class StockSeries(BaseModel):
    """Stock observation representation."""

    date: List[datetime]
    symbol: List[Union[str, None]]
    series: List[Union[str, None]]
    previous_close: List[Union[float, None]]
    open: List[Union[float, None]]
    high: List[Union[float, None]]
    low: List[Union[float, None]]
    last: List[Union[float, None]]
    close: List[Union[float, None]]
    vwap: List[Union[float, None]]
    volume: List[Union[int, None]]
    turnover: List[Union[float, None]]
    trades: List[Union[float, None]]
    deliverable_volume: List[Union[int, None]]
    deliverable_percent: List[Union[float, None]]

    @classmethod
    def from_dataframe(cls, data: pd.DataFrame):  # noqa
        data = data.replace({nan: None})
        data["date"] = pd.to_datetime(data["date"])
        return StockSeries(**data.to_dict(orient="list"))


class StockResponse(BaseModel):
    """Stock response representation."""

    company_name: str
    industry: str
    symbol: str
    series: str
    isin_code: str
    file_format: str
    created_at: datetime
    last_updated: datetime
    time_series: StockSeries


class StockListing(BaseModel):
    """Stock representation."""

    stocks: List[Stock]
    skip: int
    limit: int
    total: int


class StockFileType(str, Enum):
    """Stock file type enumerator."""

    EXCEL = "xlsx"
    CSV = "csv"
    JSON = "json"
