from fastapi import APIRouter, HTTPException
from app.services.nifty_service import (
    get_nifty_summary_and_performance,
    get_nifty_technical_and_risk,
    get_nifty_market_overview,
    get_nifty_events_and_sentiment
)

router = APIRouter(
    prefix="/nifty",
    tags=["Nifty 50"]
)


@router.get("/summary-performance")
def nifty_summary_performance():
    """
    Get comprehensive Nifty 50 summary and performance data.
    
    Includes:
    - Summary Card: Current value, today's change, volume, market cap, P/E ratio, 52-week high/low
    - Performance: Daily, weekly, and monthly performance metrics
    - Historical Data: 1 year of historical data with sample recent data points
    """
    try:
        return get_nifty_summary_and_performance()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/technical-risk")
def nifty_technical_risk():
    """
    Get Nifty 50 technical analysis and risk metrics.
    
    Includes:
    - Technical Indicators: SMA (20, 50, 200), RSI, MACD, Bollinger Bands
    - Volatility: Daily and annual volatility
    - Value at Risk (VaR): 95% and 99% confidence levels with CVaR
    - Risk Metrics: Beta, Alpha, Sharpe Ratio
    """
    try:
        return get_nifty_technical_and_risk()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/market-overview")
def nifty_market_overview():
    """
    Get Nifty 50 market overview and breadth data.
    
    Includes:
    - Market Breadth: Advancing, declining, unchanged stocks with advance-decline ratio
    - Top Gainers: Top 5 gaining stocks in Nifty 50
    - Top Losers: Top 5 losing stocks in Nifty 50
    - Sector Performance: Sector-wise performance breakdown
    """
    try:
        return get_nifty_market_overview()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/events-sentiment")
def nifty_events_sentiment():
    """
    Get Nifty 50 events, earnings reports, and market sentiment.
    
    Includes:
    - Market Sentiment: Overall sentiment analysis with sentiment score
    - News Feed: Latest news articles related to Nifty 50
    - Upcoming Events: Economic events and earnings reports that may impact Nifty 50
    """
    try:
        return get_nifty_events_and_sentiment()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

