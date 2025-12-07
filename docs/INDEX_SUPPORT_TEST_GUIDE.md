# Index Support Testing Guide

## Quick Test Checklist

Use this guide to verify that index support is working correctly across all APIs.

## Prerequisites

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Server should be running at: `http://localhost:8000`

3. Access Swagger UI: `http://localhost:8000/docs`

## Test Cases

### ✅ Test 1: Search API

**Test searching for indices:**

```bash
# Search for Nifty
curl "http://localhost:8000/api/search?query=nifty"

# Expected: Should return Nifty 50, Bank Nifty, Nifty IT, etc. with is_index: true

# Search for Sensex
curl "http://localhost:8000/api/search?query=sensex"

# Expected: Should return Sensex (BSE) with is_index: true

# Search for Bank
curl "http://localhost:8000/api/search?query=bank"

# Expected: Should return Bank Nifty (index) and bank stocks
```

**Expected Response Format:**
```json
[
  {
    "symbol": "NIFTY50",
    "name": "Nifty 50",
    "sub_symbol": "^NSEI",
    "is_index": true
  },
  {
    "symbol": "BANKNIFTY",
    "name": "Bank Nifty",
    "sub_symbol": "^NSEBANK",
    "is_index": true
  }
]
```

### ✅ Test 2: Stock/Index Fundamentals API

**Test getting index fundamentals:**

```bash
# Nifty 50
curl "http://localhost:8000/api/stock/NIFTY50"

# Bank Nifty
curl "http://localhost:8000/api/stock/BANKNIFTY"

# Sensex
curl "http://localhost:8000/api/stock/SENSEX"

# Also test with alternate symbols
curl "http://localhost:8000/api/stock/NIFTY"
curl "http://localhost:8000/api/stock/NIFTY_50"
```

**Expected Response Format:**
```json
{
  "symbol": "^NSEI",
  "longName": "NIFTY 50",
  "sector": null,
  "industry": null,
  "marketCap": null,
  "previousClose": 19500.25,
  "open": 19520.00,
  "dayHigh": 19600.50,
  "dayLow": 19480.00,
  "fiftyTwoWeekHigh": 21000.00,
  "fiftyTwoWeekLow": 17000.00,
  "forwardPE": null,
  "dividendYield": null,
  "beta": null
}
```

### ✅ Test 3: Monte Carlo Simulation

**Test Monte Carlo simulation on indices:**

```bash
# Nifty 50 - Quick test (1000 simulations)
curl "http://localhost:8000/api/simulations/NIFTY50/monte-carlo?num_simulations=1000&num_days=252"

# Bank Nifty
curl "http://localhost:8000/api/simulations/BANKNIFTY/monte-carlo?num_simulations=1000&num_days=252"

# Sensex
curl "http://localhost:8000/api/simulations/SENSEX/monte-carlo?num_simulations=1000&num_days=252"
```

**Expected Response Format:**
```json
{
  "symbol": "NIFTY50",
  "simulation_type": "monte-carlo",
  "num_simulations": 1000,
  "num_days": 252,
  "result": {
    "mean": 21450.75,
    "min": 15200.50,
    "max": 28600.25,
    "P(min)": 0.0245,
    "P(max)": 0.0312
  }
}
```

### ✅ Test 4: All Simulations (Ultra-Optimized)

**Test all 22 simulations on an index:**

```bash
# This should complete in 3-5 seconds
curl "http://localhost:8000/api/simulations/NIFTY50/all?num_simulations=10000&num_days=252&optimized=true"
```

**Expected Response:**
```json
{
  "symbol": "NIFTY50",
  "num_simulations": 10000,
  "num_days": 252,
  "optimized": true,
  "results": {
    "GARCH-N": {...},
    "GARCH-T": {...},
    "GARCH-GED": {...},
    ... (20 more models)
  }
}
```

### ✅ Test 5: Specific GARCH Model

**Test individual GARCH models:**

```bash
# GARCH-T on Bank Nifty
curl "http://localhost:8000/api/simulations/BANKNIFTY/garch-t?num_simulations=5000&num_days=252"

# EGARCH-N on Nifty 50
curl "http://localhost:8000/api/simulations/NIFTY50/egarch-n?num_simulations=5000&num_days=252"

# GJR-GARCH-Skewed-T on Sensex
curl "http://localhost:8000/api/simulations/SENSEX/gjr-garch-skewed-t?num_simulations=5000&num_days=252"
```

### ✅ Test 6: Historical Simulation

**Test historical simulation on indices:**

```bash
curl "http://localhost:8000/api/simulations/NIFTY50/historical?num_simulations=5000&num_days=252"
```

### ✅ Test 7: Risk Metrics (EWMA)

**Test RiskMetrics on indices:**

```bash
curl "http://localhost:8000/api/simulations/BANKNIFTY/risk-metrics?num_simulations=5000&num_days=252"
```

### ✅ Test 8: Portfolio Analysis with Index Only

**Test portfolio with only indices:**

```bash
curl -X POST "http://localhost:8000/api/portfolio/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "NIFTY50", "quantity": 100},
      {"symbol": "BANKNIFTY", "quantity": 50}
    ],
    "num_simulations": 5000,
    "num_days": 252,
    "confidence_level": 0.995
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "portfolio_analysis": {
    "total_value": 2500000.00,
    "expected_return": 0.08,
    "portfolio_volatility": 0.18,
    "var": {
      "variance_covariance": -250000,
      "historical": -260000,
      "monte_carlo": -270000,
      "expected_shortfall": -300000
    },
    "holdings": [...],
    "composition": [...],
    ...
  }
}
```

