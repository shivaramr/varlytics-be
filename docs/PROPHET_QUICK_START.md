# Prophet Prediction API - Quick Start Guide

## 🚀 Quick Installation

### Step 1: Install Prophet

Prophet requires some system dependencies. Choose your OS:

#### Windows
```bash
# Install Microsoft C++ Build Tools first (if not already installed)
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Then install prophet
pip install prophet==1.1.6
```

#### Linux (Ubuntu/Debian)
```bash
# Install build dependencies
sudo apt-get install build-essential

# Install prophet
pip install prophet==1.1.6
```

#### macOS
```bash
# Install using pip (XCode Command Line Tools should be installed)
pip install prophet==1.1.6
```

### Step 2: Install All Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Start the Server
```bash
uvicorn app.main:app --reload
```

Server will start at: `http://localhost:8000`

## 📡 Quick API Examples

### Using cURL

#### 1. Basic Prediction (30 days)
```bash
curl "http://localhost:8000/api/prediction/RELIANCE?forecast_days=30"
```

#### 2. Short-term Prediction (7 days)
```bash
curl "http://localhost:8000/api/prediction/TCS?forecast_days=7"
```

#### 3. Long-term Prediction (90 days)
```bash
curl "http://localhost:8000/api/prediction/INFY?forecast_days=90"
```

#### 4. Detailed Trend Analysis
```bash
curl "http://localhost:8000/api/prediction/HDFCBANK/detailed?forecast_days=30"
```

### Using Python

#### Basic Example
```python
import requests

response = requests.get(
    "http://localhost:8000/api/prediction/RELIANCE",
    params={"forecast_days": 30}
)

data = response.json()
print(f"Current: ₹{data['current_price']['value']}")
print(f"Predicted: ₹{data['prediction']['predicted_price']}")
print(f"Change: {data['prediction']['price_change_percent']}%")
```

#### Compare Multiple Stocks
```python
import requests

symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK"]

for symbol in symbols:
    response = requests.get(
        f"http://localhost:8000/api/prediction/{symbol}",
        params={"forecast_days": 7}
    )
    data = response.json()
    
    print(f"{symbol}:")
    print(f"  Current: ₹{data['current_price']['value']}")
    print(f"  Predicted: ₹{data['prediction']['predicted_price']}")
    print(f"  Change: {data['prediction']['price_change_percent']}%")
    print()
```

#### Get Detailed Analysis
```python
import requests

response = requests.get(
    "http://localhost:8000/api/prediction/TCS/detailed",
    params={"forecast_days": 30}
)

data = response.json()

print("Trend Analysis:")
for trend in data['trend_analysis'][:5]:
    print(f"  {trend['date']}:")
    print(f"    Trend: ₹{trend['trend']}")
    print(f"    Weekly Effect: {trend['weekly_effect']}")
    print(f"    Yearly Effect: {trend['yearly_effect']}")
```

### Using JavaScript (Node.js)

```javascript
const axios = require('axios');

async function predictStock(symbol, days) {
    try {
        const response = await axios.get(
            `http://localhost:8000/api/prediction/${symbol}`,
            { params: { forecast_days: days } }
        );
        
        const data = response.data;
        console.log(`${symbol} Prediction:`);
        console.log(`  Current: ₹${data.current_price.value}`);
        console.log(`  Predicted: ₹${data.prediction.predicted_price}`);
        console.log(`  Change: ${data.prediction.price_change_percent}%`);
        
        return data;
    } catch (error) {
        console.error(`Error: ${error.message}`);
    }
}

// Use it
predictStock('RELIANCE', 30);
```

### Using JavaScript (Browser/Fetch)

```javascript
async function getStockPrediction(symbol, days = 30) {
    const response = await fetch(
        `http://localhost:8000/api/prediction/${symbol}?forecast_days=${days}`
    );
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    console.log('Current Price:', data.current_price.value);
    console.log('Predicted Price:', data.prediction.predicted_price);
    console.log('Expected Change:', data.prediction.price_change_percent + '%');
    console.log('Direction:', data.prediction.direction);
    
    return data;
}

// Use it
getStockPrediction('TCS', 30)
    .then(data => console.log('Success!', data))
    .catch(error => console.error('Error:', error));
```

## 🧪 Test the API

### Run the Test Script
```bash
python test_prophet_prediction.py
```

This will:
- ✅ Check server status
- ✅ Test basic predictions
- ✅ Test detailed analysis
- ✅ Compare multiple stocks
- ✅ Test different forecast periods

### Expected Output
```
Current Price: ₹2,850.50
Predicted Price: ₹2,920.75
Change: +2.46% 📈 BULLISH

