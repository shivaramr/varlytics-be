import yfinance as yf
import pandas as pd
import numpy as np
import feedparser
from datetime import datetime, timedelta
from scipy import stats

# Nifty 50 Yahoo Finance symbol
NIFTY_SYMBOL = "^NSEI"

def get_nifty_summary_and_performance():
    """
    Get Nifty 50 summary card with current value, performance metrics, and historical data
    """
    try:
        nifty = yf.Ticker(NIFTY_SYMBOL)
        info = nifty.info
        
        # Get historical data for performance calculation
        hist_1y = nifty.history(period="1y")
        hist_1mo = nifty.history(period="1mo")
        hist_1wk = nifty.history(period="5d")
        hist_1d = nifty.history(period="1d")
        
        current_price = info.get("regularMarketPrice") or info.get("currentPrice") or hist_1d['Close'].iloc[-1]
        previous_close = info.get("previousClose") or hist_1d['Close'].iloc[-2] if len(hist_1d) > 1 else current_price
        
        # Calculate performance
        today_change = ((current_price - previous_close) / previous_close * 100) if previous_close else 0
        
        weekly_start = hist_1wk['Close'].iloc[0] if len(hist_1wk) > 0 else current_price
        weekly_change = ((current_price - weekly_start) / weekly_start * 100) if weekly_start else 0
        
        monthly_start = hist_1mo['Close'].iloc[0] if len(hist_1mo) > 0 else current_price
        monthly_change = ((current_price - monthly_start) / monthly_start * 100) if monthly_start else 0
        
        # Get 52-week high/low
        fifty_two_week_high = info.get("fiftyTwoWeekHigh") or hist_1y['High'].max()
        fifty_two_week_low = info.get("fiftyTwoWeekLow") or hist_1y['Low'].min()
        
        # Volume and market cap
        volume = info.get("volume") or hist_1d['Volume'].iloc[-1] if len(hist_1d) > 0 else 0
        market_cap = info.get("marketCap", "N/A")
        
        # P/E Ratio
        pe_ratio = info.get("trailingPE") or info.get("forwardPE", "N/A")
        
        result = {
            "summary_card": {
                "current_value": round(current_price, 2),
                "today_change_percent": round(today_change, 2),
                "volume": int(volume) if volume else 0,
                "market_cap": market_cap,
                "pe_ratio": round(pe_ratio, 2) if isinstance(pe_ratio, (int, float)) else pe_ratio,
                "52_week_high": round(fifty_two_week_high, 2),
                "52_week_low": round(fifty_two_week_low, 2)
            },
            "performance": {
                "daily_change_percent": round(today_change, 2),
                "weekly_change_percent": round(weekly_change, 2),
                "monthly_change_percent": round(monthly_change, 2)
            },
            "historical_data": {
                "period": "1 year",
                "data_points": len(hist_1y),
                "sample_recent": [
                    {
                        "date": str(date.date()),
                        "open": round(row['Open'], 2),
                        "high": round(row['High'], 2),
                        "low": round(row['Low'], 2),
                        "close": round(row['Close'], 2),
                        "volume": int(row['Volume'])
                    }
                    for date, row in hist_1y.tail(90).iterrows()
                ]
            }
        }
        
        return result
    except Exception as e:
        raise ValueError(f"Error fetching Nifty 50 data: {str(e)}")


