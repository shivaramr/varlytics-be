import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import numpy as np
from app.utils.index_utils import is_index, get_yahoo_symbol


def get_stock_prediction(symbol: str, forecast_days: int = 30):
    """
    Predict stock prices using Meta's Prophet library
    
    Args:
        symbol: Stock symbol (e.g., 'RELIANCE', 'TCS')
        forecast_days: Number of days to forecast (default: 30)
    
    Returns:
        Dictionary containing historical data, predictions, and model metrics
    """
    symbol = symbol.upper()
    
    # Determine the Yahoo Finance symbol
    if is_index(symbol):
        yahoo_symbol = get_yahoo_symbol(symbol)
    else:
        # Try NSE first
        yahoo_symbol = f"{symbol}.NS"
    
    # Calculate date range (3 years of historical data)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)
    
    # Fetch historical data
    try:
        stock_data = yf.download(
            yahoo_symbol,
            start=start_date,
            end=end_date,
            progress=False
        )
        
        if stock_data.empty:
            # If NSE fails, try BSE for stocks
            if not is_index(symbol):
                yahoo_symbol = f"{symbol}.BO"
                stock_data = yf.download(
                    yahoo_symbol,
                    start=start_date,
                    end=end_date,
                    progress=False
                )
        
        if stock_data.empty:
            raise ValueError(f"No data found for symbol '{symbol}'")
            
    except Exception as e:
        raise ValueError(f"Error fetching data for '{symbol}': {str(e)}")
    
    # Prepare data for Prophet (requires 'ds' and 'y' columns)
    # Flatten column index if it's a MultiIndex (common with yfinance)
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = stock_data.columns.get_level_values(0)
    
    df = stock_data.reset_index()
    
    # Ensure Close values are 1-dimensional
    close_values = df['Close'].values
    if len(close_values.shape) > 1:
        close_values = close_values.flatten()
    
    df_prophet = pd.DataFrame({
        'ds': df['Date'].values,
        'y': close_values
    })
    
    # Initialize and fit Prophet model
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05,  # Controls flexibility of trend
        seasonality_prior_scale=10.0    # Controls flexibility of seasonality
    )
    
    # Fit the model
    model.fit(df_prophet)
    
    # Create future dataframe for predictions
    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)
    
    # Calculate model performance metrics on historical data
    historical_predictions = forecast[forecast['ds'] <= df_prophet['ds'].max()]
    actual_values = df_prophet['y'].values
    predicted_values = historical_predictions['yhat'].values[-len(actual_values):]
    
    # Calculate metrics
    mae = np.mean(np.abs(actual_values - predicted_values))
    rmse = np.sqrt(np.mean((actual_values - predicted_values) ** 2))
    mape = np.mean(np.abs((actual_values - predicted_values) / actual_values)) * 100
    
    # Get latest actual price
    latest_price = float(df_prophet['y'].iloc[-1])
    
    # Extract future predictions
    future_predictions = forecast[forecast['ds'] > df_prophet['ds'].max()].copy()
    
    # Calculate prediction statistics
    predicted_price_30d = float(future_predictions['yhat'].iloc[-1]) if len(future_predictions) > 0 else None
    predicted_upper_30d = float(future_predictions['yhat_upper'].iloc[-1]) if len(future_predictions) > 0 else None
    predicted_lower_30d = float(future_predictions['yhat_lower'].iloc[-1]) if len(future_predictions) > 0 else None
    
    # Calculate expected change
    price_change = predicted_price_30d - latest_price if predicted_price_30d else 0
    price_change_percent = (price_change / latest_price * 100) if latest_price > 0 else 0
    
    # Prepare response
    result = {
        "symbol": symbol,
        "yahoo_symbol": yahoo_symbol,
        "analysis_period": {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "days_analyzed": len(df_prophet)
        },
        "current_price": {
            "value": round(latest_price, 2),
            "date": df_prophet['ds'].iloc[-1].strftime("%Y-%m-%d")
        },
        "prediction": {
            "forecast_days": forecast_days,
            "predicted_price": round(predicted_price_30d, 2),
            "lower_bound": round(predicted_lower_30d, 2),
            "upper_bound": round(predicted_upper_30d, 2),
            "confidence_interval": "80%",
            "price_change": round(price_change, 2),
            "price_change_percent": round(price_change_percent, 2),
            "direction": "bullish" if price_change > 0 else "bearish"
        },
        "model_performance": {
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "mape": round(mape, 2),
            "description": "MAE: Mean Absolute Error, RMSE: Root Mean Squared Error, MAPE: Mean Absolute Percentage Error"
        },
        "forecast_data": [
            {
                "date": row['ds'].strftime("%Y-%m-%d"),
                "predicted_price": round(row['yhat'], 2),
                "lower_bound": round(row['yhat_lower'], 2),
                "upper_bound": round(row['yhat_upper'], 2)
            }
            for _, row in future_predictions.iterrows()
        ],
        "historical_sample": [
            {
                "date": row['ds'].strftime("%Y-%m-%d"),
                "actual_price": round(row['y'], 2)
            }
            for _, row in df_prophet.tail(30).iterrows()
        ],
        "trend_components": {
            "has_weekly_seasonality": True,
            "has_yearly_seasonality": True,
            "changepoints_detected": len(model.changepoints)
        },
        "disclaimer": "This prediction is based on historical data and Prophet's time series forecasting. "
                     "It should not be considered as financial advice. Stock markets are inherently "
                     "unpredictable and past performance does not guarantee future results."
    }
    
    return result


