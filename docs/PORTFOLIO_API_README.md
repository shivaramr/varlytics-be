# Portfolio Analysis API

Comprehensive portfolio risk analysis API that accepts 10-50 stocks with their symbols and quantities, and provides detailed risk metrics using multiple VaR models.

## Features

- **Multiple VaR Models**: Variance-Covariance, Historical Simulation, Monte Carlo, GARCH/EGARCH, Expected Shortfall
- **Risk Metrics**: Portfolio volatility, expected returns, Sharpe ratio, Beta
- **Probability Analysis**: Upside/downside probabilities with expected values
- **Stress Testing**: Market crash and boom scenarios
- **Portfolio Composition**: Detailed breakdown with weights and values
- **Configurable**: Adjustable confidence levels (90-99.9%), simulation counts, and forecast horizons

## API Endpoints

### 1. POST `/api/portfolio/var` (Recommended - Fast)

Simplified VaR calculation optimized for speed. Returns essential metrics matching your required format.

**Request Body:**
```json
{
  "holdings": [
    {"symbol": "RELIANCE", "quantity": 100},
    {"symbol": "TCS", "quantity": 50},
    {"symbol": "INFY", "quantity": 75},
    {"symbol": "HDFCBANK", "quantity": 60},
    {"symbol": "ICICIBANK", "quantity": 80}
  ],
  "num_simulations": 10000,
  "num_days": 1,
  "confidence_level": 0.995
}
```

**Response:**
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

### 2. POST `/api/portfolio/analyze` (Comprehensive)

Complete portfolio analysis with additional metrics including composition, stress tests, and beta.

**Request Body:** Same as `/var` endpoint

**Response:** Includes everything from `/var` plus:
```json
{
  "status": "success",
  "portfolio_analysis": {
    "total_value": 153250.00,
    "expected_return": 0.07,
    "portfolio_volatility": 0.22,
    "sharpe_ratio": 0.32,
    "VaR": { ... },
    "confidence_level": 0.995,
    "forecast_horizon_days": 1,
    "probability_up": 0.68,
    "probability_down": 0.32,
    "expected_upside": 8500,
    "expected_downside": -5600,
    "portfolio_beta": 1.05,
    "portfolio_composition": {
      "RELIANCE": {
        "quantity": 100,
        "current_price": 2500.50,
        "value": 250050.00,
        "weight": 0.25
      },
      ...
    },
    "stress_test": {
      "market_crash_20": 122600.00,
      "market_crash_30": 107275.00,
      "market_boom_20": 183900.00,
      "market_boom_30": 199225.00
    }
  }
}
```

### 3. GET `/api/portfolio/example`

Returns an example portfolio for testing.

## Request Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `holdings` | array | required | 1-50 stocks | List of {symbol, quantity} objects |
| `num_simulations` | int | 10000 | 1000-100000 | Number of Monte Carlo simulations |
| `num_days` | int | 1 | 1-252 | Forecast horizon (1 = next day) |
| `confidence_level` | float | 0.995 | 0.90-0.999 | VaR confidence level (99.5% default) |
| `include_garch` | bool | false | - | Include GARCH VaR (slower, analyze only) |

## VaR Methods Explained

### 1. Variance-Covariance (Parametric VaR)
- **Method**: Assumes normal distribution of returns
- **Speed**: Very fast
- **Best for**: Well-diversified portfolios with normal-like returns
- **Limitation**: May underestimate tail risks

### 2. Historical Simulation
- **Method**: Uses actual historical returns distribution
- **Speed**: Fast
- **Best for**: Capturing actual market behavior without distribution assumptions
- **Limitation**: Assumes future will resemble past

### 3. Monte Carlo Simulation
- **Method**: Generates thousands of random price paths
- **Speed**: Moderate (depends on num_simulations)
- **Best for**: Complex portfolios, capturing various scenarios
- **Limitation**: Computationally intensive

### 4. Expected Shortfall (CVaR)
- **Method**: Average loss beyond VaR threshold
- **Speed**: Fast (computed alongside Historical VaR)
- **Best for**: Understanding expected loss in worst-case scenarios
- **Advantage**: Captures tail risk better than VaR

### 5. GARCH (Optional)
- **Method**: Models time-varying volatility
- **Speed**: Slow (model fitting required)
- **Best for**: Markets with volatility clustering
- **Limitation**: Requires significant historical data

## Usage Examples

### Python (using requests)

```python
import requests
import json

# Define your portfolio
portfolio = {
    "holdings": [
        {"symbol": "RELIANCE", "quantity": 100},
        {"symbol": "TCS", "quantity": 50},
        {"symbol": "INFY", "quantity": 75},
        {"symbol": "HDFCBANK", "quantity": 60},
        {"symbol": "ICICIBANK", "quantity": 80}
    ],
    "num_simulations": 10000,
    "num_days": 1,
    "confidence_level": 0.995
}

# Get VaR analysis
response = requests.post(
    "http://localhost:8000/api/portfolio/var",
    json=portfolio
)

result = response.json()
print(json.dumps(result, indent=2))
```

### cURL

```bash
curl -X POST "http://localhost:8000/api/portfolio/var" \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "RELIANCE", "quantity": 100},
      {"symbol": "TCS", "quantity": 50}
    ],
    "num_simulations": 10000,
    "num_days": 1,
    "confidence_level": 0.995
  }'
```

