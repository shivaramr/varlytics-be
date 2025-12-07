from fastapi import APIRouter, Query
# from app.services.search_service import search_stock_symbols
from app.services.search_service import search_stocks

router = APIRouter(
    tags=["General"]  # 👈 Grouping under "general"
)

@router.get("/search")
def search(query: str = Query(default="", min_length=0)):
    return search_stocks(query)