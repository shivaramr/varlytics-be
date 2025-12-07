# Installation Guide - Portfolio Analysis API

## Prerequisites

- Python 3.8 or higher
- Virtual environment (venv)
- Internet connection (for fetching stock data)

## Step-by-Step Installation

### 1. Navigate to Project Directory
```bash
cd "C:\Users\RShivaram\OneDrive - DIGITAL BIZ SOLUTIONS PTE. LTD\Work\varlytics-be"
```

### 2. Activate Virtual Environment
```bash
.\venv\Scripts\activate
```

### 3. Install New Dependencies
The portfolio analysis API requires two additional packages:

```bash
pip install scipy==1.14.0
pip install arch==6.4.0
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python -c "import scipy; import arch; print('Dependencies installed successfully!')"
```

## New Dependencies Added

| Package | Version | Purpose |
|---------|---------|---------|
| `scipy` | 1.14.0 | Statistical functions (z-scores, distributions) |
| `arch` | 6.4.0 | GARCH/EGARCH volatility modeling |

## Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Quick Test

### Option 1: Browser (Easiest)
1. Open: http://localhost:8000/docs
2. Navigate to "Portfolio Analysis" section
3. Try the `GET /api/portfolio/example` endpoint
4. Copy the example response
5. Try `POST /api/portfolio/var` with the example data

### Option 2: PowerShell
```powershell
# Test the example endpoint
Invoke-RestMethod -Uri "http://localhost:8000/api/portfolio/example"

# Test with a simple portfolio
$portfolio = @{
    holdings = @(
        @{symbol="RELIANCE"; quantity=100},
        @{symbol="TCS"; quantity=50}
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

### Option 3: cURL
```bash
curl http://localhost:8000/api/portfolio/example

curl -X POST "http://localhost:8000/api/portfolio/var" ^
  -H "Content-Type: application/json" ^
  -d "{\"holdings\":[{\"symbol\":\"RELIANCE\",\"quantity\":100},{\"symbol\":\"TCS\",\"quantity\":50}],\"num_simulations\":10000,\"num_days\":1,\"confidence_level\":0.995}"
```

## Troubleshooting

### Issue: "Module not found"
**Solution**: Make sure you're in the virtual environment
```bash
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "No module named 'scipy'"
**Solution**: Install scipy
```bash
pip install scipy==1.14.0
```

### Issue: "No module named 'arch'"
**Solution**: Install arch
```bash
pip install arch==6.4.0
```

### Issue: "Port 8000 already in use"
**Solution**: Use a different port
```bash
uvicorn app.main:app --reload --port 8001
```

### Issue: "No data found for symbol"
**Solution**: 
- Verify the stock symbol is correct (NSE format: RELIANCE, TCS, INFY)
- Check your internet connection
- Try with a different stock

## Next Steps

1. ✅ Read [QUICK_START.md](QUICK_START.md) for basic usage
2. ✅ Read [PORTFOLIO_API_README.md](PORTFOLIO_API_README.md) for comprehensive documentation
3. ✅ Test with sample portfolio: [sample_portfolio_request.json](sample_portfolio_request.json)
4. ✅ Explore interactive docs at http://localhost:8000/docs

## API Endpoints Available

| Endpoint | Description |
|----------|-------------|
| `POST /api/portfolio/var` | Fast VaR calculation (5-15s) |
| `POST /api/portfolio/analyze` | Comprehensive analysis (10-30s) |
| `GET /api/portfolio/example` | Get example portfolio |

## Sample Request

Save this as a file (e.g., `my_portfolio.json`):
```json
{
  "holdings": [
    {"symbol": "RELIANCE", "quantity": 100},
    {"symbol": "TCS", "quantity": 50},
    {"symbol": "INFY", "quantity": 75}
  ],
  "num_simulations": 10000,
  "num_days": 1,
  "confidence_level": 0.995
}
```

Test it:
```bash
curl -X POST "http://localhost:8000/api/portfolio/var" ^
  -H "Content-Type: application/json" ^
  -d @my_portfolio.json
```

## Expected Output

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

## Need Help?

- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **Full Documentation**: [PORTFOLIO_API_README.md](PORTFOLIO_API_README.md)
- **Implementation Summary**: [PORTFOLIO_API_SUMMARY.md](PORTFOLIO_API_SUMMARY.md)
- **Interactive Docs**: http://localhost:8000/docs

---

**Ready to analyze your portfolio!** 🚀

