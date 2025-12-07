"""
Utility functions for generating chart data from simulation results.
"""
import numpy as np
import pandas as pd
import gzip
import base64
import json


def generate_chart_data(simulation_df: pd.DataFrame, num_bins: int = 30, sample_size: int = 50):
    """
    Generate chart data for visualization from simulation results.

    Args:
        simulation_df: DataFrame with shape (num_days, num_simulations) containing price paths
        num_bins: Number of bins for histogram
        sample_size: Number of sample paths to include in line chart

    Returns:
        Dictionary containing:
            - line_chart_data: List of dictionaries with x and y values for sample paths with 756 points
            - histogram_data: List of dictionaries with bin centers and counts for terminal prices with 30 bins
    """
    num_days, num_simulations = simulation_df.shape
    sample_size = min(sample_size, num_simulations)

    # Line chart (first N paths)
    sample_paths = simulation_df.iloc[:, :sample_size].copy()
    sample_paths.insert(0, "x", np.arange(1, num_days + 1))
    line_chart_data = sample_paths.rename(columns={i: f"y{i}" for i in range(sample_size)}).to_dict(orient="records")

    # Histogram (terminal prices)
    final_prices = simulation_df.iloc[-1].values
    counts, bin_edges = np.histogram(final_prices, bins=num_bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    histogram_data = pd.DataFrame({
        "bin": np.round(bin_centers, 2),
        "count": counts.astype(int)
    }).to_dict(orient="records")

    # This graph can be decompressed and decrypted on the frontend using the decodeCompressedChartData function
    return {
        "line_chart_data": line_chart_data,
        "histogram_data": histogram_data
    }


def compress_chart_data(chart_data: dict) -> str:
    json_bytes = json.dumps(chart_data).encode('utf-8')
    compressed = gzip.compress(json_bytes)
    encoded = base64.b64encode(compressed).decode('utf-8')
    return encoded
 