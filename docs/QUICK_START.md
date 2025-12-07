# Quick Start Guide - Portfolio Analysis API

## 🚀 Start the Server

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Start the API server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📊 Test the API

### Option 1: Interactive Documentation (Easiest)

1. Open your browser to: `http://localhost:8000/docs`
2. Navigate to **Portfolio Analysis** section
3. Click on `POST /api/portfolio/var`
4. Click **"Try it out"**
5. Use the example request body or modify it
6. Click **"Execute"**

### Option 2: Using cURL (Command Line)

```bash
curl -X POST "http://localhost:8000/api/portfolio/var" ^
  -H "Content-Type: application/json" ^
  -d @sample_portfolio_request.json
```

### Option 3: Using PowerShell

```powershell
$portfolio = @{
    holdings = @(
        @{symbol="RELIANCE"; quantity=100},
        @{symbol="TCS"; quantity=50},
        @{symbol="INFY"; quantity=75},
        @{symbol="HDFCBANK"; quantity=60},
        @{symbol="ICICIBANK"; quantity=80}
    )
    num_simulations = 10000
    num_days = 1
    confidence_level = 0.995
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/portfolio/var" `
  -Method Post `
  -Body $portfolio `
  -ContentType "application/json"
```

## 📝 Example Response

Your output will look like this (matching your required format):

```json
{
  "status": "success",
  "var_analysis": {
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
}
```

## 🎯 API Endpoints

| Endpoint | Purpose | Speed |
|----------|---------|-------|
| `POST /api/portfolio/var` | Essential VaR metrics (recommended) | Fast (5-15s) |
| `POST /api/portfolio/analyze` | Complete analysis with stress tests | Moderate (10-30s) |
| `GET /api/portfolio/example` | Get example portfolio data | Instant |

## 🔧 Parameters Explained

### Required:
- **holdings**: Array of stocks with symbol and quantity
  - Minimum: 1 stock
  - Maximum: 50 stocks
  - Recommended: 10-30 stocks

### Optional:
- **num_simulations**: Monte Carlo simulations (default: 10000)
  - Range: 1000-100000
  - Higher = more accurate but slower

- **num_days**: Forecast horizon (default: 1)
  - Range: 1-252 days
  - 1 = next day VaR
  - 10 = 10-day VaR

- **confidence_level**: VaR confidence (default: 0.995 = 99.5%)
  - Range: 0.90-0.999
  - 0.95 = 95% confidence
  - 0.995 = 99.5% confidence (regulatory standard)
  - 0.999 = 99.9% confidence (stress testing)

## 📊 Understanding Your Results

### VaR (Value at Risk)
Shows maximum expected loss at 99.5% confidence. For example:
- **VaR = -5000**: There's only a 0.5% chance of losing more than ₹5000

### Multiple VaR Methods
Each method has strengths:

1. **Variance-Covariance**: Fast, assumes normal distribution
2. **Historical**: Uses actual past returns
3. **Monte Carlo**: Generates random scenarios
4. **Expected Shortfall**: Average loss when VaR is exceeded

💡 **Best Practice**: If all methods show similar values, your risk estimate is reliable. Large differences suggest reviewing the portfolio.

### Probability Up/Down
Based on historical data:
- **Probability Up = 0.68**: Portfolio went up 68% of trading days historically
- **Probability Down = 0.32**: Portfolio went down 32% of trading days

### Expected Upside/Downside
- **Expected Upside = 8500**: When portfolio goes up, average gain is ₹8500
- **Expected Downside = -5600**: When portfolio goes down, average loss is ₹5600

## 🎨 Example Portfolios

### Conservative (Large Cap)
```json
{
  "holdings": [
    {"symbol": "RELIANCE", "quantity": 100},
    {"symbol": "TCS", "quantity": 50},
    {"symbol": "HDFCBANK", "quantity": 60}
  ],
  "confidence_level": 0.995
}
```

### Balanced (Large + Mid Cap)
```json
{
  "holdings": [
    {"symbol": "RELIANCE", "quantity": 100},
    {"symbol": "TCS", "quantity": 50},
    {"symbol": "INFY", "quantity": 75},
    {"symbol": "HDFCBANK", "quantity": 60},
    {"symbol": "ICICIBANK", "quantity": 80},
    {"symbol": "LT", "quantity": 40}
  ],
  "confidence_level": 0.995
}
```

### Aggressive (Higher quantity variation)
```json
{
  "holdings": [
    {"symbol": "RELIANCE", "quantity": 200},
    {"symbol": "TCS", "quantity": 150},
    {"symbol": "INFY", "quantity": 100},
    {"symbol": "ADANIENT", "quantity": 500},
    {"symbol": "TATAMOTORS", "quantity": 300}
  ],
  "confidence_level": 0.999
}
```

## 🐛 Troubleshooting

### Error: "No data found for symbol"
- Check the symbol is correct (use NSE symbols: RELIANCE, TCS, INFY)
- Verify the stock trades on NSE or BSE

### Error: "Insufficient historical data"
- Stock may be newly listed
- Try with more established stocks

### Slow Response
- Reduce `num_simulations` (try 5000)
- Use fewer stocks
- Use `/var` endpoint instead of `/analyze`

## 📚 Next Steps

1. ✅ Read full documentation: [PORTFOLIO_API_README.md](PORTFOLIO_API_README.md)
2. ✅ Test with your portfolio using `/docs` interface
3. ✅ Integrate into your application
4. ✅ Set up regular monitoring (daily VaR calculations)

## 🔗 Useful Links

- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/api/portfolio/example

---

**Need Help?** Check the full [PORTFOLIO_API_README.md](PORTFOLIO_API_README.md) for detailed explanations of all features.

