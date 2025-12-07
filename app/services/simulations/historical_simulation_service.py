import yfinance as yf
import numpy as np
import pandas as pd
from app.utils.vix_cache import get_vix_value
from app.utils.chart_utils import generate_chart_data
from app.utils.index_utils import is_index, get_yahoo_symbol

def run_historical_simulation(symbol: str, num_simulations: int = 10000, num_days: int = 252, include_chart_data: bool = False):
    """
    Historical Simulation using bootstrap method.
    Returns: {"mean": X, "min": Y, "max": Z, "P(min)": p1, "P(max)": p2}
    """
    if num_simulations <= 0 or num_days <= 0:
        raise ValueError("Number of simulations and days must be positive integers.")

    # Fetch historical data (stock or index)
    hist = None
    
    # Check if it's an index
    if is_index(symbol):
        yahoo_symbol = get_yahoo_symbol(symbol)
        stock = yf.Ticker(yahoo_symbol)
        hist = stock.history(period="5y")
    else:
        # For stocks, try NSE/BSE
        suffixes = ['.NS', '.BO']
        for suffix in suffixes:
            yf_symbol = symbol + suffix
            stock = yf.Ticker(yf_symbol)
            hist = stock.history(period="5y")
            if not hist.empty:
                break

    if hist is None or hist.empty:
        raise ValueError(f"No historical data found for symbol '{symbol}'.")

    # Fetch India VIX
    vix_value = get_vix_value()

    # Compute returns
    hist['Return'] = hist['Close'].pct_change()
    historical_returns = hist['Return'].dropna().values

    # Bootstrap simulation
    last_price = hist['Close'].iloc[-1]
    
    if include_chart_data:
        # Store full price paths when chart data is needed
        price_paths = np.zeros((num_days, num_simulations))
        for sim in range(num_simulations):
            sampled_returns = np.random.choice(historical_returns, size=num_days, replace=True)
            price_paths[:, sim] = last_price * np.cumprod(1 + sampled_returns)
        final_prices = price_paths[-1, :]
    else:
        # Only store final prices when chart data is not needed
        final_prices = []
        for _ in range(num_simulations):
            sampled_returns = np.random.choice(historical_returns, size=num_days, replace=True)
            price_path = last_price * np.cumprod(1 + sampled_returns)
            final_prices.append(price_path[-1])
        final_prices = np.array(final_prices)
    
    # Calculate statistics
    mean_price = float(np.mean(final_prices))
    min_price = float(np.min(final_prices))
    max_price = float(np.max(final_prices))
    
    p_min = float(np.sum(final_prices <= min_price * 1.05) / num_simulations)
    p_max = float(np.sum(final_prices >= max_price * 0.95) / num_simulations)
    
    result = {
        "mean": round(mean_price, 2),
        "min": round(min_price, 2),
        "max": round(max_price, 2),
        "P(min)": round(p_min, 4),
        "P(max)": round(p_max, 4)
    }
    
    # Add chart data if requested
    if include_chart_data:
        simulation_df = pd.DataFrame(price_paths)  # Shape is already (num_days, num_simulations)
        result["chart_data"] = generate_chart_data(simulation_df)
    
    return result

