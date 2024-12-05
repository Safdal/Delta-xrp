import requests
import schedule
import time
from datetime import datetime, timedelta

# Delta Exchange API endpoints
BASE_URL = "https://api.delta.exchange"
PLACE_ORDER_URL = f"{BASE_URL}/orders"
AUTH_URL = f"{BASE_URL}/auth"

# Replace with your Delta Exchange API keys
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

# Helper function for authentication
def get_auth_headers():
    return {
        "api-key": API_KEY,
        "api-secret": API_SECRET,
        "Content-Type": "application/json"
    }

# Place an order
def place_order(symbol, side, size, stop_loss, target, trailing_points):
    order_data = {
        "product_id": symbol,
        "side": side,  # 'buy' or 'sell'
        "size": size,
        "type": "market",  # Market order
        "stop_loss": stop_loss,
        "take_profit": target,
        "trailing_points": trailing_points
    }
    
    try:
        response = requests.post(PLACE_ORDER_URL, json=order_data, headers=get_auth_headers())
        if response.status_code == 200:
            print(f"Order placed successfully: {response.json()}")
        else:
            print(f"Failed to place order: {response.text}")
    except Exception as e:
        print(f"Error placing order: {e}")

# Task to execute at 9:30 AM
def execute_trades():
    print("Starting trade automation at 9:30 AM...")
    symbol = "TRX/USD"  # Replace with the correct product ID
    size = 100  # Set appropriate trade size
    
    # Buy Trade
    place_order(symbol, "buy", size, stop_loss=3.5, target=7, trailing_points=2)
    
    # Short Trade
    place_order(symbol, "sell", size, stop_loss=3.5, target=7, trailing_points=2)

# Schedule the task to run daily at 9:30 AM
schedule.every().day.at("09:30").do(execute_trades)

print("Trade automation initialized. Waiting for 9:30 AM IST...")
while True:
    schedule.run_pending()
    time.sleep(1)
