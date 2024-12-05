import requests
import schedule
import time
from datetime import datetime

# Delta Exchange API keys (replace with your actual keys)
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
BASE_URL = 'https://api.delta.exchange'

# Headers for authentication
headers = {
    'api-key': API_KEY,
    'Content-Type': 'application/json'
}

# Function to place a trade
def place_trade(symbol, side, quantity, leverage):
    # Set leverage for the trade
    leverage_url = f"{BASE_URL}/v2/orders/leverage"
    leverage_payload = {
        "product_id": get_product_id(symbol),
        "leverage": leverage
    }
    requests.post(leverage_url, json=leverage_payload, headers=headers)

    # Place market order
    order_url = f"{BASE_URL}/v2/orders"
    order_payload = {
        "product_id": get_product_id(symbol),
        "size": quantity,
        "side": side,
        "order_type": "market"
    }
    response = requests.post(order_url, json=order_payload, headers=headers)
    order_data = response.json()
    
    if response.status_code == 200:
        print(f"{side.capitalize()} order placed for {symbol}: {order_data}")
        order_id = order_data['result']['id']
        set_stop_and_target(symbol, order_id, side)
    else:
        print(f"Error placing order: {response.json()}")

# Function to get product ID for a given symbol
def get_product_id(symbol):
    url = f"{BASE_URL}/products"
    response = requests.get(url)
    products = response.json()['result']
    product = next((p for p in products if p['symbol'] == symbol), None)
    return product['id'] if product else None

# Function to set stop-loss and target
def set_stop_and_target(symbol, order_id, side):
    entry_price = get_order_price(order_id)
    stop_loss = calculate_stop_loss(entry_price, side)
    target = calculate_target(entry_price, side)
    
    trailing_stop = {
        "order_id": order_id,
        "stop_price": stop_loss,
        "target_price": target,
        "trailing_delta": 2  # Trailing stop of 2 points
    }

    # Simulate placing stop-loss and target
    print(f"Setting stop-loss for {symbol}: {stop_loss}, target: {target}, trailing delta: 2")

# Helper function to calculate stop-loss
def calculate_stop_loss(entry_price, side):
    stop_loss = entry_price * (1 - 0.035) if side == 'buy' else entry_price * (1 + 0.035)
    return round(stop_loss, 2)

# Helper function to calculate target
def calculate_target(entry_price, side):
    target = entry_price * (1 + 0.07) if side == 'buy' else entry_price * (1 - 0.07)
    return round(target, 2)

# Function to fetch the executed order price
def get_order_price(order_id):
    order_url = f"{BASE_URL}/v2/orders/{order_id}"
    response = requests.get(order_url, headers=headers)
    return response.json()['result']['price']

# Main task to execute daily trades
def daily_trades():
    place_trade('TRX/USDT', 'buy', 100, 10)  # Replace quantity as needed
    place_trade('TRX/USDT', 'sell', 100, 10)

# Schedule the task every day at 9:30 AM
schedule.every().day.at("09:30").do(daily_trades)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
