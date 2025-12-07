"""
Utility functions for handling Indian market indices.
Maps common index names to their Yahoo Finance symbols.
"""

# Comprehensive mapping of Indian market indices to Yahoo Finance symbols
INDIAN_INDICES = {
    # NSE Indices
    "NIFTY": {"symbol": "^NSEI", "name": "Nifty 50", "exchange": "NSE"},
    "NIFTY50": {"symbol": "^NSEI", "name": "Nifty 50", "exchange": "NSE"},
    "NIFTY_50": {"symbol": "^NSEI", "name": "Nifty 50", "exchange": "NSE"},
    "^NSEI": {"symbol": "^NSEI", "name": "Nifty 50", "exchange": "NSE"},
    
    "BANKNIFTY": {"symbol": "^NSEBANK", "name": "Bank Nifty", "exchange": "NSE"},
    "BANK_NIFTY": {"symbol": "^NSEBANK", "name": "Bank Nifty", "exchange": "NSE"},
    "NIFTYBANK": {"symbol": "^NSEBANK", "name": "Bank Nifty", "exchange": "NSE"},
    "^NSEBANK": {"symbol": "^NSEBANK", "name": "Bank Nifty", "exchange": "NSE"},
    
    "NIFTYIT": {"symbol": "^CNXIT", "name": "Nifty IT", "exchange": "NSE"},
    "NIFTY_IT": {"symbol": "^CNXIT", "name": "Nifty IT", "exchange": "NSE"},
    "^CNXIT": {"symbol": "^CNXIT", "name": "Nifty IT", "exchange": "NSE"},
    
    "NIFTYPHARMA": {"symbol": "^CNXPHARMA", "name": "Nifty Pharma", "exchange": "NSE"},
    "NIFTY_PHARMA": {"symbol": "^CNXPHARMA", "name": "Nifty Pharma", "exchange": "NSE"},
    "^CNXPHARMA": {"symbol": "^CNXPHARMA", "name": "Nifty Pharma", "exchange": "NSE"},
    
    "NIFTYAUTO": {"symbol": "^CNXAUTO", "name": "Nifty Auto", "exchange": "NSE"},
    "NIFTY_AUTO": {"symbol": "^CNXAUTO", "name": "Nifty Auto", "exchange": "NSE"},
    "^CNXAUTO": {"symbol": "^CNXAUTO", "name": "Nifty Auto", "exchange": "NSE"},
    
    "NIFTYFMCG": {"symbol": "^CNXFMCG", "name": "Nifty FMCG", "exchange": "NSE"},
    "NIFTY_FMCG": {"symbol": "^CNXFMCG", "name": "Nifty FMCG", "exchange": "NSE"},
    "^CNXFMCG": {"symbol": "^CNXFMCG", "name": "Nifty FMCG", "exchange": "NSE"},
    
    "NIFTYMETAL": {"symbol": "^CNXMETAL", "name": "Nifty Metal", "exchange": "NSE"},
    "NIFTY_METAL": {"symbol": "^CNXMETAL", "name": "Nifty Metal", "exchange": "NSE"},
    "^CNXMETAL": {"symbol": "^CNXMETAL", "name": "Nifty Metal", "exchange": "NSE"},
    
    "NIFTYREALTY": {"symbol": "^CNXREALTY", "name": "Nifty Realty", "exchange": "NSE"},
    "NIFTY_REALTY": {"symbol": "^CNXREALTY", "name": "Nifty Realty", "exchange": "NSE"},
    "^CNXREALTY": {"symbol": "^CNXREALTY", "name": "Nifty Realty", "exchange": "NSE"},
    
    "NIFTYENERGY": {"symbol": "^CNXENERGY", "name": "Nifty Energy", "exchange": "NSE"},
    "NIFTY_ENERGY": {"symbol": "^CNXENERGY", "name": "Nifty Energy", "exchange": "NSE"},
    "^CNXENERGY": {"symbol": "^CNXENERGY", "name": "Nifty Energy", "exchange": "NSE"},
    
    "NIFTYINFRA": {"symbol": "^CNXINFRA", "name": "Nifty Infrastructure", "exchange": "NSE"},
    "NIFTY_INFRA": {"symbol": "^CNXINFRA", "name": "Nifty Infrastructure", "exchange": "NSE"},
    "^CNXINFRA": {"symbol": "^CNXINFRA", "name": "Nifty Infrastructure", "exchange": "NSE"},
    
    "NIFTYPSE": {"symbol": "^CNXPSE", "name": "Nifty PSE", "exchange": "NSE"},
    "NIFTY_PSE": {"symbol": "^CNXPSE", "name": "Nifty PSE", "exchange": "NSE"},
    "^CNXPSE": {"symbol": "^CNXPSE", "name": "Nifty PSE", "exchange": "NSE"},
    
    "NIFTYMIDCAP50": {"symbol": "^NSEMDCP50", "name": "Nifty Midcap 50", "exchange": "NSE"},
    "NIFTY_MIDCAP_50": {"symbol": "^NSEMDCP50", "name": "Nifty Midcap 50", "exchange": "NSE"},
    "^NSEMDCP50": {"symbol": "^NSEMDCP50", "name": "Nifty Midcap 50", "exchange": "NSE"},
    
    "NIFTYMIDCAP100": {"symbol": "^NSEMDCP100", "name": "Nifty Midcap 100", "exchange": "NSE"},
    "NIFTY_MIDCAP_100": {"symbol": "^NSEMDCP100", "name": "Nifty Midcap 100", "exchange": "NSE"},
    
    "NIFTYSMALLCAP50": {"symbol": "NIFTY_SMALLCAP_50.NS", "name": "Nifty Smallcap 50", "exchange": "NSE"},
    "NIFTY_SMALLCAP_50": {"symbol": "NIFTY_SMALLCAP_50.NS", "name": "Nifty Smallcap 50", "exchange": "NSE"},
    
    "NIFTYSMALLCAP100": {"symbol": "NIFTY_SMALLCAP_100.NS", "name": "Nifty Smallcap 100", "exchange": "NSE"},
    "NIFTY_SMALLCAP_100": {"symbol": "NIFTY_SMALLCAP_100.NS", "name": "Nifty Smallcap 100", "exchange": "NSE"},
    
    "NIFTYNEXT50": {"symbol": "^NSMIDCP", "name": "Nifty Next 50", "exchange": "NSE"},
    "NIFTY_NEXT_50": {"symbol": "^NSMIDCP", "name": "Nifty Next 50", "exchange": "NSE"},
    "^NSMIDCP": {"symbol": "^NSMIDCP", "name": "Nifty Next 50", "exchange": "NSE"},
    
    "NIFTY100": {"symbol": "^CNX100", "name": "Nifty 100", "exchange": "NSE"},
    "NIFTY_100": {"symbol": "^CNX100", "name": "Nifty 100", "exchange": "NSE"},
    "^CNX100": {"symbol": "^CNX100", "name": "Nifty 100", "exchange": "NSE"},
    
    "NIFTY200": {"symbol": "^CNX200", "name": "Nifty 200", "exchange": "NSE"},
    "NIFTY_200": {"symbol": "^CNX200", "name": "Nifty 200", "exchange": "NSE"},
    "^CNX200": {"symbol": "^CNX200", "name": "Nifty 200", "exchange": "NSE"},
    
    "NIFTY500": {"symbol": "^CNX500", "name": "Nifty 500", "exchange": "NSE"},
    "NIFTY_500": {"symbol": "^CNX500", "name": "Nifty 500", "exchange": "NSE"},
    "^CNX500": {"symbol": "^CNX500", "name": "Nifty 500", "exchange": "NSE"},
    
    # BSE Indices
    "SENSEX": {"symbol": "^BSESN", "name": "S&P BSE Sensex", "exchange": "BSE"},
    "^BSESN": {"symbol": "^BSESN", "name": "S&P BSE Sensex", "exchange": "BSE"},
    
    "BSE100": {"symbol": "^BSE100", "name": "S&P BSE 100", "exchange": "BSE"},
    "BSE_100": {"symbol": "^BSE100", "name": "S&P BSE 100", "exchange": "BSE"},
    "^BSE100": {"symbol": "^BSE100", "name": "S&P BSE 100", "exchange": "BSE"},
    
    "BSE200": {"symbol": "^BSE200", "name": "S&P BSE 200", "exchange": "BSE"},
    "BSE_200": {"symbol": "^BSE200", "name": "S&P BSE 200", "exchange": "BSE"},
    "^BSE200": {"symbol": "^BSE200", "name": "S&P BSE 200", "exchange": "BSE"},
    
    "BSE500": {"symbol": "^BSE500", "name": "S&P BSE 500", "exchange": "BSE"},
    "BSE_500": {"symbol": "^BSE500", "name": "S&P BSE 500", "exchange": "BSE"},
    "^BSE500": {"symbol": "^BSE500", "name": "S&P BSE 500", "exchange": "BSE"},
    
    "BSEMIDCAP": {"symbol": "BSE-MIDCAP.BO", "name": "S&P BSE Midcap", "exchange": "BSE"},
    "BSE_MIDCAP": {"symbol": "BSE-MIDCAP.BO", "name": "S&P BSE Midcap", "exchange": "BSE"},
    
    "BSESMALLCAP": {"symbol": "BSE-SMLCAP.BO", "name": "S&P BSE Smallcap", "exchange": "BSE"},
    "BSE_SMALLCAP": {"symbol": "BSE-SMLCAP.BO", "name": "S&P BSE Smallcap", "exchange": "BSE"},
    
    "BSEBANKEX": {"symbol": "^BSESN", "name": "S&P BSE Bankex", "exchange": "BSE"},
    "BSE_BANKEX": {"symbol": "^BSESN", "name": "S&P BSE Bankex", "exchange": "BSE"},
}


