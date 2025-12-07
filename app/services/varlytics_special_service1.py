import numpy as np
import pandas as pd
import yfinance as yf
from arch import arch_model
from scipy.stats import t
from app.utils.vix_cache import get_vix_value
from app.utils.chart_utils import generate_chart_data, compress_chart_data
from app.utils.index_utils import is_index, get_yahoo_symbol

def simulate_skewt(df, skew, size):
    """
    Simulate random numbers from a skewed t-distribution.
    Uses the Azzalini method for skewed distributions.
    """
    u = np.random.standard_t(df, size=size)
    v = np.random.standard_normal(size=size)
    delta = skew / np.sqrt(1 + skew**2)
    return delta * np.abs(u) + np.sqrt(1 - delta**2) * v

def simulate_stock_egarch(symbol: str, num_simulations: int = 10000, num_days: int = 252):
    if num_simulations <= 0 or num_days <= 0:
        raise ValueError("Number of simulations and days must be positive integers.")

    # --- 1. Fetch historical data (stock or index) ---
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

    # --- 2. Fetch India VIX ---
    vix_value = get_vix_value()

    # --- 3. Compute log returns for EGARCH ---
    hist['Log Return'] = np.log(hist['Close'] / hist['Close'].shift(1))
    log_returns = hist['Log Return'].dropna() * 100  # arch expects percentage returns

    # 🔄 UPDATED: Use skewed-t distribution
    model = arch_model(log_returns, vol='EGARCH', p=1, q=1, dist='skewt')
    fitted_model = model.fit(disp="off")
    forecast = fitted_model.forecast(horizon=num_days, reindex=False, method="simulation")

    mean_forecast = forecast.mean.values[-1] / 100  # Convert from % to decimal
    vol_forecast = np.sqrt(forecast.variance.values[-1]) / 100

    # 🔄 Extract skewness and degrees of freedom from the fitted model
    params = fitted_model.params
    skew = params.get('skew', 0)
    df = params.get('nu', 10)  # Default to 10 if not found

    # --- 4. Vectorized Monte Carlo simulation ---
    dt = 1 / 252
    last_price = hist['Close'].iloc[-1]

    # 🔄 Simulate skewed-t random shocks
    shocks = simulate_skewt(df, skew, size=(num_days, num_simulations))

    drift = (mean_forecast - 0.5 * vol_forecast**2) * dt
    diffusion = vol_forecast * np.sqrt(dt)

    drift = drift[:, np.newaxis]
    diffusion = diffusion[:, np.newaxis]

    returns = np.exp(drift + diffusion * shocks)
    price_paths = np.vstack([
        np.full((1, num_simulations), last_price),
        last_price * np.cumprod(returns, axis=0)
    ])
    simulation_df = pd.DataFrame(price_paths[1:])
    final_prices = simulation_df.iloc[-1].values

    # --- 5. Build Summary ---
    summary = {
        "model": "EGARCH(1,1) with Skewed-t",
        "current_price": round(last_price, 2),
        "mean": round(float(np.mean(final_prices)), 2),
        "min": round(float(np.min(final_prices)), 2),
        "max": round(float(np.max(final_prices)), 2),
        "percentile_5": round(float(np.percentile(final_prices, 5)), 2),
        "percentile_95": round(float(np.percentile(final_prices, 95)), 2),
        "simulations_run": num_simulations,
        "days_simulated": num_days,
        "vix_index_used": "^INDIAVIX",
        "vix_value": round(vix_value, 2) if vix_value else "Unavailable"
    }

    # --- 6. First-hit probabilities (vectorized) ---
    price_targets = [round(last_price * (1 + pct / 100), 2) for pct in [-10, -5, -2, 2, 5, 10]]
    simulation_array = simulation_df.values
    final_inference = []

    for target in price_targets:
        if target < last_price:
            hit_matrix = simulation_array <= target
        else:
            hit_matrix = simulation_array >= target

        hit_indices = np.argmax(hit_matrix, axis=0)
        was_hit = hit_matrix.any(axis=0)
        valid_hit_days = hit_indices[was_hit]

        probability = (np.sum(was_hit) / num_simulations) * 100
        avg_day_to_hit = None
        description = f"~{probability:.1f}% chance of touching {target} during the simulation period."

        if valid_hit_days.size > 0:
            avg_day = np.mean(valid_hit_days)
            if probability >= 20 and avg_day <= num_days * 0.7:
                avg_day_to_hit = round(avg_day)
                description += f" On average, this happens around day {avg_day_to_hit}."
            elif probability < 20:
                description += " But it rarely occurs in most simulations."
            else:
                description += " When it happens, it usually occurs late in the simulation period."

        final_inference.append({
            "target_price": target,
            "change_percent": round((target - last_price) / last_price * 100, 2),
            "direction": "downside" if target < last_price else "upside",
            "probability_percent": round(probability, 2),
            "average_day_to_hit": avg_day_to_hit,
            "description": description
        })

    summary["final_inference"] = final_inference

    # --- 7. Prepare Chart Data for MUI X Charts (Vectorized) ---
    chart_data = generate_chart_data(simulation_df)
    # This graph can be decompressed and decrypted on the frontend using the decodeCompressedChartData function from chart_utils.py
    summary["compressed_chart_data"] = compress_chart_data(chart_data)
    # summary["chart_data"] = generate_chart_data(simulation_df)

    # The above data, we need to try streamlining it to reduce payload size
    return summary
 