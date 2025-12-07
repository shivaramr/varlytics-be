from fastapi import APIRouter, HTTPException, Query
from app.services.stock_service import get_stock_fundamentals

router = APIRouter(
    prefix="/stock",
    tags=["Stock"]  # 👈 This defines the group name in Swagger UI
)

@router.get("/{symbol}")
def stock_fundamentals(symbol: str):
    try:
        return get_stock_fundamentals(symbol)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
