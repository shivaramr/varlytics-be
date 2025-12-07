# Stock Price Prediction API

## Overview

This service provides AI-powered stock price prediction using **Meta's Prophet** machine learning library. It analyzes 3 years of historical stock data and generates future price predictions with confidence intervals.

## Features

### 🎯 Core Capabilities
- **Historical Analysis**: Uses 3 years of historical stock data from yfinance
- **ML-Powered Predictions**: Leverages Meta's Prophet for time series forecasting
- **Confidence Intervals**: Provides upper and lower bounds (80% confidence)
- **Performance Metrics**: Includes MAE, RMSE, and MAPE for model validation
- **Trend Decomposition**: Breaks down trends into weekly, yearly, and monthly patterns
- **Flexible Forecasting**: Predict from 1 day to 1 year ahead

### 📊 What You Get
- Current stock price and date
- Predicted prices with confidence intervals
- Price change amount and percentage
- Bullish/Bearish direction indicator
- Model performance metrics
- Daily forecast data
- Historical data sample
- Trend component analysis

## Installation

### Install Dependencies

```bash
pip install -r requirements.txt
```

The new dependency added:
- `prophet==1.1.6` - Meta's Prophet library for time series forecasting

## API Endpoints

### 1. Basic Prediction

**Endpoint:** `GET /api/prediction/{symbol}`

**Parameters:**
- `symbol` (required): Stock symbol (e.g., RELIANCE, TCS, INFY)
- `forecast_days` (optional): Number of days to forecast (default: 30, max: 365)

**Example Request:**
```bash
curl "http://localhost:8000/api/prediction/RELIANCE?forecast_days=30"
```

**Example Response:**
```json
{
  "symbol": "RELIANCE",
  "yahoo_symbol": "RELIANCE.NS",
  "analysis_period": {
    "start_date": "2022-10-10",
    "end_date": "2025-10-10",
    "days_analyzed": 756
  },
  "current_price": {
    "value": 2850.50,
    "date": "2025-10-10"
  },
  "prediction": {
    "forecast_days": 30,
    "predicted_price": 2920.75,
    "lower_bound": 2750.30,
    "upper_bound": 3091.20,
    "confidence_interval": "80%",
    "price_change": 70.25,
    "price_change_percent": 2.46,
    "direction": "bullish"
  },
  "model_performance": {
    "mae": 45.32,
    "rmse": 58.67,
    "mape": 1.89,
    "description": "MAE: Mean Absolute Error, RMSE: Root Mean Squared Error, MAPE: Mean Absolute Percentage Error"
  },
  "forecast_data": [
    {
      "date": "2025-10-11",
      "predicted_price": 2855.40,
      "lower_bound": 2695.80,
      "upper_bound": 3015.00
    },
    // ... more forecast days
  ],
  "historical_sample": [
    {
      "date": "2025-09-10",
      "actual_price": 2800.25
    },
    // ... last 30 days
  ],
  "trend_components": {
    "has_weekly_seasonality": true,
    "has_yearly_seasonality": true,
    "changepoints_detected": 25
  },
  "disclaimer": "This prediction is based on historical data and Prophet's time series forecasting. It should not be considered as financial advice. Stock markets are inherently unpredictable and past performance does not guarantee future results."
}
```

### 2. Detailed Trend Analysis

**Endpoint:** `GET /api/prediction/{symbol}/detailed`

**Parameters:**
- `symbol` (required): Stock symbol
- `forecast_days` (optional): Number of days to forecast (default: 30, max: 365)

**Example Request:**
```bash
curl "http://localhost:8000/api/prediction/TCS/detailed?forecast_days=30"
```

**Example Response:**
```json
{
  "symbol": "TCS",
  "yahoo_symbol": "TCS.NS",
  "trend_analysis": [
    {
      "date": "2025-10-11",
      "trend": 3550.20,
      "weekly_effect": 15.30,
      "yearly_effect": -8.50
    },
    // ... more forecast days
  ],
  "changepoints": [
    {
      "date": "2024-08-15",
      "index": 0
    },
    // ... last 10 changepoints
  ],
  "description": {
    "trend": "The overall direction of the stock price",
    "weekly_effect": "Weekly seasonal patterns",
    "yearly_effect": "Yearly seasonal patterns",
    "changepoints": "Dates where the trend significantly changed"
  }
}
```

