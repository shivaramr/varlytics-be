from fastapi import APIRouter, HTTPException, Query
from app.services.varlytics_special_service import get_egarch_monte_carlo_simulation
from app.services.varlytics_special_service1 import simulate_stock_egarch

router = APIRouter(
    prefix="/varlytics-special",
    tags=["VarLytics Special"]
)

@router.get("/monte-carlo/{symbol}")
def stock_monte_carlo(
    symbol: str,
    num_simulations: int = Query(default=10000, description="Number of simulations"),
    num_days: int = Query(default=252 * 3, description="Number of days to simulate")
):
    try:
        return get_egarch_monte_carlo_simulation(symbol, num_simulations, num_days)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/egarch-skewed-t/{symbol}")
def stock_egarch_skewedT(
    symbol: str,
    num_simulations: int = Query(default=10000, description="Number of simulations"),
    num_days: int = Query(default=252 * 3, description="Number of days to simulate")
):
    try:
        return simulate_stock_egarch(symbol, num_simulations, num_days)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
