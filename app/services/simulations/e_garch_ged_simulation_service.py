import yfinance as yf
import numpy as np
import pandas as pd
from arch import arch_model
from app.utils.vix_cache import get_vix_value
from app.utils.chart_utils import generate_chart_data

def run_e_garch_ged_simulation(symbol: str, num_simulations: int = 10000, num_days: int = 252, include_chart_data: bool = False):
    """
    EGARCH(1,1) with Generalized Error Distribution (GED) simulation.
    Returns: {"mean": X, "min": Y, "max": Z, "P(min)": p1, "P(max)": p2}
    """
    if num_simulations <= 0 or num_days <= 0:
        raise ValueError("Number of simulations and days must be positive integers.")

    # Fetch stock historical data
    suffixes = ['.NS', '.BO']
    hist = None
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

    # Compute log returns
    hist['Log Return'] = np.log(hist['Close'] / hist['Close'].shift(1))
    log_returns = hist['Log Return'].dropna() * 100

    # Fit EGARCH(1,1) with GED distribution
    model = arch_model(log_returns, vol='EGARCH', p=1, q=1, dist='ged')
    fitted_model = model.fit(disp="off")
    
    # Forecast
    forecast = fitted_model.forecast(horizon=num_days, reindex=False, method="simulation")
    mean_forecast = forecast.mean.values[-1] / 100
    vol_forecast = np.sqrt(forecast.variance.values[-1]) / 100

    # Monte Carlo simulation
    dt = 1 / 252
    last_price = hist['Close'].iloc[-1]
    
    shocks = np.random.normal(0, 1, size=(num_days, num_simulations))
    drift = (mean_forecast - 0.5 * vol_forecast**2) * dt
    diffusion = vol_forecast * np.sqrt(dt)
    
    drift = drift[:, np.newaxis]
    diffusion = diffusion[:, np.newaxis]
    
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

