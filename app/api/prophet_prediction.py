from fastapi import APIRouter, HTTPException, Query
from app.services.prophet_prediction_service import get_stock_prediction, get_detailed_analysis

router = APIRouter(
    prefix="/prediction/prophet",
    tags=["Stock Price Prediction"]
)

@router.get("/{symbol}")
def predict_stock_price(
    symbol: str,
    forecast_days: int = Query(
        default=30,
        ge=1,
        le=365,
        description="Number of days to forecast (1-365)"
    )
):
    """
    Predict stock prices using Meta's Prophet machine learning library.
    
    **How it works:**
    - Fetches last 3 years of historical data using yfinance
    - Trains a Prophet model on the historical data
    - Generates predictions for the specified number of days
    - Provides confidence intervals and model performance metrics
    
    **Parameters:**
    - `symbol`: Stock symbol (e.g., RELIANCE, TCS, INFY)
    - `forecast_days`: Number of days to forecast (default: 30, max: 365)
    
    **Returns:**
    - Current price and latest date
    - Predicted price with upper and lower bounds
    - Model performance metrics (MAE, RMSE, MAPE)
    - Daily forecast data
    - Historical sample data
    - Trend components information
    
    **Example:**
    ```
    GET /api/prediction/RELIANCE?forecast_days=30
    ```
    """
    try:
        result = get_stock_prediction(symbol, forecast_days)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/{symbol}/detailed")
def detailed_prediction_analysis(
    symbol: str,
    forecast_days: int = Query(
        default=30,
        ge=1,
        le=365,
        description="Number of days to forecast (1-365)"
    )
):
    """
    Get detailed trend analysis and decomposition for stock price prediction.
    
    **What you get:**
    - Trend decomposition (overall trend, weekly patterns, yearly patterns)
    - Significant changepoints in the stock's history
    - Seasonal effects breakdown
    
    **Parameters:**
    - `symbol`: Stock symbol (e.g., RELIANCE, TCS, INFY)
    - `forecast_days`: Number of days to forecast (default: 30, max: 365)
    
    **Returns:**
    - Detailed trend analysis for each forecast day
    - Historical changepoints where trend shifted
    - Seasonal component explanations
    
    **Example:**
    ```
    GET /api/prediction/RELIANCE/detailed?forecast_days=30
    ```
    """
    try:
        result = get_detailed_analysis(symbol, forecast_days)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

