# Indian Market Indices Support

## Overview

All APIs in the VarLytics backend now support Indian market indices in addition to NSE and BSE stocks. You can now analyze indices like Nifty 50, Sensex, Bank Nifty, IT, and many more using all available endpoints.

## Supported Indices

### NSE Indices

| Index Name | Symbol | Description |
|------------|--------|-------------|
| Nifty 50 | `NIFTY50`, `NIFTY`, `NIFTY_50` | NSE's benchmark index |
| Bank Nifty | `BANKNIFTY`, `BANK_NIFTY`, `NIFTYBANK` | Banking sector index |
| Nifty IT | `NIFTYIT`, `NIFTY_IT` | IT sector index |
| Nifty Pharma | `NIFTYPHARMA`, `NIFTY_PHARMA` | Pharma sector index |
| Nifty Auto | `NIFTYAUTO`, `NIFTY_AUTO` | Auto sector index |
| Nifty FMCG | `NIFTYFMCG`, `NIFTY_FMCG` | FMCG sector index |
| Nifty Metal | `NIFTYMETAL`, `NIFTY_METAL` | Metal sector index |
| Nifty Realty | `NIFTYREALTY`, `NIFTY_REALTY` | Realty sector index |
| Nifty Energy | `NIFTYENERGY`, `NIFTY_ENERGY` | Energy sector index |
| Nifty Infrastructure | `NIFTYINFRA`, `NIFTY_INFRA` | Infrastructure index |
| Nifty PSE | `NIFTYPSE`, `NIFTY_PSE` | Public sector enterprises |
| Nifty Next 50 | `NIFTYNEXT50`, `NIFTY_NEXT_50` | Next 50 largest companies |
| Nifty 100 | `NIFTY100`, `NIFTY_100` | Top 100 companies |
| Nifty 200 | `NIFTY200`, `NIFTY_200` | Top 200 companies |
| Nifty 500 | `NIFTY500`, `NIFTY_500` | Top 500 companies |

### BSE Indices

| Index Name | Symbol | Description |
|------------|--------|-------------|
| Sensex | `SENSEX` | BSE's benchmark index |
| BSE 100 | `BSE100`, `BSE_100` | Top 100 companies |
| BSE 200 | `BSE200`, `BSE_200` | Top 200 companies |
| BSE 500 | `BSE500`, `BSE_500` | Top 500 companies |

## API Usage Examples

### 1. Search API

Search for indices by name or symbol:

```bash
# Search for Nifty
GET /api/search?query=nifty

# Response includes indices with is_index flag:
{
  "results": [
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
}
```

### 2. Stock/Index Fundamentals API

Get fundamental data for any index:

```bash
# Get Nifty 50 fundamentals
GET /api/stock/NIFTY50

# Get Sensex fundamentals
GET /api/stock/SENSEX

# Get Bank Nifty fundamentals
GET /api/stock/BANKNIFTY
```

### 3. Portfolio Analysis API

Include indices in your portfolio:

```bash
POST /api/portfolio/analyze

{
  "holdings": [
    {"symbol": "NIFTY50", "quantity": 100},
    {"symbol": "BANKNIFTY", "quantity": 50},
    {"symbol": "RELIANCE", "quantity": 75},
    {"symbol": "TCS", "quantity": 60}
  ],
  "num_simulations": 10000,
  "num_days": 252,
  "confidence_level": 0.995
}
```

### 4. Simulations API

Run any simulation on indices:

```bash
# Run all simulations on Nifty 50
GET /api/simulations/NIFTY50/all?num_simulations=10000&num_days=252

# Run specific simulation on Bank Nifty
GET /api/simulations/BANKNIFTY/garch-t?num_simulations=10000&num_days=252

# Run Monte Carlo on Sensex
GET /api/simulations/SENSEX/monte-carlo?num_simulations=10000&num_days=252
```

Available simulation types for indices:
- All 22 GARCH variants (GARCH, EGARCH, GJR-GARCH with different distributions)
- Historical simulation
- Monte Carlo simulation
- Risk Metrics (EWMA)
- Simple Variance

### 5. VarLytics Special API

Special EGARCH simulations for indices:

```bash
# EGARCH Monte Carlo on Nifty 50
GET /api/varlytics-special/monte-carlo/NIFTY50?num_simulations=10000&num_days=756

# EGARCH Skewed-T on Bank Nifty
GET /api/varlytics-special/egarch-skewed-t/BANKNIFTY?num_simulations=10000&num_days=756
```

## How It Works

### Symbol Resolution

