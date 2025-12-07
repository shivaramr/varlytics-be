"""
Performance test script for simulation optimizations.
Run this to compare sequential vs parallel vs ultra-optimized performance.
"""

import time
from app.services.simulations_service import (
    run_all_simulations,
    run_all_simulations_sequential
)
from app.services.simulations.optimized_batch_service import run_all_simulations_ultra_optimized


def benchmark_simulations(symbol: str = "RELIANCE", num_simulations: int = 10000, num_days: int = 252):
    """
    Benchmark all three implementations.
    """
    print("=" * 70)
    print(f"PERFORMANCE BENCHMARK")
    print(f"Symbol: {symbol}")
    print(f"Simulations: {num_simulations}")
    print(f"Days: {num_days}")
    print("=" * 70)
    print()
    
    # Test 1: Ultra-Optimized (Recommended)
    print("🔥 Testing Ultra-Optimized (Shared Data + Parallel)...")
    start = time.time()
    try:
        results_opt = run_all_simulations_ultra_optimized(symbol, num_simulations, num_days)
        time_opt = time.time() - start
        success_opt = sum(1 for v in results_opt.values() if "error" not in v)
        print(f"   ✅ Completed in {time_opt:.2f} seconds")
        print(f"   ✅ Successful simulations: {success_opt}/22")
        print(f"   ✅ Sample result (GARCH-T): {results_opt.get('GARCH-T', {})}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        time_opt = None
    print()
    
    # Test 2: Parallel
    print("⚡ Testing Parallel (Separate Data Fetching)...")
    start = time.time()
    try:
        results_par = run_all_simulations(symbol, num_simulations, num_days)
        time_par = time.time() - start
        success_par = sum(1 for v in results_par.values() if "error" not in v)
        print(f"   ✅ Completed in {time_par:.2f} seconds")
        print(f"   ✅ Successful simulations: {success_par}/22")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        time_par = None
    print()
    
    # Test 3: Sequential (Optional - only if you have time)
    run_sequential = input("⚠️  Run sequential test? (takes ~35s) [y/N]: ").lower() == 'y'
    
    if run_sequential:
        print("🐌 Testing Sequential (Original - SLOW!)...")
        start = time.time()
        try:
            results_seq = run_all_simulations_sequential(symbol, num_simulations, num_days)
            time_seq = time.time() - start
            success_seq = sum(1 for v in results_seq.values() if "error" not in v)
            print(f"   ✅ Completed in {time_seq:.2f} seconds")
            print(f"   ✅ Successful simulations: {success_seq}/22")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            time_seq = None
        print()
    else:
        time_seq = 35.0  # Approximate baseline
        print(f"   ⏭️  Skipped (baseline: ~{time_seq}s)")
        print()
    
    # Summary
    print("=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)
    
    if time_opt:
        print(f"Ultra-Optimized: {time_opt:.2f}s  {'🥇' if time_opt and (not time_par or time_opt <= time_par) else '🥈'}")
        if time_seq:
            speedup_opt = time_seq / time_opt
            print(f"  → {speedup_opt:.1f}x faster than sequential")
    
    if time_par:
        print(f"Parallel:        {time_par:.2f}s  {'🥇' if time_par and (not time_opt or time_par < time_opt) else '🥈'}")
        if time_seq:
            speedup_par = time_seq / time_par
            print(f"  → {speedup_par:.1f}x faster than sequential")
    
    if time_seq and run_sequential:
        print(f"Sequential:      {time_seq:.2f}s  🐌 (baseline)")
    elif time_seq:
        print(f"Sequential:      ~{time_seq:.0f}s  🐌 (estimated baseline)")
    
    print("=" * 70)
    
    # Recommendation
    print()
    print("📊 RECOMMENDATION:")
    if time_opt and time_opt < 6:
        print("   ✅ Use Ultra-Optimized version (default in API)")
        print("   ✅ Performance is excellent!")
    elif time_opt and time_opt < 10:
        print("   ✅ Use Ultra-Optimized version (default in API)")
        print("   ⚠️  Performance is good, but could be better")
        print("   💡 Try reducing num_simulations or num_days for faster results")
    else:
        print("   ⚠️  Performance seems slower than expected")
        print("   💡 Suggestions:")
        print("      - Check CPU usage")
        print("      - Reduce num_simulations (try 500)")
        print("      - Reduce num_days (try 126)")
        print("      - Check network speed (yfinance data fetching)")
    print()


if __name__ == "__main__":
    print()
    print("🚀 Simulation Performance Benchmark")
    print()
    
    # Default test
    symbol = input("Enter stock symbol (default: RELIANCE): ").strip() or "RELIANCE"
    
    try:
        num_sims = input("Number of simulations (default: 10000): ").strip()
        num_sims = int(num_sims) if num_sims else 10000
    except ValueError:
        num_sims = 10000
    
    try:
        num_days = input("Number of days (default: 252): ").strip()
        num_days = int(num_days) if num_days else 252
    except ValueError:
        num_days = 252
    
    print()
    benchmark_simulations(symbol, num_sims, num_days)
    
    print()
    print("✅ Benchmark complete!")
    print()

