import requests
import schedule
import time
from datetime import datetime, timedelta

# Delta Exchange API credentials
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
BASE_URL = 'https://api.delta.exchange'

# Headers for authenticated requests
HEADERS = {
    'api-key': API_KEY,
    'Content-Type': 'application/json'
}

# Function to place a market order
def place_order(symbol, side, leverage, quantity):
    url = f"{BASE_URL}/orders"
    payload = {
        "product_id": get_product_id(symbol),
        "side": side,
        "size": quantity,
        "order_type": "market",
        "leverage": leverage
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

# Get product ID for TRX/USD Futures
def get_product_id(symbol):
    url = f"{BASE_URL}/products"
    response = requests.get(url)
    products = response.json()['result']
    for product in products:
        if product['symbol'] == symbol:
            return product['id']
    raise Exception(f"Product {symbol} not found.")

# Function to set stop loss and take profit orders
def set_stop_and_target(order_id, entry_price, stop_loss_pct, take_profit_pct, trailing_stop_pct):
    stop_loss_price = entry_price * (1 - stop_loss_pct / 100)
    take_profit_price = entry_price * (1 + take_profit_pct / 100)
    trailing_stop_price = entry_price * (1 + trailing_stop_pct / 100)

    # Example of setting a stop loss
    # Adjust stop loss orders as price moves
    # Repeat for trailing stops and take profit
    print(f"Stop Loss: {stop_loss_price}, Take Profit: {take_profit_price}, Trailing Stop Loss: {trailing_stop_price}")

# Main function to execute trades
def execute_trades():
    try:
        # Place Buy Trade
        buy_response = place_order('TRX/USD', 'buy', 10, 10)
        print("Buy Trade Response:", buy_response)

        # Place Short Sell Trade
        sell_response = place_order('TRX/USD', 'sell', 10, 10)
        print("Sell Trade Response:", sell_response)
    except Exception as e:
        print(f"Failed to execute trades: {str(e)}")

# Schedule trades every day at 9:30AM
schedule.every().day.at("09:30").do(execute_trades)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