def get_nifty_technical_and_risk():
    """
    Get Nifty 50 technical indicators, volatility, VaR, Beta, and Alpha
    """
    try:
        nifty = yf.Ticker(NIFTY_SYMBOL)
        hist = nifty.history(period="1y")
        
        if hist.empty:
            raise ValueError("No historical data available")
        
        # Calculate returns
        hist['Returns'] = hist['Close'].pct_change()
        
        # Technical Indicators
        # Moving Averages
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
        
        # RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # MACD
        ema_12 = hist['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = hist['Close'].ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9, adjust=False).mean()
        
        # Bollinger Bands
        bb_middle = hist['Close'].rolling(window=20).mean()
        bb_std = hist['Close'].rolling(window=20).std()
        bb_upper = bb_middle + (bb_std * 2)
        bb_lower = bb_middle - (bb_std * 2)
        
        current_price = hist['Close'].iloc[-1]
        
        # Volatility
        daily_volatility = hist['Returns'].std()
        annual_volatility = daily_volatility * np.sqrt(252)
        
        # VaR Calculation (95% and 99% confidence)
        confidence_95 = 0.95
        confidence_99 = 0.99
        returns = hist['Returns'].dropna()
        
        var_95 = np.percentile(returns, (1 - confidence_95) * 100)
        var_99 = np.percentile(returns, (1 - confidence_99) * 100)
        
        # CVaR (Expected Shortfall)
        cvar_95 = returns[returns <= var_95].mean()
        cvar_99 = returns[returns <= var_99].mean()
        
        # Beta and Alpha calculation (using market proxy as NIFTY itself, so Beta=1, Alpha=0)
        # For real calculation, we'd compare against a risk-free rate
        info = nifty.info
        beta = info.get("beta", 1.0)  # Nifty vs itself is 1
        
        # Alpha calculation (simplified)
        mean_return = returns.mean() * 252  # Annualized
        risk_free_rate = 0.07  # Assuming 7% risk-free rate (Indian context)
        alpha = mean_return - risk_free_rate
        
        result = {
            "technical_indicators": {
                "current_price": round(current_price, 2),
                "sma_20": round(hist['SMA_20'].iloc[-1], 2) if not pd.isna(hist['SMA_20'].iloc[-1]) else None,
                "sma_50": round(hist['SMA_50'].iloc[-1], 2) if not pd.isna(hist['SMA_50'].iloc[-1]) else None,
                "sma_200": round(hist['SMA_200'].iloc[-1], 2) if not pd.isna(hist['SMA_200'].iloc[-1]) else None,
                "rsi_14": round(rsi.iloc[-1], 2) if not pd.isna(rsi.iloc[-1]) else None,
                "macd": round(macd.iloc[-1], 2) if not pd.isna(macd.iloc[-1]) else None,
                "macd_signal": round(signal.iloc[-1], 2) if not pd.isna(signal.iloc[-1]) else None,
                "bollinger_upper": round(bb_upper.iloc[-1], 2) if not pd.isna(bb_upper.iloc[-1]) else None,
                "bollinger_middle": round(bb_middle.iloc[-1], 2) if not pd.isna(bb_middle.iloc[-1]) else None,
                "bollinger_lower": round(bb_lower.iloc[-1], 2) if not pd.isna(bb_lower.iloc[-1]) else None
            },
            "volatility": {
                "daily_volatility_percent": round(daily_volatility * 100, 2),
                "annual_volatility_percent": round(annual_volatility * 100, 2)
            },
            "value_at_risk": {
                "var_95_percent": round(var_95 * 100, 2),
                "var_99_percent": round(var_99 * 100, 2),
                "cvar_95_percent": round(cvar_95 * 100, 2),
                "cvar_99_percent": round(cvar_99 * 100, 2),
                "confidence_levels": "95% and 99%"
            },
            "risk_metrics": {
                "beta": round(beta, 2),
                "alpha_percent": round(alpha * 100, 2),
                "sharpe_ratio": round((mean_return - risk_free_rate) / annual_volatility, 2) if annual_volatility > 0 else 0
            }
        }
        
        return result
    except Exception as e:
        raise ValueError(f"Error calculating technical and risk metrics: {str(e)}")


def get_nifty_market_overview():
    """
    Get Nifty 50 market breadth, top gainers/losers, and sector performance
    """
    try:
        # Nifty 50 constituents (sample list - in production, fetch from live source)
        nifty_50_constituents = [
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
            "ICICIBANK.NS", "KOTAKBANK.NS", "SBIN.NS", "BHARTIARTL.NS", "BAJFINANCE.NS",
            "ITC.NS", "ASIANPAINT.NS", "MARUTI.NS", "LT.NS", "AXISBANK.NS",
            "HCLTECH.NS", "WIPRO.NS", "ULTRACEMCO.NS", "TITAN.NS", "SUNPHARMA.NS",
            "NESTLEIND.NS", "BAJAJFINSV.NS", "POWERGRID.NS", "NTPC.NS", "ONGC.NS",
            "M&M.NS", "TATAMOTORS.NS", "TECHM.NS", "ADANIPORTS.NS", "COALINDIA.NS",
            "TATASTEEL.NS", "DIVISLAB.NS", "DRREDDY.NS", "GRASIM.NS", "HINDALCO.NS",
            "INDUSINDBK.NS", "JSWSTEEL.NS", "BRITANNIA.NS", "CIPLA.NS", "EICHERMOT.NS",
            "HEROMOTOCO.NS", "BPCL.NS", "APOLLOHOSP.NS", "TATACONSUM.NS", "UPL.NS",
            "BAJAJ-AUTO.NS", "SBILIFE.NS", "HDFCLIFE.NS", "ADANIENT.NS", "LTIM.NS"
        ]
        
        # Fetch data for all constituents
        gainers = []
        losers = []
        sector_performance = {}
        advancing = 0
        declining = 0
        unchanged = 0
        
        for symbol in nifty_50_constituents[:20]:  # Limit to 20 for performance
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period="2d")
                info = stock.info
                
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change_percent = ((current - previous) / previous * 100)
                    
                    stock_data = {
                        "symbol": symbol.replace(".NS", ""),
                        "name": info.get("longName", symbol),
                        "current_price": round(current, 2),
                        "change_percent": round(change_percent, 2),
                        "sector": info.get("sector", "Unknown")
                    }
                    
                    if change_percent > 0:
                        advancing += 1
                        gainers.append(stock_data)
                    elif change_percent < 0:
                        declining += 1
                        losers.append(stock_data)
                    else:
                        unchanged += 1
                    
                    # Aggregate sector performance
                    sector = info.get("sector", "Unknown")
                    if sector not in sector_performance:
                        sector_performance[sector] = {"total_change": 0, "count": 0}
                    sector_performance[sector]["total_change"] += change_percent
                    sector_performance[sector]["count"] += 1
            except:
                continue
        
        # Sort gainers and losers
        gainers.sort(key=lambda x: x["change_percent"], reverse=True)
        losers.sort(key=lambda x: x["change_percent"])
        
        # Calculate sector averages
        sector_summary = [
            {
                "sector": sector,
                "avg_change_percent": round(data["total_change"] / data["count"], 2),
                "stocks_count": data["count"]
            }
            for sector, data in sector_performance.items()
        ]
        sector_summary.sort(key=lambda x: x["avg_change_percent"], reverse=True)
        
        result = {
            "market_breadth": {
                "advancing": advancing,
                "declining": declining,
                "unchanged": unchanged,
                "advance_decline_ratio": round(advancing / declining, 2) if declining > 0 else "N/A",
                "total_stocks_analyzed": advancing + declining + unchanged
            },
            "top_gainers": gainers[:5],
            "top_losers": losers[:5],
            "sector_performance": sector_summary
        }
        
        return result
    except Exception as e:
        raise ValueError(f"Error fetching market overview: {str(e)}")


