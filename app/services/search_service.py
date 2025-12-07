import pandas as pd
import requests
from io import StringIO

from app.data.stock_data import FALLBACK_STOCKS, FALLBACK_INDICES, FALLBACK_ALL
from app.utils.index_utils import INDIAN_INDICES, is_index

# Cache for stock data
_stock_cache = None


def _load_stock_data():
    """Load and cache NSE and BSE stock data plus indices"""
    global _stock_cache

    if _stock_cache is not None:
        return _stock_cache

    stock_dict = {}

    # Add all indices to the dictionary
    for key, info in FALLBACK_INDICES.items():
        stock_dict[key] = {
            "name": info["name"],
            "sub_symbol": info["sub_symbol"],
            "is_index": True,
            "exchange": info.get("exchange", "NSE"),
        }

    # --- NSE STOCKS ---
    try:
        url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            df.columns = df.columns.str.strip()

            for _, row in df.iterrows():
                symbol = str(row["SYMBOL"]).strip()
                name = str(row["NAME OF COMPANY"]).strip()

                # Skip mutual funds and ETFs
                if "MUTUAL FUND" in name.upper() or "ETF" in name.upper():
                    continue

                key = f"{symbol}"
                if key not in stock_dict:
                    stock_dict[key] = {
                        "name": name,
                        "sub_symbol": None,
                        "is_index": False,
                    }

            print(f"Loaded {len(stock_dict)} NSE stocks and indices")
    except Exception as e:
        print(f"Failed to load from NSE: {str(e)}")

    # --- BSE STOCKS ---
    try:
        url = "http://content.indiainfoline.com/IIFLTT/Scripmaster.csv"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            df.columns = df.columns.str.strip()

            # Filter for equity (cash segment) stocks only
            bse_equities = df[
                (df["Exch"] == "B")
                & (df["ExchType"] == "C")
                & (df["Series"].isin(['EQ', 'BE', 'BZ']))
            ]

            bse_count = 0
            for _, row in bse_equities.iterrows():
                scripcode = str(row["Scripcode"]).strip()
                sub_symbol = str(row["Name"]).strip()
                name = str(row["FullName"]).strip()

                # Skip mutual funds or ETFs
                if "MUTUAL FUND" in name.upper() or "ETF" in name.upper():
                    continue

                key = scripcode
                if key not in stock_dict and scripcode and name:
                    stock_dict[key] = {
                        "name": name,
                        "sub_symbol": sub_symbol,
                        "is_index": False,
                    }
                    bse_count += 1

            print(f"Loaded {bse_count} BSE-only stocks. Total stocks: {len(stock_dict)}")
    except Exception as e:
        print(f"Failed to load from BSE: {str(e)}")

    # If we got valid data, cache and return
    if stock_dict:
        _stock_cache = stock_dict
        return stock_dict

    # Fallback: Use a comprehensive list of major Indian stocks and indices
    fallback_with_indices = {}

    # Add indices first
    for key, info in FALLBACK_INDICES.items():
        fallback_with_indices[key] = {
            "name": info["name"],
            "sub_symbol": info["sub_symbol"],
            "is_index": True,
            "exchange": info.get("exchange", "NSE"),
        }

    # Add stocks
    for key, info in FALLBACK_STOCKS.items():
        fallback_with_indices[key] = {
            "name": info["name"],
            "sub_symbol": info.get("sub_symbol"),
            "is_index": False,
        }

    _stock_cache = fallback_with_indices
    return fallback_with_indices


def search_stocks(query: str):
    """
    Search for stocks and indices in NSE and BSE based on symbol or company name.
    Returns a list of matching stocks/indices with symbol, name, and sub_symbol (for BSE).
    """
    if not query:
        return []

    query = query.upper().strip()
    results = []

    try:
        # Load stock data
        stock_data = _load_stock_data()

        # Search through stocks
        for symbol, data in stock_data.items():
            if not symbol or not data:
                continue

            name = data.get("name", "")
            sub_symbol = data.get("sub_symbol")
            is_idx = data.get("is_index", False)

            if not name:
                continue

            symbol_upper = symbol.upper()
            name_upper = name.upper()
            sub_symbol_upper = sub_symbol.upper() if sub_symbol else ""

            if (
                query in symbol_upper
                or query in name_upper
                or (sub_symbol and query in sub_symbol_upper)
            ):
                result = {
                    "symbol": symbol,
                    "name": name.title() if not is_idx else name,
                    "is_index": is_idx,
                }

                if sub_symbol:
                    result["sub_symbol"] = sub_symbol

                results.append(result)

        # Sorting function
        def sort_key(item):
            symbol = item["symbol"].upper()
            sub_symbol = item.get("sub_symbol", "").upper()
            is_idx = item.get("is_index", False)

            if is_idx:
                if symbol == query or sub_symbol == query:
                    return (0, 0, len(symbol), symbol)
                elif symbol.startswith(query) or sub_symbol.startswith(query):
                    return (0, 1, len(symbol), symbol)
                else:
                    return (0, 2, len(symbol), symbol)

            if symbol == query or sub_symbol == query:
                return (1, 0, len(symbol), symbol)
            elif symbol.startswith(query) or sub_symbol.startswith(query):
                return (1, 1, len(symbol), symbol)
            else:
                return (1, 2, len(symbol), symbol)

        results.sort(key=sort_key)

        # Limit to top 20 results
        return results[:20]

    except Exception as e:
        print(f"Error searching stocks: {str(e)}")
        return []
