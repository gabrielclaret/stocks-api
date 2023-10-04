from fastapi import APIRouter, Depends
from fastapi.params import Query

from api.dependencies.depends import get_service
from api.schemas.stock import StockListing, StockResponse
from api.services.stocks import StockService

router = APIRouter()


@router.get("")
async def list_metadata(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0, le=100),
    sort: str = Query("company_name", max_length=50),
    stocks_service: StockService = Depends(get_service(StockService)),
) -> StockListing:
    """Get a stock by id.

    Query parameters:
    **skip (int)**: documents to skip
    **limit (int)**: documents limit
    **sort (str)**: field to sort (asc: company_name, desc: -company_name)
    """
    stocks, total = stocks_service.list(skip, limit, sort)

    return StockListing(stocks=stocks, skip=skip, limit=limit, total=total)


@router.get("/{id}")
async def get(
    id: str, stocks_service: StockService = Depends(get_service(StockService))
) -> StockResponse:
    """Get a stock with its time series by id.

    Path parameters:
    **id (str)**: stock id
    """
    stock, stock_time_series = stocks_service.get(id)

    return StockResponse(**stock.model_dump(), time_series=stock_time_series)
