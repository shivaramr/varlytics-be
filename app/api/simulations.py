"""
API endpoints for running stock simulations.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.simulations import run_all_simulations, run_all_simulations_ultra_optimized

# Individual simulation imports
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

router = APIRouter(
    tags=["Simulations"]
)

# Mapping of simulation names to functions
SIMULATION_MAP = {
    "garch-n": run_garch_n_simulation,
    "garch-t": run_garch_t_simulation,
    "garch-ged": run_garch_ged_simulation,
    "garch-skewed-n": run_garch_skewed_n_simulation,
    "garch-skewed-t": run_garch_skewed_t_simulation,
    "garch-skewed-ged": run_garch_skewed_ged_simulation,
    "egarch-n": run_e_garch_n_simulation,
    "egarch-t": run_e_garch_t_simulation,
    "egarch-ged": run_e_garch_ged_simulation,
    "egarch-skewed-n": run_e_garch_skewed_n_simulation,
    "egarch-skewed-t": run_e_garch_skewed_t_simulation,
    "egarch-skewed-ged": run_e_garch_skewed_ged_simulation,
    "gjr-garch-n": run_gjr_garch_n_simulation,
    "gjr-garch-t": run_gjr_garch_t_simulation,
    "gjr-garch-ged": run_gjr_garch_ged_simulation,
    "gjr-garch-skewed-n": run_gjr_garch_skewed_n_simulation,
    "gjr-garch-skewed-t": run_gjr_garch_skewed_t_simulation,
    "gjr-garch-skewed-ged": run_gjr_garch_skewed_ged_simulation,
    "historical": run_historical_simulation,
    "monte-carlo": run_monte_carlo_simulation,
    "risk-metrics": run_risk_metrics_simulation,
    "simple-variance": run_simple_variance_simulation,
}


@router.get("/simulations/{symbol}/all")
async def get_all_simulations(
    symbol: str,
    num_simulations: int = Query(10000, description="Number of Monte Carlo simulations", ge=100, le=10000),
    num_days: int = Query(252, description="Number of days to simulate", ge=1, le=1000),
    optimized: bool = Query(True, description="Use ultra-optimized version (3-5s vs 8s)")
):
    """
    Run all 22 simulations for a given stock symbol.
    
    Performance:
    - optimized=true: Ultra-optimized with shared data fetching (3-5 seconds)
    - optimized=false: Standard parallel execution (8 seconds)
    
    Returns a dictionary with results from all simulation models:
    {
      "GARCH-N": {"mean": X, "min": Y, "max": Z, "P(min)": p1, "P(max)": p2},
      "GARCH-T": {"mean": X, "min": Y, "max": Z, "P(min)": p1, "P(max)": p2},
      ...
    }
    """
    try:
        if optimized:
            results = run_all_simulations_ultra_optimized(symbol, num_simulations, num_days)
        else:
            results = run_all_simulations(symbol, num_simulations, num_days)
        
        return {
            "symbol": symbol,
            "num_simulations": num_simulations,
            "num_days": num_days,
            "optimized": optimized,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running simulations: {str(e)}")


@router.get("/simulations/{symbol}/{simulation_type}")
async def get_specific_simulation(
    symbol: str,
    simulation_type: str,
    num_simulations: int = Query(10000, description="Number of Monte Carlo simulations", ge=100, le=10000),
    num_days: int = Query(252, description="Number of days to simulate", ge=1, le=1000),
    include_chart_data: bool = Query(True, description="Include chart data for visualization (line chart and histogram)")
):
    """
    Run a specific simulation model for a given stock symbol.
    
    Available simulation types:
    - garch-n, garch-t, garch-ged, garch-skewed-n, garch-skewed-t, garch-skewed-ged
    - egarch-n, egarch-t, egarch-ged, egarch-skewed-n, egarch-skewed-t, egarch-skewed-ged
    - gjr-garch-n, gjr-garch-t, gjr-garch-ged, gjr-garch-skewed-n, gjr-garch-skewed-t, gjr-garch-skewed-ged
    - historical, monte-carlo, risk-metrics, simple-variance
    
    Returns:
    {
        "mean": X, "min": Y, "max": Z, "P(min)": p1, "P(max)": p2,
        "chart_data": {  // Only if include_chart_data=true
            "line_chart_data": [...],  // Sample price paths
            "histogram_data": [...]    // Terminal price distribution
        }
    }
    """
    simulation_type_lower = simulation_type.lower()
    
    if simulation_type_lower not in SIMULATION_MAP:
        raise HTTPException(
            status_code=404,
            detail=f"Simulation type '{simulation_type}' not found. Available types: {', '.join(SIMULATION_MAP.keys())}"
        )
    
    try:
        simulation_func = SIMULATION_MAP[simulation_type_lower]
        result = simulation_func(symbol, num_simulations, num_days, include_chart_data=include_chart_data)
        return {
            "symbol": symbol,
            "simulation_type": simulation_type_lower,
            "num_simulations": num_simulations,
            "num_days": num_days,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running simulation: {str(e)}")


@router.get("/simulations/available")
async def get_available_simulations():
    """
    Get a list of all available simulation types.
    """
    return {
        "total_simulations": len(SIMULATION_MAP),
        "simulation_types": list(SIMULATION_MAP.keys()),
        "categories": {
            "GARCH": [k for k in SIMULATION_MAP.keys() if k.startswith("garch-")],
            "EGARCH": [k for k in SIMULATION_MAP.keys() if k.startswith("egarch-")],
            "GJR-GARCH": [k for k in SIMULATION_MAP.keys() if k.startswith("gjr-garch-")],
            "Classical": [k for k in SIMULATION_MAP.keys() if k in ["historical", "monte-carlo", "risk-metrics", "simple-variance"]]
        }
    }