Model Performance:
  MAE: 45.32
  RMSE: 58.67
  MAPE: 1.89%
```

## 🌐 Swagger UI

Best way to test interactively:

1. **Open Browser**: http://localhost:8000/docs
2. **Find Section**: "Stock Price Prediction"
3. **Try Endpoints**: 
   - Click "Try it out"
   - Enter symbol (e.g., RELIANCE)
   - Set forecast_days (e.g., 30)
   - Click "Execute"

## 📊 Popular Symbols to Try

### Large Cap Stocks
- `RELIANCE` - Reliance Industries
- `TCS` - Tata Consultancy Services
- `HDFCBANK` - HDFC Bank
- `INFY` - Infosys
- `ICICIBANK` - ICICI Bank
- `HINDUNILVR` - Hindustan Unilever
- `SBIN` - State Bank of India
- `BHARTIARTL` - Bharti Airtel
- `ITC` - ITC Limited
- `LT` - Larsen & Toubro

### Indices
- `NIFTY50` or `NIFTY` - Nifty 50 Index
- `BANKNIFTY` - Bank Nifty Index

## ⚡ Quick Tips

### 1. Optimal Forecast Period
- **Short-term**: 7-14 days (more accurate)
- **Medium-term**: 30-60 days (balanced)
- **Long-term**: 90-180 days (less accurate, more strategic)

### 2. Interpreting Results
- **MAPE < 5%**: Excellent model performance
- **MAPE 5-10%**: Good model performance
- **MAPE > 10%**: Use with caution

### 3. Understanding Confidence Intervals
```
Lower Bound  ←  Predicted Price  →  Upper Bound
₹2,750.30       ₹2,920.75          ₹3,091.20

80% probability the actual price will be in this range
```

### 4. Direction Indicator
- 📈 **Bullish**: Price expected to increase
- 📉 **Bearish**: Price expected to decrease

## 🐛 Troubleshooting

### Prophet Installation Failed
```bash
# Error: Microsoft Visual C++ 14.0 is required
# Solution: Install C++ Build Tools
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### Symbol Not Found
```bash
# Error: Stock symbol 'XYZ' not found
# Solution: 
# 1. Check spelling (use uppercase)
# 2. Verify stock is listed on NSE/BSE
# 3. Try with exchange suffix: XYZ.NS or XYZ.BO
```

### Server Not Running
```bash
# Error: Connection refused
# Solution: Start the server
uvicorn app.main:app --reload
```

### Slow Response
```bash
# First request takes longer (downloads 3 years of data)
# Subsequent requests are faster
# Typical time: 2-5 seconds
```

## 📈 Response Time Expectations

| Request Type | Expected Time |
|-------------|---------------|
| First request (new symbol) | 3-5 seconds |
| Subsequent requests | 2-3 seconds |
| Detailed analysis | 3-6 seconds |

## 🎯 Use Cases

### Investment Planning
```bash
# Get 90-day forecast for quarterly planning
curl "http://localhost:8000/api/prediction/RELIANCE?forecast_days=90"
```

### Day Trading
```bash
# Get 7-day forecast for short-term trades
curl "http://localhost:8000/api/prediction/TCS?forecast_days=7"
```

### Portfolio Analysis
```python
# Compare multiple stocks
symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK"]
for symbol in symbols:
    # Get predictions and compare
    ...
```

### Trend Research
```bash
# Understand underlying patterns
curl "http://localhost:8000/api/prediction/INFY/detailed?forecast_days=30"
```

## 📚 Full Documentation

For complete documentation, see:
- **API Reference**: `PROPHET_PREDICTION_README.md`
- **Swagger UI**: http://localhost:8000/docs
- **Test Script**: `test_prophet_prediction.py`

## ⚠️ Important Disclaimers

1. **Not Financial Advice**: This is a forecasting tool, not investment advice
2. **Past Performance ≠ Future Results**: Historical patterns may not continue
3. **Use Multiple Sources**: Combine with fundamental and technical analysis
4. **Market Risks**: Stocks can be affected by unpredictable events

## 🎉 You're Ready!

Start predicting:
```bash
# 1. Start server
uvicorn app.main:app --reload

# 2. Test it
curl "http://localhost:8000/api/prediction/RELIANCE?forecast_days=30"

# 3. Open Swagger UI
# http://localhost:8000/docs
```

Happy Predicting! 📈🚀