def get_nifty_events_and_sentiment():
    """
    Get upcoming economic events, earnings reports, and market sentiment for Nifty 50
    """
    try:
        nifty = yf.Ticker(NIFTY_SYMBOL)
        
        # Get recent news
        news = nifty.news if hasattr(nifty, 'news') else []
        
        news_feed = []
        if news:
            for article in news[:10]:  # Limit to 10 articles
                content = article.get("content", {})
                provider = content.get("provider", {})
                click_through = content.get("clickThroughUrl", {})
                thumbnail_data = content.get("thumbnail", {})
                
                # Parse pubDate (ISO format string)
                pub_date_str = content.get("pubDate", "")
                try:
                    if pub_date_str:
                        pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                        formatted_date = pub_date.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        formatted_date = None
                except:
                    formatted_date = pub_date_str
                
                # Extract thumbnail - prefer smaller resolution for performance
                thumbnail_url = None
                if thumbnail_data:
                    resolutions = thumbnail_data.get("resolutions", [])
                    if resolutions:
                        # Try to get the smaller resolution (170x128) or fallback to original
                        small_res = next((r for r in resolutions if r.get("tag") == "170x128"), None)
                        if small_res:
                            thumbnail_url = small_res.get("url")
                        else:
                            # Fallback to original URL
                            thumbnail_url = thumbnail_data.get("originalUrl")
                
                news_feed.append({
                    "title": content.get("title", ""),
                    "publisher": provider.get("displayName", ""),
                    "link": click_through.get("url", ""),
                    "published_date": formatted_date,
                    "summary": content.get("summary", ""),
                    "thumbnail": thumbnail_url
                })
        
        # Calculate sentiment score based on recent performance
        hist = nifty.history(period="5d")
        returns = hist['Close'].pct_change().dropna()
        
        avg_return = returns.mean()
        if avg_return > 0.005:
            sentiment = "Bullish"
            sentiment_score = min(100, 50 + (avg_return * 1000))
        elif avg_return < -0.005:
            sentiment = "Bearish"
            sentiment_score = max(0, 50 + (avg_return * 1000))
        else:
            sentiment = "Neutral"
            sentiment_score = 50
        
        # Upcoming events from Google News RSS for Nifty50
        upcoming_events = []
        try:
            rss_url = "https://news.google.com/rss/search?q=Nifty50+earnings+OR+RBI+OR+economic+data&hl=en-IN&gl=IN&ceid=IN:en"
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:5]:  # Limit to top 5
                # Parse published date
                published_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M:%S")
                elif hasattr(entry, 'published'):
                    published_date = entry.published

                upcoming_events.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published_date": published_date,
                    "source": entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else "Google News"
                })
        except Exception as e:
            # Fallback to static data if RSS fails
            upcoming_events = [
                {
                    "title": "RBI Monetary Policy Meeting",
                    "link": "https://www.rbi.org.in/",
                    "published_date": "2025-10-15",
                    "source": "Reserve Bank of India"
                },
                {
                    "title": "CPI Inflation Data Release",
                    "link": "https://www.mospi.gov.in/",
                    "published_date": "2025-10-12",
                    "source": "Ministry of Statistics"
                }
            ]
        
        result = {
            "market_sentiment": {
                "overall_sentiment": sentiment,
                "sentiment_score": round(sentiment_score, 2),
                "description": f"Based on recent 5-day performance analysis"
            },
            "news_feed": news_feed,
            "upcoming_events": upcoming_events
        }
        
        return result
    except Exception as e:
        raise ValueError(f"Error fetching events and sentiment: {str(e)}")