## Understanding the Results

### Model Performance Metrics

1. **MAE (Mean Absolute Error)**
   - Average absolute difference between predicted and actual prices
   - Lower is better
   - Expressed in the same unit as stock price

2. **RMSE (Root Mean Squared Error)**
   - Square root of average squared differences
   - Penalizes larger errors more heavily
   - Lower is better

3. **MAPE (Mean Absolute Percentage Error)**
   - Average percentage error
   - Useful for comparing across different price scales
   - Lower is better (< 5% is excellent, < 10% is good)

### Confidence Intervals

- **Lower Bound**: Pessimistic scenario (80% confidence)
- **Predicted Price**: Most likely outcome
- **Upper Bound**: Optimistic scenario (80% confidence)

The 80% confidence interval means there's an 80% probability that the actual price will fall between the lower and upper bounds.

### Trend Components

- **Trend**: Overall long-term direction
- **Weekly Effect**: Pattern that repeats every week
- **Yearly Effect**: Seasonal pattern that repeats annually
- **Changepoints**: Dates where significant trend shifts occurred

## Supported Stock Symbols

The API supports:
- **Indian Stocks**: NSE and BSE listed stocks (e.g., RELIANCE, TCS, INFY, HDFCBANK)
- **Indices**: Major Indian indices (NIFTY50, NIFTY, BANKNIFTY, etc.)

The service automatically:
1. Tries NSE first (`.NS` suffix)
2. Falls back to BSE if NSE data is unavailable (`.BO` suffix)
3. Handles indices using proper Yahoo Finance symbols

## How Prophet Works

Meta's Prophet is a time series forecasting library that:

1. **Decomposes Time Series**: Breaks down stock prices into trend, seasonality, and holidays
2. **Fits Components**: Uses curve fitting to model each component
3. **Makes Predictions**: Combines components to forecast future values
4. **Provides Uncertainty**: Calculates confidence intervals using simulations

### Prophet Model Configuration

```python
model = Prophet(
    daily_seasonality=False,      # Stocks don't have strong daily patterns
    weekly_seasonality=True,       # Markets have weekly patterns
    yearly_seasonality=True,       # Annual business cycles
    changepoint_prior_scale=0.05,  # Controls trend flexibility
    seasonality_prior_scale=10.0   # Controls seasonality flexibility
)
```

## Use Cases

### 1. Investment Planning
```bash
# Get 90-day forecast for portfolio planning
GET /api/prediction/HDFCBANK?forecast_days=90
```

### 2. Short-term Trading
```bash
# Get 7-day forecast for swing trading
GET /api/prediction/INFY?forecast_days=7
```

### 3. Long-term Analysis
```bash
# Get 6-month forecast for fundamental analysis
GET /api/prediction/RELIANCE?forecast_days=180
```

### 4. Trend Understanding
```bash
# Understand underlying trends and patterns
GET /api/prediction/TCS/detailed?forecast_days=30
```

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK**: Successful prediction
- **404 Not Found**: Stock symbol not found
- **500 Internal Server Error**: Processing error

**Example Error Response:**
```json
{
  "detail": "Stock symbol 'INVALID' not found on NSE or BSE."
}
```

## Testing the API

### Using FastAPI Swagger UI

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Open browser: `http://localhost:8000/docs`

3. Navigate to **"Stock Price Prediction"** section

4. Try the endpoints with different symbols and forecast periods

### Using Python

```python
import requests

# Basic prediction
response = requests.get(
    "http://localhost:8000/api/prediction/RELIANCE",
    params={"forecast_days": 30}
)
data = response.json()

print(f"Current Price: ₹{data['current_price']['value']}")
print(f"Predicted Price (30d): ₹{data['prediction']['predicted_price']}")
print(f"Expected Change: {data['prediction']['price_change_percent']}%")
print(f"Direction: {data['prediction']['direction']}")
```

### Using cURL

```bash
# Basic prediction
curl "http://localhost:8000/api/prediction/TCS?forecast_days=30"

# Detailed analysis
curl "http://localhost:8000/api/prediction/TCS/detailed?forecast_days=30"
```

## Performance Considerations

### Data Fetching
- First request for a symbol takes longer (downloads 3 years of data)
- Subsequent requests are faster if data is cached by yfinance

