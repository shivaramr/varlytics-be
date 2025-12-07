"""
Simulation services for stock analysis.
Contains 22 different simulation models including GARCH, EGARCH, GJR-GARCH variants,
and classical methods like Monte Carlo, Historical Simulation, etc.

Performance:
- run_all_simulations: Parallel execution (~8 seconds)
- run_all_simulations_ultra_optimized: Shared data + parallel (~3-5 seconds)
"""

from app.services.simulations_service import (
    run_all_simulations,
    run_all_simulations_sequential
)
from app.services.simulations.optimized_batch_service import run_all_simulations_ultra_optimized

__all__ = [
    'run_all_simulations',
    'run_all_simulations_ultra_optimized',
    'run_all_simulations_sequential'
]