### JavaScript (fetch)

```javascript
const portfolio = {
  holdings: [
    { symbol: "RELIANCE", quantity: 100 },
    { symbol: "TCS", quantity: 50 }
  ],
  num_simulations: 10000,
  num_days: 1,
  confidence_level: 0.995
};

fetch('http://localhost:8000/api/portfolio/var', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(portfolio)
})
.then(response => response.json())
.then(data => console.log(data));
```

## Supported Stock Symbols

The API supports Indian stocks from:
- **NSE (National Stock Exchange)**: Major stocks like RELIANCE, TCS, INFY, HDFCBANK, etc.
- **BSE (Bombay Stock Exchange)**: Accessible via NSE symbols or scripcode

### Popular Symbols

| Symbol | Company |
|--------|---------|
| RELIANCE | Reliance Industries |
| TCS | Tata Consultancy Services |
| HDFCBANK | HDFC Bank |
| INFY | Infosys |
| ICICIBANK | ICICI Bank |
| HINDUNILVR | Hindustan Unilever |
| ITC | ITC Limited |
| SBIN | State Bank of India |
| BHARTIARTL | Bharti Airtel |
| LT | Larsen & Toubro |

## Understanding the Output

### Total Value
Current market value of the entire portfolio (sum of quantity × current price for all holdings).

### Expected Return
Annualized expected return based on historical performance (252 trading days).

### Portfolio Volatility
Annualized standard deviation of portfolio returns (risk measure).

### Sharpe Ratio
Risk-adjusted return metric (Expected Return / Volatility). Higher is better.

### VaR (Value at Risk)
Maximum expected loss at the specified confidence level:
- **Negative values** indicate potential losses
- Example: VaR of -5000 at 99.5% confidence means there's only a 0.5% chance of losing more than ₹5000

### Probability Up/Down
Historical probability of portfolio value increasing or decreasing on any given day.

### Expected Upside/Downside
Average expected gain (on up days) and average expected loss (on down days).

### Portfolio Beta
Sensitivity to market movements (relative to NIFTY50):
- Beta > 1: More volatile than market
- Beta = 1: Moves with market
- Beta < 1: Less volatile than market

## Performance Considerations

### Optimization Tips

1. **Use `/var` endpoint** for faster results (simplified output)
2. **Reduce simulations** for testing (1000 is usually sufficient)
3. **Set `include_garch=false`** unless specifically needed
4. **Keep portfolio size** reasonable (10-30 stocks optimal)

### Expected Response Times

| Endpoint | Portfolio Size | Simulations | Time |
|----------|---------------|-------------|------|
| `/var` | 10 stocks | 10,000 | 5-10s |
| `/var` | 50 stocks | 10,000 | 15-25s |
| `/analyze` | 10 stocks | 10,000 | 5-10s |
| `/analyze` | 50 stocks | 10,000 | 15-25s |
| `/analyze` (with GARCH) | 10 stocks | 10,000 | 30-60s |

## Error Handling

### Common Errors

**400 Bad Request**: Invalid input
```json
{
  "detail": "Quantity must be positive"
}
```

**400 Bad Request**: No data found
```json
{
  "detail": "No data found for symbol 'INVALID'"
}
```

**500 Internal Server Error**: Calculation error
```json
{
  "detail": "Error analyzing portfolio: Insufficient historical data"
}
```

## Running the API

### Start the Server

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the API
uvicorn app.main:app --reload

# API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for:
- Interactive API testing
- Complete endpoint documentation
- Request/response schemas
- Example requests

## Technical Details

### Data Sources
- Historical price data: Yahoo Finance (via yfinance)
- Market index: NIFTY 50 (^NSEI)
- Historical period: 2 years (minimum 100 days required)

### Calculations

**Portfolio Return**: `Σ(weight_i × return_i)` for all holdings

**Portfolio Volatility**: Standard deviation of portfolio returns, annualized

**Variance-Covariance VaR**: `Value × (μ + z × σ) × √days`
- μ = mean return
- z = z-score at confidence level
- σ = standard deviation

**Historical VaR**: Percentile of actual historical returns distribution

**Monte Carlo VaR**: Percentile of simulated returns distribution

### Confidence Levels

| Confidence | Percentile | Use Case |
|------------|-----------|----------|
| 90% | 10th | General risk assessment |
| 95% | 5th | Standard risk management |
| 99% | 1st | Conservative risk management |
| 99.5% | 0.5th | Regulatory compliance |
| 99.9% | 0.1st | Stress testing |

## Limitations

1. **Historical Data**: Requires at least 100 days of price data
2. **Market Hours**: Current prices reflect last closing price
3. **Liquidity**: Does not account for position liquidation impact
4. **Correlations**: Based on historical correlations (may change)
5. **Black Swan Events**: Rare extreme events may not be captured

## Best Practices

1. **Use 99.5% confidence** for regulatory compliance
2. **Run daily** to monitor risk exposure
3. **Compare VaR methods** - if they diverge significantly, investigate
4. **Monitor CVaR** - it's often more informative than VaR alone
5. **Regular rebalancing** - update quantities as positions change
6. **Stress test** - use the provided scenarios to understand extreme risks

## Support

For issues or questions:
- Check `/docs` for interactive documentation
- Use `/portfolio/example` to get a working test case
- Verify stock symbols are valid NSE/BSE tickers

