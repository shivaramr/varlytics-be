"""
Portfolio Analysis API endpoints

Provides comprehensive portfolio risk analysis including:
- Value at Risk (VaR) using multiple methods
- Portfolio volatility and expected returns
- Stress testing
- Upside/downside probabilities
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from app.services.portfolio_service import (
    calculate_portfolio_metrics,
    calculate_portfolio_var_detailed
)

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio Analysis"]
)


class PortfolioHolding(BaseModel):
    """Individual stock holding in the portfolio"""
    symbol: str = Field(..., description="Stock symbol (e.g., 'RELIANCE', 'TCS')")
    quantity: float = Field(..., gt=0, description="Number of shares held")
    
    @validator('symbol')
    def symbol_must_be_uppercase(cls, v):
        return v.upper().strip()
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v


class PortfolioAnalysisRequest(BaseModel):
    """Portfolio analysis request model"""
    holdings: List[PortfolioHolding] = Field(
        ..., 
        min_items=1, 
        max_items=50,
        description="List of stock holdings (10-50 stocks recommended)"
    )
    num_simulations: Optional[int] = Field(
        10000,
        ge=1000,
        le=100000,
        description="Number of Monte Carlo simulations (default: 10000)"
    )
    num_days: Optional[int] = Field(
        252,
        ge=1,
        le=252,
        description="Forecast horizon in days (default: 252 = 1 year)"
    )
    confidence_level: Optional[float] = Field(
        0.995,
        ge=0.90,
        le=0.999,
        description="VaR confidence level (default: 99.5%)"
    )
    include_garch: Optional[bool] = Field(
        False,
        description="Include GARCH model VaR (slower, default: False)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "holdings": [
                    {"symbol": "RELIANCE", "quantity": 100},
                    {"symbol": "TCS", "quantity": 50},
                    {"symbol": "INFY", "quantity": 75},
                    {"symbol": "HDFCBANK", "quantity": 60},
                    {"symbol": "ICICIBANK", "quantity": 80}
                ],
                "num_simulations": 10000,
                "num_days": 252,
                "confidence_level": 0.995
            }
        }


@router.post("/analyze")
async def analyze_portfolio(request: PortfolioAnalysisRequest):
    """
    Comprehensive portfolio risk analysis.
    
    Calculates:
    - Total portfolio value
    - Expected return and volatility
    - VaR using multiple methods (Variance-Covariance, Historical, Monte Carlo, CVaR)
    - Upside/downside probabilities
    - Expected gains and losses
    - Portfolio composition and weights
    - Stress test scenarios
    - Portfolio Beta (if market data available)
    
    Returns detailed portfolio metrics including VaR at specified confidence level.
    """
    try:
        holdings_dict = [
            {"symbol": h.symbol, "quantity": h.quantity}
            for h in request.holdings
        ]
        
        result = calculate_portfolio_metrics(
            holdings=holdings_dict,
            num_simulations=request.num_simulations,
            num_days=request.num_days,
            confidence_level=request.confidence_level,
            include_garch=request.include_garch
        )
        
        return {
            "status": "success",
            "portfolio_analysis": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing portfolio: {str(e)}"
        )


@router.post("/var")
async def calculate_var(request: PortfolioAnalysisRequest):
    """
    Simplified portfolio VaR calculation (faster).
    
    Returns only essential metrics:
    - Total value
    - Expected return and volatility
    - VaR estimates (multiple methods)
    - Probability up/down
    - Expected upside/downside
    
    Default forecast horizon: 252 days (1 year)
    
    This endpoint is optimized for speed and returns results similar to:
    {
      "total_value": 153250.00,
      "expected_return": 0.07,
      "portfolio_volatility": 0.22,
      "VaR": {
        "variance_covariance": -5000,
        "historical": -5200,
        "monte_carlo": -5600,
        "expected_shortfall": -6200
      },
      "probability_up": 0.68,
      "probability_down": 0.32,
      "expected_upside": 8500,
      "expected_downside": -5600
    }
    """
    try:
        holdings_dict = [
            {"symbol": h.symbol, "quantity": h.quantity}
            for h in request.holdings
        ]
        
        result = calculate_portfolio_var_detailed(
            holdings=holdings_dict,
            num_simulations=request.num_simulations,
            num_days=request.num_days,
            confidence_level=request.confidence_level
        )
        
        return {
            "status": "success",
            "var_analysis": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating VaR: {str(e)}"
        )


@router.get("/example")
async def get_example_portfolio():
    """
    Get an example portfolio for testing.
    
    Returns a sample portfolio with major Indian stocks that can be used
    to test the portfolio analysis endpoints.
    """
    return {
        "example_portfolio": {
            "holdings": [
                {"symbol": "RELIANCE", "quantity": 100},
                {"symbol": "TCS", "quantity": 50},
                {"symbol": "INFY", "quantity": 75},
                {"symbol": "HDFCBANK", "quantity": 60},
                {"symbol": "ICICIBANK", "quantity": 80},
                {"symbol": "HINDUNILVR", "quantity": 30},
                {"symbol": "ITC", "quantity": 200},
                {"symbol": "SBIN", "quantity": 150},
                {"symbol": "BHARTIARTL", "quantity": 100},
                {"symbol": "LT", "quantity": 40}
            ],
            "num_simulations": 10000,
            "num_days": 252,
            "confidence_level": 0.995
        },
        "usage": "POST this data to /api/portfolio/analyze or /api/portfolio/var"
    }

