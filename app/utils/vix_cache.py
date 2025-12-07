from datetime import datetime, timedelta
import yfinance as yf

# Global cache dictionary
vix_cache = {
    "value": None,
    "last_updated": None
}

def get_vix_value(symbol: str = "^INDIAVIX") -> float | None:
    """
    Fetch and cache VIX index value once every 24 hours.
    """
    now = datetime.utcnow()

    # Return cached value if less than 24 hours old
    if vix_cache["value"] is not None and vix_cache["last_updated"]:
        if now - vix_cache["last_updated"] < timedelta(hours=24):
            return vix_cache["value"]

    # Fetch new value from Yahoo Finance
    try:
        vix_data = yf.Ticker(symbol).history(period="5d")
        latest_vix = float(vix_data["Close"].iloc[-1])
        vix_cache["value"] = latest_vix
        vix_cache["last_updated"] = now
        return latest_vix
    except Exception as e:
        print(f"[VIX Fetch Error]: {e}")
        return None
