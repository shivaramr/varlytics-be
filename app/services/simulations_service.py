"""
Optimized aggregator service to run all 22 simulations in parallel.
Uses ThreadPoolExecutor for concurrent execution.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any

from app.services.simulations.garch_n_simulation_service import run_garch_n_simulation
from app.services.simulations.garch_t_simulation_service import run_garch_t_simulation
from app.services.simulations.garch_ged_simulation_service import run_garch_ged_simulation
from app.services.simulations.garch_skewed_n_simulation_service import run_garch_skewed_n_simulation
from app.services.simulations.garch_skewed_t_simulation_service import run_garch_skewed_t_simulation
from app.services.simulations.garch_skewed_ged_simulation_service import run_garch_skewed_ged_simulation

from app.services.simulations.e_garch_n_simulation_service import run_e_garch_n_simulation
from app.services.simulations.e_garch_t_simulation_service import run_e_garch_t_simulation
from app.services.simulations.e_garch_ged_simulation_service import run_e_garch_ged_simulation
from app.services.simulations.e_garch_skewed_n_simulation_service import run_e_garch_skewed_n_simulation
from app.services.simulations.e_garch_skewed_t_simulation_service import run_e_garch_skewed_t_simulation
from app.services.simulations.e_garch_skewed_ged_simulation_service import run_e_garch_skewed_ged_simulation

from app.services.simulations.gjr_garch_n_simulation_service import run_gjr_garch_n_simulation
from app.services.simulations.gjr_garch_t_simulation_service import run_gjr_garch_t_simulation
from app.services.simulations.gjr_garch_ged_simulation_service import run_gjr_garch_ged_simulation
from app.services.simulations.gjr_garch_skewed_n_simulation_service import run_gjr_garch_skewed_n_simulation
from app.services.simulations.gjr_garch_skewed_t_simulation_service import run_gjr_garch_skewed_t_simulation
from app.services.simulations.gjr_garch_skewed_ged_simulation_service import run_gjr_garch_skewed_ged_simulation

from app.services.simulations.historical_simulation_service import run_historical_simulation
from app.services.simulations.monte_carlo_simulation_service import run_monte_carlo_simulation
from app.services.simulations.risk_metrics_simulation_service import run_risk_metrics_simulation
from app.services.simulations.simple_variance_simulation_service import run_simple_variance_simulation


# Map of simulation names to functions
SIMULATION_REGISTRY = {
    "GARCH-N": run_garch_n_simulation,
    "GARCH-T": run_garch_t_simulation,
    "GARCH-GED": run_garch_ged_simulation,
    "GARCH-SKEWED-N": run_garch_skewed_n_simulation,
    "GARCH-SKEWED-T": run_garch_skewed_t_simulation,
    "GARCH-SKEWED-GED": run_garch_skewed_ged_simulation,
    "EGARCH-N": run_e_garch_n_simulation,
    "EGARCH-T": run_e_garch_t_simulation,
    "EGARCH-GED": run_e_garch_ged_simulation,
    "EGARCH-SKEWED-N": run_e_garch_skewed_n_simulation,
    "EGARCH-SKEWED-T": run_e_garch_skewed_t_simulation,
    "EGARCH-SKEWED-GED": run_e_garch_skewed_ged_simulation,
    "GJR-GARCH-N": run_gjr_garch_n_simulation,
    "GJR-GARCH-T": run_gjr_garch_t_simulation,
    "GJR-GARCH-GED": run_gjr_garch_ged_simulation,
    "GJR-GARCH-SKEWED-N": run_gjr_garch_skewed_n_simulation,
    "GJR-GARCH-SKEWED-T": run_gjr_garch_skewed_t_simulation,
    "GJR-GARCH-SKEWED-GED": run_gjr_garch_skewed_ged_simulation,
    "HISTORICAL": run_historical_simulation,
    "MONTE-CARLO": run_monte_carlo_simulation,
    "RISK-METRICS": run_risk_metrics_simulation,
    "SIMPLE-VARIANCE": run_simple_variance_simulation,
}


def _run_single_simulation(name: str, func, symbol: str, num_simulations: int, num_days: int) -> tuple:
    """Helper function to run a single simulation with error handling."""
    try:
        result = func(symbol, num_simulations, num_days)
        return name, result
    except Exception as e:
        return name, {"error": str(e)}


def run_all_simulations(
    symbol: str, 
    num_simulations: int = 10000, 
    num_days: int = 252, 
    max_workers: int = 8
) -> Dict[str, Any]:
    """
    Run all 22 simulations in parallel and return combined results.
    
    Args:
        symbol: Stock symbol (e.g., "RELIANCE")
        num_simulations: Number of Monte Carlo paths
        num_days: Days to simulate
        max_workers: Maximum number of parallel workers (default: 8)
    
    Returns:
        {
          "GARCH-N": {"mean": X, "min": Y, "max": Z, "P(min)": p1, "P(max)": p2},
          "GARCH-T": {"mean": X, "min": Y, "max": Z, "P(min)": p1, "P(max)": p2},
          ...
        }
    
    Performance:
        - Sequential execution: ~35 seconds
        - Parallel execution (8 workers): ~5-8 seconds
    """
    results = {}
    
    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all simulation tasks
        futures = {
            executor.submit(
                _run_single_simulation, 
                name, 
                func, 
                symbol, 
                num_simulations, 
                num_days
            ): name 
            for name, func in SIMULATION_REGISTRY.items()
        }
        
        # Collect results as they complete
        for future in as_completed(futures):
            name, result = future.result()
            results[name] = result
    
    return results


def run_all_simulations_sequential(
    symbol: str, 
    num_simulations: int = 10000, 
    num_days: int = 252
) -> Dict[str, Any]:
    """
    Sequential version - kept for comparison/debugging.
    Use run_all_simulations() for better performance.
    """
    results = {}
    
    for name, func in SIMULATION_REGISTRY.items():
        try:
            results[name] = func(symbol, num_simulations, num_days)
        except Exception as e:
            results[name] = {"error": str(e)}
    
    return results

