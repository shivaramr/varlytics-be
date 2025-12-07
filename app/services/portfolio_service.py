"""
Portfolio Analysis Service

Analyzes portfolio risk using multiple risk models:
- Variance-Covariance VaR
- Historical Simulation VaR
- Monte Carlo Simulation VaR
- GARCH/EGARCH models
- Expected Shortfall (CVaR)
"""

import yfinance as yf
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from scipy import stats
from arch import arch_model
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.utils.index_utils import is_index, get_yahoo_symbol


def fetch_stock_data(symbol: str, period: str = "2y") -> tuple:
    """
    Fetch stock/index data with NSE/BSE fallback.
    Returns: (symbol, current_price, historical_data)
    """
    # Check if it's an index first
    if is_index(symbol):
        yahoo_symbol = get_yahoo_symbol(symbol)
        try:
            stock = yf.Ticker(yahoo_symbol)
            hist = stock.history(period=period)
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                return symbol, float(current_price), hist
        except Exception:
            pass
        raise ValueError(f"No data found for index '{symbol}'")
    
    # For stocks, try NSE/BSE
    suffixes = ['.NS', '.BO']
    for suffix in suffixes:
        yf_symbol = symbol + suffix
        try:
            stock = yf.Ticker(yf_symbol)
            hist = stock.history(period=period)
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                return symbol, float(current_price), hist
        except Exception:
            continue
    
    raise ValueError(f"No data found for symbol '{symbol}'")


