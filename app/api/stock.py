from fastapi import APIRouter, HTTPException, Query
from app.services.stock_service import (
    get_stock_fundamentals,
    get_macd_data,
    MACDRequest
)

router = APIRouter(
    prefix="/stock",
    tags=["Stock"]
)

@router.get("/macd")
def macd(
    symbol: str = Query(...),
    period: str = Query("6mo"),
    interval: str = Query("1d")
):
    try:
        return get_macd_data(symbol, period, interval)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/{symbol}")
def stock_fundamentals(symbol: str):
    try:
        return get_stock_fundamentals(symbol)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
