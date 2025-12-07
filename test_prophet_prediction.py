"""
Test script for Prophet Stock Price Prediction API

This script demonstrates how to use the Prophet prediction endpoints
and validates that the service is working correctly.

Usage:
    python test_prophet_prediction.py
"""

import requests
import json
from datetime import datetime


# API Configuration
BASE_URL = "http://localhost:8000/api"
PREDICTION_ENDPOINT = f"{BASE_URL}/prediction"


def test_basic_prediction(symbol: str, forecast_days: int = 30):
    """
    Test basic stock price prediction endpoint
    """
    print(f"\n{'='*70}")
    print(f"Testing Basic Prediction for {symbol}")
    print(f"{'='*70}")
    
    try:
        url = f"{PREDICTION_ENDPOINT}/{symbol}"
        params = {"forecast_days": forecast_days}
        
        print(f"\n📡 Making request to: {url}")
        print(f"   Parameters: {params}")
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Display results
        print(f"\n✅ Success! Got prediction for {data['symbol']}")
        print(f"\n📊 Analysis Period:")
        print(f"   Start: {data['analysis_period']['start_date']}")
        print(f"   End: {data['analysis_period']['end_date']}")
        print(f"   Days Analyzed: {data['analysis_period']['days_analyzed']}")
        
        print(f"\n💰 Current Price:")
        print(f"   Value: ₹{data['current_price']['value']:,.2f}")
        print(f"   Date: {data['current_price']['date']}")
        
        print(f"\n🔮 Prediction ({forecast_days} days):")
        pred = data['prediction']
        print(f"   Predicted Price: ₹{pred['predicted_price']:,.2f}")
        print(f"   Lower Bound: ₹{pred['lower_bound']:,.2f}")
        print(f"   Upper Bound: ₹{pred['upper_bound']:,.2f}")
        print(f"   Expected Change: ₹{pred['price_change']:,.2f} ({pred['price_change_percent']}%)")
        print(f"   Direction: {pred['direction'].upper()} {'📈' if pred['direction'] == 'bullish' else '📉'}")
        
        print(f"\n📈 Model Performance:")
        perf = data['model_performance']
        print(f"   MAE: {perf['mae']:,.2f}")
        print(f"   RMSE: {perf['rmse']:,.2f}")
        print(f"   MAPE: {perf['mape']:.2f}%")
        
        print(f"\n🔍 Trend Components:")
        trend = data['trend_components']
        print(f"   Weekly Seasonality: {'Yes' if trend['has_weekly_seasonality'] else 'No'}")
        print(f"   Yearly Seasonality: {'Yes' if trend['has_yearly_seasonality'] else 'No'}")
        print(f"   Changepoints Detected: {trend['changepoints_detected']}")
        
        print(f"\n📅 First 5 Forecast Days:")
        for i, forecast in enumerate(data['forecast_data'][:5], 1):
            print(f"   {i}. {forecast['date']}: ₹{forecast['predicted_price']:,.2f} "
                  f"(Range: ₹{forecast['lower_bound']:,.2f} - ₹{forecast['upper_bound']:,.2f})")
        
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ HTTP Error: {e}")
        print(f"   Response: {response.text}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_detailed_analysis(symbol: str, forecast_days: int = 30):
    """
    Test detailed trend analysis endpoint
    """
    print(f"\n{'='*70}")
    print(f"Testing Detailed Analysis for {symbol}")
    print(f"{'='*70}")
    
    try:
        url = f"{PREDICTION_ENDPOINT}/{symbol}/detailed"
        params = {"forecast_days": forecast_days}
        
        print(f"\n📡 Making request to: {url}")
        print(f"   Parameters: {params}")
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Display results
        print(f"\n✅ Success! Got detailed analysis for {data['symbol']}")
        
        print(f"\n📈 Trend Analysis (First 5 days):")
        for i, trend in enumerate(data['trend_analysis'][:5], 1):
            print(f"   {i}. {trend['date']}:")
            print(f"      Overall Trend: ₹{trend['trend']:,.2f}")
            print(f"      Weekly Effect: {trend['weekly_effect']:+.2f}")
            print(f"      Yearly Effect: {trend['yearly_effect']:+.2f}")
        
        print(f"\n🔄 Recent Changepoints (Last 5):")
        for i, cp in enumerate(data['changepoints'][-5:], 1):
            print(f"   {i}. {cp['date']} (Index: {cp['index']})")
        
        print(f"\n📖 Component Descriptions:")
        for key, desc in data['description'].items():
            print(f"   {key}: {desc}")
        
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ HTTP Error: {e}")
        print(f"   Response: {response.text}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_multiple_symbols():
    """
    Test prediction for multiple stock symbols
    """
    print(f"\n{'='*70}")
    print(f"Testing Multiple Symbols")
    print(f"{'='*70}")
    
    symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK"]
    results = {}
    
    for symbol in symbols:
        try:
            url = f"{PREDICTION_ENDPOINT}/{symbol}"
            params = {"forecast_days": 7}
            
            print(f"\n📊 Fetching {symbol}...", end=" ")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results[symbol] = {
                'current': data['current_price']['value'],
                'predicted': data['prediction']['predicted_price'],
                'change_percent': data['prediction']['price_change_percent'],
                'direction': data['prediction']['direction']
            }
            print("✅")
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}")
            results[symbol] = None
    
    # Display comparison
    print(f"\n{'='*70}")
    print(f"Stock Comparison (7-day forecast)")
    print(f"{'='*70}")
    print(f"\n{'Symbol':<12} {'Current':<12} {'Predicted':<12} {'Change %':<12} {'Direction'}")
    print(f"{'-'*70}")
    
    for symbol, data in results.items():
        if data:
            direction_icon = '📈' if data['direction'] == 'bullish' else '📉'
            print(f"{symbol:<12} ₹{data['current']:<11,.2f} ₹{data['predicted']:<11,.2f} "
                  f"{data['change_percent']:>10.2f}% {direction_icon} {data['direction']}")
        else:
            print(f"{symbol:<12} {'Error':>50}")


def test_different_forecast_periods(symbol: str):
    """
    Test predictions for different forecast periods
    """
    print(f"\n{'='*70}")
    print(f"Testing Different Forecast Periods for {symbol}")
    print(f"{'='*70}")
    
    periods = [7, 30, 90, 180]
    
    print(f"\n{'Period':<10} {'Predicted Price':<18} {'Change %':<12} {'Direction'}")
    print(f"{'-'*60}")
    
    for days in periods:
        try:
            url = f"{PREDICTION_ENDPOINT}/{symbol}"
            params = {"forecast_days": days}
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            pred = data['prediction']
            
            direction_icon = '📈' if pred['direction'] == 'bullish' else '📉'
            print(f"{days} days{'':<4} ₹{pred['predicted_price']:<16,.2f} "
                  f"{pred['price_change_percent']:>10.2f}% {direction_icon} {pred['direction']}")
            
        except Exception as e:
            print(f"{days} days{'':<4} Error: {str(e)[:40]}")


def check_server():
    """
    Check if the server is running
    """
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """
    Main test function
    """
    print("\n" + "="*70)
    print("Prophet Stock Price Prediction API - Test Suite")
    print("="*70)
    print(f"\nTest started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if server is running
    print(f"\n🔍 Checking server status...")
    if not check_server():
        print(f"\n❌ Server is not running!")
        print(f"\n💡 Please start the server first:")
        print(f"   uvicorn app.main:app --reload")
        return
    
    print(f"✅ Server is running!")
    
    # Run tests
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Basic prediction for RELIANCE
    tests_total += 1
    if test_basic_prediction("RELIANCE", 30):
        tests_passed += 1
    
    # Test 2: Detailed analysis for TCS
    tests_total += 1
    if test_detailed_analysis("TCS", 30):
        tests_passed += 1
    
    # Test 3: Multiple symbols comparison
    test_multiple_symbols()
    
    # Test 4: Different forecast periods
    test_different_forecast_periods("INFY")
    
    # Summary
    print(f"\n{'='*70}")
    print(f"Test Summary")
    print(f"{'='*70}")
    print(f"\n✅ Tests Passed: {tests_passed}/{tests_total}")
    print(f"\n⏱️  Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n📚 Next Steps:")
    print(f"   1. Access Swagger UI: http://localhost:8000/docs")
    print(f"   2. Navigate to 'Stock Price Prediction' section")
    print(f"   3. Try different symbols and forecast periods")
    print(f"   4. Review the detailed documentation in PROPHET_PREDICTION_README.md")
    
    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    main()