The system automatically detects if a symbol is an index and uses the correct Yahoo Finance symbol:

```python
# User Input: "NIFTY50" or "NIFTY" or "NIFTY_50"
# System resolves to: "^NSEI"

# User Input: "SENSEX"
# System resolves to: "^BSESN"

# User Input: "BANKNIFTY"
# System resolves to: "^NSEBANK"
```

### Backwards Compatibility

All existing stock APIs continue to work exactly as before:

```bash
# NSE stocks
GET /api/stock/RELIANCE
GET /api/simulations/TCS/all

# BSE stocks (by scrip code)
GET /api/stock/500325
```

## Technical Details

### New Utility Module

**File:** `app/utils/index_utils.py`

Contains:
- `INDIAN_INDICES`: Comprehensive mapping of index symbols to Yahoo Finance symbols
- `is_index(symbol)`: Check if a symbol is an index
- `get_yahoo_symbol(symbol)`: Get Yahoo Finance symbol for an index
- `get_index_info(symbol)`: Get detailed information about an index
- `get_all_indices()`: List all available indices

### Updated Services

All services have been updated to handle indices:

1. **Search Service** (`app/services/search_service.py`)
   - Includes indices in search results
   - Prioritizes indices in search results
   - Adds `is_index` flag to results

2. **Stock Service** (`app/services/stock_service.py`)
   - Checks for indices before trying NSE/BSE
   - Returns fundamental data for indices

3. **Portfolio Service** (`app/services/portfolio_service.py`)
   - Handles indices in portfolio holdings
   - Fetches historical data for indices

4. **Simulation Services** (all simulation files)
   - Support indices in all 22 simulation models
   - Optimized batch service handles indices
   - Historical, Monte Carlo, Risk Metrics, and Simple Variance support

5. **VarLytics Special Services**
   - EGARCH Monte Carlo for indices
   - EGARCH Skewed-T for indices

### Data Fetching Strategy

```python
def fetch_data(symbol):
    if is_index(symbol):
        # Use direct Yahoo Finance symbol
        yahoo_symbol = get_yahoo_symbol(symbol)  # e.g., "^NSEI"
        return fetch_from_yahoo(yahoo_symbol)
    else:
        # Try NSE first, then BSE
        try:
            return fetch_from_yahoo(f"{symbol}.NS")
        except:
            return fetch_from_yahoo(f"{symbol}.BO")
```

## Mixed Portfolio Example

You can now create portfolios with both stocks and indices:

```bash
POST /api/portfolio/analyze

{
  "holdings": [
    {"symbol": "NIFTY50", "quantity": 100},      # Index
    {"symbol": "BANKNIFTY", "quantity": 50},      # Index
    {"symbol": "RELIANCE", "quantity": 75},       # NSE Stock
    {"symbol": "TCS", "quantity": 60},            # NSE Stock
    {"symbol": "HDFCBANK", "quantity": 80},       # NSE Stock
    {"symbol": "SENSEX", "quantity": 30}          # BSE Index
  ],
  "num_simulations": 10000,
  "num_days": 252,
  "confidence_level": 0.995
}
```

## Performance

Index data fetching is as fast as stock data fetching since both use Yahoo Finance. All optimizations remain intact:

- Ultra-optimized batch simulations: 3-5 seconds for all 22 simulations
- Parallel execution for portfolio analysis
- VIX caching (24-hour cache)
- Stock data caching for repeated requests

## Testing

To test index support:

```bash
# 1. Search for an index
curl "http://localhost:8000/api/search?query=nifty"

# 2. Get index fundamentals
curl "http://localhost:8000/api/stock/NIFTY50"

# 3. Run simulation on index
curl "http://localhost:8000/api/simulations/NIFTY50/monte-carlo?num_simulations=1000&num_days=252"

# 4. Analyze portfolio with indices
curl -X POST "http://localhost:8000/api/portfolio/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "NIFTY50", "quantity": 100},
      {"symbol": "RELIANCE", "quantity": 50}
    ],
    "num_simulations": 5000,
    "num_days": 252
  }'
```

## Notes

- All index symbols are case-insensitive
- Multiple aliases are supported (e.g., `NIFTY`, `NIFTY50`, `NIFTY_50` all work)
- Indices appear at the top of search results
- Portfolio analysis works seamlessly with mixed stocks and indices
- All 22 simulation models support indices

## Future Enhancements

Potential future additions:
- More sectoral indices (Consumer Durables, Media, etc.)
- International indices
- Custom index creation from portfolios
- Index comparison tools

