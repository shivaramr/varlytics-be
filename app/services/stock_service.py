import yfinance as yf
from app.utils.index_utils import is_index, get_yahoo_symbol

def get_stock_info(yahoo_symbol: str):
    stock = yf.Ticker(yahoo_symbol)
    info = stock.info

    # Check if the response contains valid data
    if not info or info.get("longName") is None:
        return None

    # Extract fundamental data
    result = {
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

    return result


def get_stock_fundamentals(symbol: str):
    symbol = symbol.upper()

    # Check if it's an index first
    if is_index(symbol):
        yahoo_symbol = get_yahoo_symbol(symbol)
        data = get_stock_info(yahoo_symbol)
        if data:
            return data
        raise ValueError(f"Index '{symbol}' data not available.")

    # For stocks, try NSE first
    nse_symbol = f"{symbol}.NS"
    data = get_stock_info(nse_symbol)

    if data:
        return data

    # If NSE fails, try BSE
    bse_symbol = f"{symbol}.BO"
    data = get_stock_info(bse_symbol)

    if data:
        return data

    # If both fail, raise an error
    raise ValueError(f"Stock symbol '{symbol}' not found on NSE or BSE.")