### Processing Time
- Typical response time: 2-5 seconds
- Factors affecting speed:
  - Network speed (downloading historical data)
  - Model training time
  - Forecast period length

### Optimization Tips
- Use reasonable forecast periods (30-90 days recommended)
- Cache results on client side for frequently accessed symbols
- Consider implementing server-side caching for popular stocks

## Limitations & Disclaimers

### ⚠️ Important Warnings

1. **Not Financial Advice**: This tool is for informational purposes only
2. **Past Performance**: Historical patterns may not continue in the future
3. **Market Volatility**: Unexpected events can make predictions inaccurate
4. **Model Limitations**: Prophet assumes continuity and may miss sudden changes

### Known Limitations

- Cannot predict market crashes or sudden events
- Less accurate during high volatility periods
- Assumes historical patterns will continue
- Does not consider fundamental analysis or news
- 3-year window may miss longer-term cycles

### Best Practices

1. **Combine with Other Analysis**: Use alongside fundamental and technical analysis
2. **Monitor Confidence Intervals**: Wide intervals indicate higher uncertainty
3. **Check Model Performance**: Review MAE, RMSE, MAPE before trusting predictions
4. **Regular Updates**: Run predictions regularly as new data becomes available
5. **Diversify**: Never rely on a single prediction method

## Architecture

```
┌─────────────────┐
│   API Layer     │  (app/api/prophet_prediction.py)
│   FastAPI       │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Service Layer  │  (app/services/prophet_prediction_service.py)
│   Prophet ML    │  - Data preparation
│                 │  - Model training
│                 │  - Prediction generation
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Data Layer     │  (yfinance)
│  Yahoo Finance  │  - Historical data
│                 │  - 3 years of prices
└─────────────────┘
```

## Technical Details

### Prophet Model Parameters

- **changepoint_prior_scale**: 0.05 (conservative, prevents overfitting)
- **seasonality_prior_scale**: 10.0 (allows flexibility in seasonal patterns)
- **Seasonalities**:
  - Weekly: Enabled (market day-of-week effects)
  - Yearly: Enabled (annual business cycles)
  - Monthly: Custom added (30.5-day cycle)

### Data Processing

1. **Download**: 3 years of daily OHLC data
2. **Prepare**: Convert to Prophet format (ds, y columns)
3. **Train**: Fit Prophet model
4. **Predict**: Generate forecasts with confidence intervals
5. **Evaluate**: Calculate performance metrics

### Response Time Breakdown

- Data download: 1-2 seconds
- Model training: 1-2 seconds
- Prediction generation: < 1 second
- Response formatting: < 1 second
- **Total**: 2-5 seconds typically

## Future Enhancements

Potential improvements:
- [ ] Add caching for frequently requested stocks
- [ ] Include volume-based predictions
- [ ] Support for cryptocurrency predictions
- [ ] Multi-stock comparison predictions
- [ ] Export predictions to CSV/Excel
- [ ] Visualization endpoints (charts)
- [ ] Real-time prediction updates
- [ ] Custom model parameter tuning
- [ ] Ensemble predictions (multiple models)

## Troubleshooting

### Common Issues

1. **Symbol Not Found**
   - Verify symbol is correct (use NSE/BSE format)
   - Check if stock is actively traded
   - Try alternative exchange (.NS vs .BO)

2. **Slow Response**
   - First request downloads 3 years of data
   - Network issues can slow down yfinance
   - Consider implementing caching

3. **Prophet Installation Issues**
   - Prophet requires C compiler
   - On Windows: Install Microsoft C++ Build Tools
   - On Linux: `sudo apt-get install build-essential`

### Debug Mode

Run with verbose logging:
```bash
uvicorn app.main:app --reload --log-level debug
```

## Contributing

To add new features:

1. Update `app/services/prophet_prediction_service.py` for business logic
2. Update `app/api/prophet_prediction.py` for new endpoints
3. Update this README with documentation
4. Test with multiple stocks and scenarios

## License

This service is part of the VaRLytics API project.

## Support

For issues or questions:
- Check existing documentation
- Review error messages carefully
- Test with known working symbols (RELIANCE, TCS, INFY)
- Verify Prophet installation is correct

---

**Remember**: Stock market predictions are inherently uncertain. Always do your own research and consult with financial advisors before making investment decisions.