def get_detailed_analysis(symbol: str, forecast_days: int = 30):
    """
    Get detailed analysis including trend decomposition
    
    Args:
        symbol: Stock symbol
        forecast_days: Number of days to forecast
    
    Returns:
        Dictionary with comprehensive analysis including trend, seasonality, and holidays
    """
    symbol = symbol.upper()
    
    # Determine the Yahoo Finance symbol
    if is_index(symbol):
        yahoo_symbol = get_yahoo_symbol(symbol)
    else:
        yahoo_symbol = f"{symbol}.NS"
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)
    
    # Fetch historical data
    try:
        stock_data = yf.download(
            yahoo_symbol,
            start=start_date,
            end=end_date,
            progress=False
        )
        
        if stock_data.empty and not is_index(symbol):
            yahoo_symbol = f"{symbol}.BO"
            stock_data = yf.download(
                yahoo_symbol,
                start=start_date,
                end=end_date,
                progress=False
            )
        
        if stock_data.empty:
            raise ValueError(f"No data found for symbol '{symbol}'")
            
    except Exception as e:
        raise ValueError(f"Error fetching data for '{symbol}': {str(e)}")
    
    # Prepare data for Prophet
    # Flatten column index if it's a MultiIndex (common with yfinance)
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = stock_data.columns.get_level_values(0)
    
    df = stock_data.reset_index()
    
    # Ensure Close values are 1-dimensional
    close_values = df['Close'].values
    if len(close_values.shape) > 1:
        close_values = close_values.flatten()
    
    df_prophet = pd.DataFrame({
        'ds': df['Date'].values,
        'y': close_values
    })
    
    # Initialize Prophet with additional components
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10.0
    )
    
    # Add custom seasonality
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    
    # Fit the model
    model.fit(df_prophet)
    
    # Make predictions
    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)
    
    # Extract trend components
    trend_data = forecast[['ds', 'trend', 'weekly', 'yearly']].tail(forecast_days)
    
    result = {
        "symbol": symbol,
        "yahoo_symbol": yahoo_symbol,
        "trend_analysis": [
            {
                "date": row['ds'].strftime("%Y-%m-%d"),
                "trend": round(row['trend'], 2),
                "weekly_effect": round(row['weekly'], 2) if not pd.isna(row['weekly']) else 0,
                "yearly_effect": round(row['yearly'], 2) if not pd.isna(row['yearly']) else 0
            }
            for _, row in trend_data.iterrows()
        ],
        "changepoints": [
            {
                "date": cp.strftime("%Y-%m-%d"),
                "index": idx
            }
            for idx, cp in enumerate(model.changepoints[-10:])  # Last 10 changepoints
        ],
        "description": {
            "trend": "The overall direction of the stock price",
            "weekly_effect": "Weekly seasonal patterns",
            "yearly_effect": "Yearly seasonal patterns",
            "changepoints": "Dates where the trend significantly changed"
        }
    }
    
    return result

