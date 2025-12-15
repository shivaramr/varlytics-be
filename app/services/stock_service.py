from pydantic import BaseModel
from app.utils.index_utils import is_index, get_yahoo_symbol
import yfinance as yf
import pandas as pd

# =========================
# FUNDAMENTALS
# =========================

def get_stock_info(yahoo_symbol: str):
    stock = yf.Ticker(yahoo_symbol)
    info = stock.info

    if not info or info.get("longName") is None:
        return None

    return {
        "symbol": yahoo_symbol,
        "longName": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "marketCap": info.get("marketCap"),
        "previousClose": info.get("previousClose"),
        "open": info.get("open"),
        "dayHigh": info.get("dayHigh"),
        "dayLow": info.get("dayLow"),
        "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
        "forwardPE": info.get("forwardPE"),
        "trailingPE": info.get("trailingPE"),
        "dividendYield": info.get("dividendYield"),
        "beta": info.get("beta"),
        "bookValue": info.get("bookValue"),
        "priceToBook": info.get("priceToBook"),
        "earningsPerShare": info.get("epsTrailingTwelveMonths")
    }


def get_stock_fundamentals(symbol: str):
    symbol = symbol.upper()

    if is_index(symbol):
        yahoo_symbol = get_yahoo_symbol(symbol)
        data = get_stock_info(yahoo_symbol)
        if data:
            return data
        raise ValueError(f"Index '{symbol}' data not available.")

    # NSE
    data = get_stock_info(f"{symbol}.NS")
    if data:
        return data

    # BSE
    data = get_stock_info(f"{symbol}.BO")
    if data:
        return data

    # If both fail, raise an error
    raise ValueError(f"Stock symbol '{symbol}' not found on NSE or BSE.")


# =========================
# MACD
# =========================

class MACDRequest(BaseModel):
    symbol: str
    period: str = "6mo"
    interval: str = "1d"


def calculate_macd(df: pd.DataFrame) -> pd.DataFrame:
    df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
    df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["Histogram"] = df["MACD"] - df["Signal"]
    return df


def resolve_yahoo_symbol(symbol: str) -> str:
    """
    Reuse the same NSE/BSE/index logic for MACD
    """
    symbol = symbol.upper()

    if is_index(symbol):
        return get_yahoo_symbol(symbol)

    for suffix in [".NS", ".BO"]:
        test_symbol = f"{symbol}{suffix}"
        data = yf.download(test_symbol, period="5d", progress=False)
        if not data.empty:
            return test_symbol

    raise ValueError(f"Invalid symbol '{symbol}'")


def get_macd_data(symbol: str, period: str, interval: str):
    yahoo_symbol = resolve_yahoo_symbol(symbol)

    stock = yf.download(
        yahoo_symbol,
        period=period,
        interval=interval,
        progress=False
    )

    if stock.empty:
        raise ValueError("No price data available")

    stock = calculate_macd(stock)

    return {
        "symbol": yahoo_symbol,
        "dates": stock.index.strftime("%Y-%m-%d").tolist(),
        "macd": stock["MACD"].round(4).fillna(0).tolist(),
        "signal": stock["Signal"].round(4).fillna(0).tolist(),
        "histogram": stock["Histogram"].round(4).fillna(0).tolist()
    }
