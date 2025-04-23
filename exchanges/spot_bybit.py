#!/usr/bin/env python3

from pybit.unified_trading import HTTP
import os,time


BYBIT_KEY = os.getenv("BYBIT_KEY")
BYBIT_SECRET = os.getenv("BYBIT_SECRET")


def create_spot_api(key=BYBIT_KEY, secret=BYBIT_SECRET):
    """
    Create and return a Bybit Unified Trading HTTP session for spot trading in production.
    """
    session = HTTP(testnet=False, api_key=key, api_secret=secret)
    return session


def get_my_balances():
    """
    Retrieve and return all spot wallet balances.
    """
    session = create_spot_api()
    for i in range(5):
        try:
            resp = session.get_wallet_balance(category='spot', accountType='UNIFIED')
            return resp["result"]
        except Exception as e:
            print("Error getting wallet balance:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_order_book(pair: str, limit=5):
    """
    Retrieve and return the current order book for the specified trading pair.

    Parameters:
      pair - Trading pair (e.g. "BTCUSDT")
    """
    session = create_spot_api()
    for i in range(5):
        try:
            resp = session.get_orderbook(category="spot", symbol=pair,limit=limit)
            return resp["result"]
        except Exception as e:
            print("Error getting order book:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def cancel_order(pair: str, order_id: str):
    """
    Cancel an order by its ID for the specified trading pair.

    Parameters:
      pair     - Trading pair in Bybit format (e.g. "BTCUSDT")
      order_id - The Bybit order ID to cancel
    """
    session = create_spot_api()
    for i in range(5):
        try:
            resp = session.cancel_order(category="spot", symbol=pair, orderId=order_id)
            return resp["result"]
        except Exception as e:
            print("Error cancelling order:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_my_orders(pair: str,limit=50):
    """
    Retrieve and return active (open) orders for the specified trading pair.

    Parameters:
      pair - Trading pair in Bybit format (e.g. "BTCUSDT")
    """
    session = create_spot_api()
    for i in range(5):
        try:
            resp = session.get_open_orders(category="spot", symbol=pair, limit=limit)
            return resp["result"]["list"]
        except Exception as e:
            print("Error retrieving active orders:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def cancel_all_orders(pair: str,limit=50):
    """
    Cancel all active orders for the specified trading pair.
    """
    session = create_spot_api()
    for i in range(5):
        try:
            resp = session.cancel_all_orders(category="spot", symbol=pair, limit=limit)
            return resp["result"]
        except Exception as e:
            print("Error retrieving active orders:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def put_buy_order(pair: str, amount: float, price: str):
    """
    Place a buy (limit) order on the specified trading pair.

    Parameters:
      pair   - Trading pair in Bybit format (e.g. "BTCUSDT")
      amount - Order amount (float)
      price  - Order price (as a string)
    """
    session = create_spot_api()
    order_data = {
        "category": "spot",
        "symbol": pair,
        "side": "Buy",
        "orderType": "Limit",
        "qty": str(amount),
        "price": price,
        "timeInForce": "GTC",
        "isLeverage": 0,
        "orderFilter": "Order"
    }
    for i in range(5):
        try:
            resp = session.place_order(**order_data)
            return resp["result"]
        except Exception as e:
            print("Error placing buy order:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def put_sell_order(pair: str, amount: float, price: str):
    """
    Place a sell (limit) order on the specified trading pair.

    Parameters:
      pair   - Trading pair in Bybit format (e.g. "BTCUSDT")
      amount - Order amount (float)
      price  - Order price (as a string)
    """
    session = create_spot_api()
    order_data = {
        "category": "spot",
        "symbol": pair,
        "side": "Sell",
        "orderType": "Limit",
        "qty": str(amount),
        "price": price,
        "timeInForce": "GTC",
        "isLeverage": 0,
        "orderFilter": "Order"
    }
    for i in range(5):
        try:
            resp = session.place_order(**order_data)
            return resp["result"]
        except Exception as e:
            print("Error placing sell order:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_pair_info(pair):
    session = create_spot_api()
    for i in range(5):
        try:
            resp = session.get_instruments_info(category="spot", symbol=pair)
            return resp["result"]
        except Exception as e:
            print("Error retrieving apair info:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_balance(ticker):
    """
    Retrieve available balance for the specified ticker (e.g. "BTC").
    """
    balances = get_my_balances()
    for coin in balances["list"][0]["coin"]:
        if coin["coin"] == ticker:
            return float(coin["walletBalance"])
    else:
        return 0


def get_precision(pair):
    pair_info = get_pair_info(pair)
    for info in pair_info["list"]:
        if info["symbol"] == pair:
            pair_quote_precision = info["lotSizeFilter"]["quotePrecision"]
            quote_precision = len(pair_quote_precision.split(".")[1])
            pair_base_precision = info["lotSizeFilter"]["basePrecision"]
            base_precision = len(pair_base_precision.split(".")[1])
            return base_precision, quote_precision
    else:
        return None, None