def calculate_portfolio_metrics(
    holdings: List[Dict[str, Any]],
    num_simulations: int = 10000,
    num_days: int = 252,
    confidence_level: float = 0.995,
    include_garch: bool = False
) -> Dict[str, Any]:
    """
    Calculate comprehensive portfolio risk metrics.
    
    Args:
        holdings: List of {"symbol": str, "quantity": int/float}
        num_simulations: Number of Monte Carlo simulations (default 10000)
        num_days: Forecast horizon (default 252 = 1 year)
        confidence_level: VaR confidence level (default 99.5%)
        include_garch: Whether to include GARCH models (can be slow)
    
    Returns:
        Dictionary with portfolio metrics and VaR estimates
    """
    if not holdings or len(holdings) == 0:
        raise ValueError("Holdings list cannot be empty")
    
    # Step 1: Fetch data for all stocks in parallel
    stock_data = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(fetch_stock_data, holding["symbol"]): holding 
            for holding in holdings
        }
        
        for future in as_completed(futures):
            holding = futures[future]
            try:
                symbol, current_price, hist_data = future.result()
                stock_data[symbol] = {
                    "quantity": holding["quantity"],
                    "current_price": current_price,
                    "historical_data": hist_data
                }
            except Exception as e:
                raise ValueError(f"Error fetching data for {holding['symbol']}: {str(e)}")
    
    # Step 2: Calculate portfolio value and weights
    total_value = sum(
        data["quantity"] * data["current_price"] 
        for data in stock_data.values()
    )
    
    weights = {
        symbol: (data["quantity"] * data["current_price"]) / total_value
        for symbol, data in stock_data.items()
    }
    
    # Step 3: Calculate returns for all stocks
    returns_data = {}
    for symbol, data in stock_data.items():
        hist = data["historical_data"]
        returns = hist['Close'].pct_change().dropna()
        returns_data[symbol] = returns
    
    # Create returns DataFrame
    returns_df = pd.DataFrame(returns_data)
    returns_df = returns_df.dropna()
    
    if len(returns_df) < 100:
        raise ValueError("Insufficient historical data for analysis (minimum 100 days required)")
    
    # Step 4: Calculate portfolio-level metrics
    portfolio_returns = sum(
        returns_df[symbol] * weights[symbol] 
        for symbol in returns_df.columns
    )
    
    expected_return = float(portfolio_returns.mean()) * 252  # Annualized
    portfolio_volatility = float(portfolio_returns.std()) * np.sqrt(252)  # Annualized
    
    # Step 5: Calculate VaR using multiple methods
    var_results = {}
    
    # 5.1 Variance-Covariance VaR (Parametric)
    mean_return = portfolio_returns.mean()
    std_return = portfolio_returns.std()
    z_score = stats.norm.ppf(1 - confidence_level)
    var_parametric = total_value * (mean_return + z_score * std_return) * np.sqrt(num_days)
    var_results["variance_covariance"] = round(float(var_parametric), 2)
    
    # 5.2 Historical Simulation VaR
    sorted_returns = np.sort(portfolio_returns.values)
    var_index = int((1 - confidence_level) * len(sorted_returns))
    var_historical = total_value * sorted_returns[var_index] * np.sqrt(num_days)
    var_results["historical"] = round(float(var_historical), 2)
    
    # 5.3 Monte Carlo VaR
    mc_simulations = np.random.normal(
        mean_return, 
        std_return, 
        num_simulations
    ) * np.sqrt(num_days)
    mc_var = np.percentile(mc_simulations, (1 - confidence_level) * 100)
    var_results["monte_carlo"] = round(float(total_value * mc_var), 2)
    
    # 5.4 Expected Shortfall (CVaR) - average loss beyond VaR
    cvar_threshold = sorted_returns[var_index]
    cvar = portfolio_returns[portfolio_returns <= cvar_threshold].mean()
    expected_shortfall = total_value * cvar * np.sqrt(num_days)
    var_results["expected_shortfall"] = round(float(expected_shortfall), 2)
    
    # 5.5 GARCH VaR (optional, can be slow)
    if include_garch:
        try:
            # Fit GARCH(1,1) model to portfolio returns
            scaled_returns = portfolio_returns * 100  # Scale for numerical stability
            model = arch_model(
                scaled_returns, 
                vol='Garch', 
                p=1, 
                q=1,
                dist='normal'
            )
            model_fit = model.fit(disp='off', show_warning=False)
            
            # Forecast volatility
            forecast = model_fit.forecast(horizon=num_days)
            forecasted_variance = forecast.variance.values[-1, :].sum()
            forecasted_volatility = np.sqrt(forecasted_variance) / 100
            
            # Calculate GARCH VaR
            garch_var = total_value * (mean_return * num_days + z_score * forecasted_volatility)
            var_results["garch"] = round(float(garch_var), 2)
        except Exception as e:
            var_results["garch"] = f"Error: {str(e)}"
    
    # Step 6: Calculate upside/downside probabilities
    positive_returns = portfolio_returns[portfolio_returns > 0]
    negative_returns = portfolio_returns[portfolio_returns < 0]
    
    probability_up = float(len(positive_returns) / len(portfolio_returns))
    probability_down = float(len(negative_returns) / len(portfolio_returns))
    
    # Expected gains and losses
    expected_upside = total_value * positive_returns.mean() * np.sqrt(num_days) if len(positive_returns) > 0 else 0
    expected_downside = total_value * negative_returns.mean() * np.sqrt(num_days) if len(negative_returns) > 0 else 0
    
    # Step 7: Calculate portfolio Beta (relative to market if possible)
    try:
        # Use NIFTY50 as market proxy
        nifty = yf.Ticker("^NSEI")
        nifty_hist = nifty.history(period="2y")
        if not nifty_hist.empty:
            nifty_returns = nifty_hist['Close'].pct_change().dropna()
            
            # Align dates
            common_dates = portfolio_returns.index.intersection(nifty_returns.index)
            if len(common_dates) > 100:
                aligned_portfolio = portfolio_returns.loc[common_dates]
                aligned_market = nifty_returns.loc[common_dates]
                
                covariance = np.cov(aligned_portfolio, aligned_market)[0, 1]
                market_variance = np.var(aligned_market)
                portfolio_beta = float(covariance / market_variance)
            else:
                portfolio_beta = None
        else:
            portfolio_beta = None
    except Exception:
        portfolio_beta = None
    
    # Step 8: Stress testing scenarios
    stress_scenarios = {
        "market_crash_20": total_value * (1 - 0.20),  # -20% scenario
        "market_crash_30": total_value * (1 - 0.30),  # -30% scenario
        "market_boom_20": total_value * (1 + 0.20),   # +20% scenario
        "market_boom_30": total_value * (1 + 0.30),   # +30% scenario
    }
    
    # Step 9: Compile results
    result = {
        "total_value": round(float(total_value), 2),
        "expected_return": round(expected_return, 4),
        "portfolio_volatility": round(portfolio_volatility, 4),
        "sharpe_ratio": round(expected_return / portfolio_volatility, 4) if portfolio_volatility > 0 else 0,
        "VaR": var_results,
        "confidence_level": confidence_level,
        "forecast_horizon_days": num_days,
        "probability_up": round(probability_up, 4),
        "probability_down": round(probability_down, 4),
        "expected_upside": round(float(expected_upside), 2),
        "expected_downside": round(float(expected_downside), 2),
        "portfolio_composition": {
            symbol: {
                "quantity": data["quantity"],
                "current_price": round(data["current_price"], 2),
                "value": round(data["quantity"] * data["current_price"], 2),
                "weight": round(weights[symbol], 4)
            }
            for symbol, data in stock_data.items()
        },
        "stress_test": {
            k: round(v, 2) for k, v in stress_scenarios.items()
        }
    }
    
    if portfolio_beta is not None:
        result["portfolio_beta"] = round(portfolio_beta, 4)
    
    return result


def calculate_portfolio_var_detailed(
    holdings: List[Dict[str, Any]],
    num_simulations: int = 10000,
    num_days: int = 252,
    confidence_level: float = 0.995
) -> Dict[str, Any]:
    """
    Simplified version focusing on VaR calculations only.
    Faster than full portfolio analysis.
    
    Args:
        holdings: List of {"symbol": str, "quantity": int/float}
        num_simulations: Number of Monte Carlo simulations (default 10000)
        num_days: Forecast horizon (default 252 = 1 year)
        confidence_level: VaR confidence level (default 99.5%)
    """
    result = calculate_portfolio_metrics(
        holdings=holdings,
        num_simulations=num_simulations,
        num_days=num_days,
        confidence_level=confidence_level,
        include_garch=False
    )
    
    # Return simplified result
    return {
        "total_value": result["total_value"],
        "expected_return": result["expected_return"],
        "portfolio_volatility": result["portfolio_volatility"],
        "VaR": result["VaR"],
        "probability_up": result["probability_up"],
        "probability_down": result["probability_down"],
        "expected_upside": result["expected_upside"],
        "expected_downside": result["expected_downside"]
    }