def is_index(symbol: str) -> bool:
    """
    Check if a symbol is an index.
    
    Args:
        symbol: The symbol to check (e.g., 'NIFTY', 'SENSEX', '^NSEI')
    
    Returns:
        True if the symbol is an index, False otherwise
    """
    symbol_upper = symbol.upper().strip()
    return symbol_upper in INDIAN_INDICES


def get_yahoo_symbol(symbol: str) -> str:
    """
    Get the Yahoo Finance symbol for a stock or index.
    
    For indices: Returns the mapped Yahoo Finance symbol (e.g., 'NIFTY' -> '^NSEI')
    For stocks: Returns None (caller should try .NS and .BO suffixes)
    
    Args:
        symbol: The symbol to look up
    
    Returns:
        Yahoo Finance symbol for indices, None for stocks
    """
    symbol_upper = symbol.upper().strip()
    
    if symbol_upper in INDIAN_INDICES:
        return INDIAN_INDICES[symbol_upper]["symbol"]
    
    return None


def get_index_info(symbol: str) -> dict:
    """
    Get information about an index.
    
    Args:
        symbol: The index symbol
    
    Returns:
        Dictionary with 'symbol', 'name', and 'exchange' keys, or None if not found
    """
    symbol_upper = symbol.upper().strip()
    return INDIAN_INDICES.get(symbol_upper)


def get_all_indices() -> list:
    """
    Get a list of all available indices.
    
    Returns:
        List of dictionaries with index information
    """
    # Remove duplicates (same Yahoo symbol, different aliases)
    seen_symbols = set()
    indices = []
    
    for key, info in INDIAN_INDICES.items():
        yahoo_symbol = info["symbol"]
        if yahoo_symbol not in seen_symbols:
            seen_symbols.add(yahoo_symbol)
            indices.append({
                "symbol": key,  # Use a clean symbol name
                "name": info["name"],
                "exchange": info["exchange"],
                "yahoo_symbol": yahoo_symbol
            })
    
    return indices


def normalize_symbol(symbol: str) -> str:
    """
    Normalize a symbol to its canonical form.
    
    For indices: Returns the primary alias (e.g., 'NIFTY_50' -> 'NIFTY50')
    For stocks: Returns the symbol as-is
    
    Args:
        symbol: The symbol to normalize
    
    Returns:
        Normalized symbol
    """
    symbol_upper = symbol.upper().strip()
    
    if symbol_upper in INDIAN_INDICES:
        # Return the Yahoo symbol for indices
        return INDIAN_INDICES[symbol_upper]["symbol"]
    
    return symbol_upper

