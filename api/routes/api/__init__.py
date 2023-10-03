from fastapi import APIRouter

from api.routes.v1.endpoints import stocks

endpoint_router = APIRouter()


endpoint_router.include_router(
    stocks.router, prefix="/stocks", tags=["Stocks"]
)
