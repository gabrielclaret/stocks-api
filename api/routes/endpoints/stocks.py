import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query

from api.dependencies.depends import get_service
from api.schemas.stock import Stock, StockListing
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
    try:
        stocks, total = stocks_service.list_metadata(skip, limit, sort)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=500,
            detail={"description": f"error getting stock with id [{id}]."},
        )

    return StockListing(stocks=stocks, skip=skip, limit=limit, total=total)


@router.get("{id}")
async def get(
    id: str, stocks_service: StockService = Depends(get_service(StockService))
) -> Stock:
    """Get a stock with its time series by id.

    Path parameters:
    **id (str)**: document id
    """
    try:
        result = stocks_service.get_by_id(id)
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=500,
            detail={"description": f"error getting stock with id [{id}]."},
        )

    return result
