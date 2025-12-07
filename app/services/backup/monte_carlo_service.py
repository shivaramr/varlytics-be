import yfinance as yf
import numpy as np
import pandas as pd

def get_monte_carlo_simulation(symbol: str, num_simulations: int = 10000, num_days: int = 252):
    # Validate inputs
    if num_simulations <= 0 or num_days <= 0:
        raise ValueError("Number of simulations and days must be positive integers.")

    # Attempt to fetch data with .NS suffix first, then .BO if no data
    suffixes = ['.NS', '.BO']
    hist = None

    for suffix in suffixes:
        yf_symbol = symbol + suffix
        stock = yf.Ticker(yf_symbol)
        hist = stock.history(period="1y")
        if not hist.empty:
            break  # Exit the loop if data found

    if hist.empty:
        raise ValueError(f"No historical data found for symbol '{symbol}'.")

    # Calculate daily returns
    hist['Daily Return'] = hist['Close'].pct_change()
    daily_returns = hist['Daily Return'].dropna()

    # Calculate mean and standard deviation
    mu = daily_returns.mean()
    sigma = daily_returns.std()

    # Monte Carlo simulation using Geometric Brownian Motion
    dt = 1 / 252
    simulations = np.zeros((num_days, num_simulations))
    last_price = hist['Close'].iloc[-1]

    for i in range(num_simulations):
        price_path = [last_price]
        for _ in range(num_days):
            shock = np.random.normal(0, 1)
            price = price_path[-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * shock * np.sqrt(dt))
            price_path.append(price)
        simulations[:, i] = price_path[1:]

    simulation_df = pd.DataFrame(simulations)

    final_prices = simulation_df.iloc[-1].values

    summary = {
        "mean": float(np.mean(final_prices)),
        "min": float(np.min(final_prices)),
        "max": float(np.max(final_prices)),
        "percentile_5": float(np.percentile(final_prices, 5)),
        "percentile_95": float(np.percentile(final_prices, 95)),
        "simulations_run": num_simulations,
        "days_simulated": num_days,
    }

    # First-hit target levels (±2%, ±5%, ±10%) from last known price
    price_targets = []
    for pct in [-10, -5, -2, 2, 5, 10]:
        level = last_price * (1 + pct / 100)
        price_targets.append(round(level, 2))

    # Convert simulation DataFrame to NumPy for faster ops
    simulation_array = simulation_df.values

    # Compute probabilities for touching each target
    final_inference = []
    for target in price_targets:
        # For each simulation, check if any price in the path touches the target
        touched = np.any(simulation_array <= target, axis=0) if target < last_price else np.any(simulation_array >= target, axis=0)
        probability = np.mean(touched) * 100  # as percentage
        
        # Build human-readable label
        description = (
            f"~{probability:.1f}% chance of touching {target} during the simulation period."
        )
        
        final_inference.append({
            "target_price": target,
            "direction": "downside" if target < last_price else "upside",
            "probability_percent": round(probability, 2),
            "description": description
        })

        summary["final_inference"] = final_inference

    return summary
    # Return JSON-serializable format
    # return simulation_df.to_dict(orient="records")