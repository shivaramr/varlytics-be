import yfinance as yf
import numpy as np
import pandas as pd
from app.utils.vix_cache import get_vix_value
from app.utils.chart_utils import generate_chart_data
from app.utils.index_utils import is_index, get_yahoo_symbol

def run_risk_metrics_simulation(symbol: str, num_simulations: int = 10000, num_days: int = 252, lambda_decay: float = 0.94, include_chart_data: bool = False):
    """
    RiskMetrics EWMA (Exponentially Weighted Moving Average) simulation.
    Returns: {"mean": X, "min": Y, "max": Z, "P(min)": p1, "P(max)": p2}
    """
    if num_simulations <= 0 or num_days <= 0:
        raise ValueError("Number of simulations and days must be positive integers.")

    # Fetch historical data (stock or index)
    hist = None
    
    if is_index(symbol):
        yahoo_symbol = get_yahoo_symbol(symbol)
        stock = yf.Ticker(yahoo_symbol)
        hist = stock.history(period="5y")
    else:
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

    # Calculate returns
    hist['Log Return'] = np.log(hist['Close'] / hist['Close'].shift(1))
    log_returns = hist['Log Return'].dropna()
    
    # Calculate EWMA volatility
    squared_returns = log_returns ** 2
    ewma_variance = squared_returns.ewm(alpha=1-lambda_decay, adjust=False).mean()
    current_volatility = np.sqrt(ewma_variance.iloc[-1])
    
    mu = log_returns.mean()

    # Monte Carlo simulation
    dt = 1 / 252
    last_price = hist['Close'].iloc[-1]
    
    shocks = np.random.normal(0, 1, size=(num_days, num_simulations))
    drift = (mu - 0.5 * current_volatility**2) * dt
    diffusion = current_volatility * np.sqrt(dt)
    
    returns = np.exp(drift + diffusion * shocks)
    price_paths = last_price * np.cumprod(returns, axis=0)
    
    final_prices = price_paths[-1, :]
    
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

