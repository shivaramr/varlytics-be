# VarLytics Backend

A comprehensive portfolio risk analysis and stock simulation API for Indian markets (NSE, BSE) and market indices.

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Initialise virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install uvicorn
pip install uvicorn

# Install fastapi
pip install fastapi

# Run the server
uvicorn app.main:app --reload
```

### Access API Documentation

**Swagger UI:** http://127.0.0.1:8000/docs

## ✨ Features

### 📊 **Market Coverage**
- **NSE Stocks**: All NSE-listed stocks
- **BSE Stocks**: All BSE-listed stocks
- **Market Indices**: 
  - Nifty 50, Bank Nifty, Nifty IT, Nifty Pharma, Nifty Auto, and more
  - Sensex, BSE 100, BSE 200, BSE 500
  - See [INDEX_SUPPORT_README.md](INDEX_SUPPORT_README.md) for complete list

### 🔍 **Search & Discovery**
- Smart search for stocks and indices
- Fuzzy matching and autocomplete support
- Prioritized results (indices first, exact matches, partial matches)

### 📈 **Portfolio Analysis**
- Comprehensive portfolio risk metrics
- Multiple VaR calculation methods:
  - Variance-Covariance VaR
  - Historical Simulation VaR
  - Monte Carlo VaR
  - Conditional VaR (CVaR/Expected Shortfall)
- Support for mixed portfolios (stocks + indices)
- Stress testing scenarios
- Portfolio composition analysis

### 🎲 **Simulation Models** (22 Models)
All simulation models support both stocks and indices:

**GARCH Models** (6 variants):
- GARCH with Normal distribution
- GARCH with Student-t distribution
- GARCH with GED distribution
- GARCH with Skewed-Normal
- GARCH with Skewed-t
- GARCH with Skewed-GED

**EGARCH Models** (6 variants):
- EGARCH with all distributions above

**GJR-GARCH Models** (6 variants):
- GJR-GARCH with all distributions above

**Classical Models** (4 models):
- Historical Simulation
- Monte Carlo Simulation
- RiskMetrics (EWMA)
- Simple Variance

### ⚡ **Performance**
- Ultra-optimized batch simulations: **3-5 seconds** for all 22 models
- Parallel execution for portfolio analysis
- Smart caching (VIX data, stock data)
- Efficient data fetching with fallback mechanisms

## 📚 API Endpoints

### General
- `GET /api/search?query={query}` - Search stocks and indices

### Stock/Index Fundamentals
- `GET /api/stock/{symbol}` - Get fundamental data

### Portfolio Analysis
- `POST /api/portfolio/analyze` - Comprehensive portfolio analysis
- `POST /api/portfolio/var` - Quick VaR calculation
- `GET /api/portfolio/example` - Get example portfolio

### Simulations
- `GET /api/simulations/{symbol}/all` - Run all 22 simulations
- `GET /api/simulations/{symbol}/{simulation_type}` - Run specific simulation
- `GET /api/simulations/available` - List all available simulations

### VarLytics Special
- `GET /api/varlytics-special/monte-carlo/{symbol}` - EGARCH Monte Carlo
- `GET /api/varlytics-special/egarch-skewed-t/{symbol}` - EGARCH Skewed-T

## 📖 Usage Examples

### Search for an Index
```bash
curl "http://localhost:8000/api/search?query=nifty"
```

### Get Nifty 50 Fundamentals
```bash
curl "http://localhost:8000/api/stock/NIFTY50"
```

### Run Monte Carlo Simulation on Bank Nifty
```bash
curl "http://localhost:8000/api/simulations/BANKNIFTY/monte-carlo?num_simulations=10000&num_days=252"
```

### Analyze Mixed Portfolio
```bash
curl -X POST "http://localhost:8000/api/portfolio/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "NIFTY50", "quantity": 100},
      {"symbol": "RELIANCE", "quantity": 75},
      {"symbol": "TCS", "quantity": 60}
    ],
    "num_simulations": 10000,
    "num_days": 252,
    "confidence_level": 0.995
  }'
```

## 🗂️ Project Structure

```
varlytics-be/
├── app/
│   ├── api/              # API endpoint definitions
│   ├── services/         # Business logic
│   │   └── simulations/  # 22 simulation models
│   ├── data/             # Fallback data
│   ├── utils/            # Utility functions
│   │   ├── index_utils.py      # Index mapping utilities
│   │   ├── vix_cache.py        # VIX caching
│   │   └── chart_utils.py      # Chart data generation
│   └── main.py           # FastAPI app
├── requirements.txt
└── README.md
```

## 📄 Documentation

- [INDEX_SUPPORT_README.md](INDEX_SUPPORT_README.md) - Complete guide to index support
- [PORTFOLIO_API_README.md](PORTFOLIO_API_README.md) - Portfolio API documentation
- [QUICK_START.md](QUICK_START.md) - Quick start guide
- [INSTALLATION.md](INSTALLATION.md) - Detailed installation instructions

## 🔧 Configuration

The API uses:
- **Yahoo Finance** for stock and index data
- **India VIX** for volatility data (cached for 24 hours)
- **FastAPI** framework
- **arch** library for GARCH models
- **numpy**, **pandas**, **scipy** for calculations

## 🎯 Key Features

### Symbol Flexibility
```python
# All of these work for Nifty 50:
"NIFTY", "NIFTY50", "NIFTY_50", "^NSEI"

# All of these work for Bank Nifty:
"BANKNIFTY", "BANK_NIFTY", "NIFTYBANK", "^NSEBANK"
```

### Smart Fallback
- Tries NSE first for stocks (`.NS` suffix)
- Falls back to BSE if NSE fails (`.BO` suffix)
- Direct Yahoo Finance symbols for indices

### Mixed Portfolios
- Combine stocks and indices in the same portfolio
- Seamless correlation analysis
- Unified risk metrics

## 🧪 Testing

```bash
# Test search
curl "http://localhost:8000/api/search?query=nifty"

# Test fundamentals
curl "http://localhost:8000/api/stock/NIFTY50"

# Test simulation
curl "http://localhost:8000/api/simulations/NIFTY50/monte-carlo?num_simulations=1000&num_days=252"
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is private and confidential.

## 🆕 Recent Updates

### Index Support (Latest)
- ✅ Support for 15+ NSE indices (Nifty 50, Bank Nifty, sectoral indices)
- ✅ Support for 4+ BSE indices (Sensex, BSE 100, 200, 500)
- ✅ All 22 simulation models work with indices
- ✅ Portfolio analysis with mixed stocks and indices
- ✅ Smart search with index prioritization

See [INDEX_SUPPORT_README.md](INDEX_SUPPORT_README.md) for complete details.

## 📞 Support

For issues or questions, please contact the development team.