### ✅ Test 9: Mixed Portfolio (Stocks + Indices)

**Test portfolio with both stocks and indices:**

```bash
curl -X POST "http://localhost:8000/api/portfolio/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "NIFTY50", "quantity": 50},
      {"symbol": "RELIANCE", "quantity": 100},
      {"symbol": "TCS", "quantity": 75},
      {"symbol": "BANKNIFTY", "quantity": 25},
      {"symbol": "HDFCBANK", "quantity": 60}
    ],
    "num_simulations": 10000,
    "num_days": 252,
    "confidence_level": 0.995
  }'
```

### ✅ Test 10: Portfolio VaR (Quick Analysis)

**Test quick VaR calculation with indices:**

```bash
curl -X POST "http://localhost:8000/api/portfolio/var" \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "NIFTY50", "quantity": 100},
      {"symbol": "SENSEX", "quantity": 50}
    ],
    "num_simulations": 5000,
    "num_days": 252,
    "confidence_level": 0.995
  }'
```

### ✅ Test 11: VarLytics Special - EGARCH Monte Carlo

**Test VarLytics special endpoints:**

```bash
# EGARCH Monte Carlo on Nifty 50
curl "http://localhost:8000/api/varlytics-special/monte-carlo/NIFTY50?num_simulations=10000&num_days=756"

# EGARCH Skewed-T on Bank Nifty
curl "http://localhost:8000/api/varlytics-special/egarch-skewed-t/BANKNIFTY?num_simulations=10000&num_days=756"
```

### ✅ Test 12: Symbol Aliases

**Test different symbol formats:**

```bash
# All of these should work for Nifty 50:
curl "http://localhost:8000/api/stock/NIFTY"
curl "http://localhost:8000/api/stock/NIFTY50"
curl "http://localhost:8000/api/stock/NIFTY_50"

# All of these should work for Bank Nifty:
curl "http://localhost:8000/api/stock/BANKNIFTY"
curl "http://localhost:8000/api/stock/BANK_NIFTY"
curl "http://localhost:8000/api/stock/NIFTYBANK"
```

### ✅ Test 13: Error Handling

**Test invalid index symbols:**

```bash
# Invalid index
curl "http://localhost:8000/api/stock/INVALIDINDEX"

# Expected: 404 error with message
```

### ✅ Test 14: Backward Compatibility (Stocks)

**Verify stocks still work:**

```bash
# NSE stock
curl "http://localhost:8000/api/stock/RELIANCE"
curl "http://localhost:8000/api/simulations/TCS/monte-carlo?num_simulations=1000&num_days=252"

# BSE stock
curl "http://localhost:8000/api/stock/500325"

# Portfolio with stocks only
curl -X POST "http://localhost:8000/api/portfolio/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "RELIANCE", "quantity": 100},
      {"symbol": "TCS", "quantity": 50}
    ],
    "num_simulations": 5000,
    "num_days": 252
  }'
```

## Using Swagger UI

Alternatively, you can test all endpoints using the Swagger UI:

1. Go to `http://localhost:8000/docs`
2. Find the endpoint you want to test
3. Click "Try it out"
4. Enter parameters (e.g., symbol: "NIFTY50")
5. Click "Execute"
6. View the response

## Expected Performance

- **Single simulation**: < 1 second
- **All 22 simulations (optimized)**: 3-5 seconds
- **Portfolio analysis**: 2-10 seconds (depends on portfolio size and simulations)
- **Search**: < 0.1 seconds

## Common Issues and Solutions

### Issue 1: "No historical data found"
**Cause:** Symbol might be misspelled or not supported
**Solution:** Check symbol spelling, try aliases, or verify in search API first

### Issue 2: Slow response
**Cause:** Too many simulations or long forecast horizon
**Solution:** Start with smaller values (num_simulations=1000, num_days=252)

### Issue 3: Connection timeout
**Cause:** Yahoo Finance might be slow
**Solution:** Retry the request, data is cached after first successful fetch

## Success Criteria

✅ All tests pass
✅ Indices return valid data
✅ Mixed portfolios work
✅ Stocks still work (backward compatibility)
✅ Performance is acceptable (3-5s for all simulations)
✅ Error handling works for invalid symbols

## Testing Completion Report

After running all tests, verify:

- [ ] Search API returns indices with `is_index: true`
- [ ] Fundamentals API works for all major indices
- [ ] Monte Carlo simulation works for indices
- [ ] All 22 simulations work for indices (test optimized batch)
- [ ] Individual GARCH models work
- [ ] Historical simulation works
- [ ] Risk Metrics works
- [ ] Portfolio analysis works with indices only
- [ ] Mixed portfolios (stocks + indices) work
- [ ] Portfolio VaR works with indices
- [ ] VarLytics special endpoints work
- [ ] Symbol aliases work correctly
- [ ] Error handling works
- [ ] Backward compatibility maintained (stocks still work)

## Next Steps After Testing

If all tests pass:
1. ✅ Mark feature as production-ready
2. ✅ Update any frontend components to use indices
3. ✅ Add indices to user documentation
4. ✅ Notify users of new feature

If any tests fail:
1. Check error messages in terminal
2. Verify symbol spelling
3. Check internet connection (Yahoo Finance dependency)
4. Review server logs for detailed errors

