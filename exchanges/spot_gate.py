#!/usr/bin/env python3

import os,time
import gate_api
from gate_api.exceptions import ApiException, GateApiException


GATE_KEY = os.getenv("GATE_KEY")
GATE_SECRET = os.getenv("GATE_SECRET")


def create_spot_api(key=GATE_KEY,secret=GATE_SECRET):
    configuration = gate_api.Configuration(
        key=key,
        secret=secret,
        host="https://api.gateio.ws/api/v4"
    )
    api_client = gate_api.ApiClient(configuration)
    spot_api = gate_api.SpotApi(api_client)
    return spot_api


def get_my_balances():
    """
    Retrieve and print all spot account balances.
    """
    spot_api = create_spot_api()
    for i in range(5):
        try:
            accounts = spot_api.list_spot_accounts()
            return accounts
        except (ApiException, GateApiException) as e:
            print("Error getting wallet balance:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_order_book(pair: str):
    """
    Retrieve and print the current order book for the specified trading pair.

    Parameter:
      pair - Trading pair in native format (e.g. "BTC_USDT")
    """
    spot_api = create_spot_api()
    for i in range(5):
        try:
            order_book = spot_api.list_order_book(currency_pair=pair)
            return order_book
        except (ApiException, GateApiException) as e:
            print("Error getting order book:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def cancel_order(pair: str, order_id: str):
    """
    Cancel an order by its ID for the specified trading pair.

    Parameters:
      pair     - Trading pair in native format (e.g. "BTC_USDT")
      order_id - The ID of the order to cancel
    """
    spot_api = create_spot_api()
    for i in range(5):
        try:
            result = spot_api.cancel_order(order_id, pair)
            return result
        except (ApiException, GateApiException) as e:
            print("Error cancelling order:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_my_orders(pair: str):
    """
    Retrieve and print a list of active (open) orders for the specified trading pair.

    Parameter:
      pair - Trading pair in native format (e.g. "BTC_USDT")
    """
    spot_api = create_spot_api()
    for i in range(5):
        try:
            orders = spot_api.list_orders(currency_pair=pair, status="open")
            return orders
        except (ApiException, GateApiException) as e:
            print("Error retrieving active orders:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def put_buy_order(pair: str, amount: float, price: str):
    """
    Place a buy order on the specified trading pair.

    Parameters:
      pair   - Trading pair in Gate.io native format (e.g. "BTC_USDT")
      amount - Order amount (float)
      price  - Order price (as a string)
    """
    spot_api = create_spot_api()
    order = gate_api.Order(
        currency_pair=pair,
        side="buy",
        amount=str(amount),
        price=price
    )
    for i in range(5):
        try:
            result = spot_api.create_order(order)
            return result
        except (ApiException, GateApiException) as e:
            print("Error placing buy order:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def put_sell_order(pair: str, amount: float, price: str):
    """
    Place a sell order on the specified trading pair.

    Parameters:
      pair   - Trading pair in Gate.io native format (e.g. "BTC_USDT")
      amount - Order amount (float)
      price  - Order price (as a string)
    """
    spot_api = create_spot_api()
    order = gate_api.Order(
        currency_pair=pair,
        side="sell",
        amount=str(amount),
        price=price
    )
    for i in range(5):
        try:
            result = spot_api.create_order(order)
            return result
        except (ApiException, GateApiException) as e:
            print("Error placing sell order:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_balance(ticker):
    accounts = get_my_balances()
    for account in accounts:
        if ticker == account.currency:
            return account.available
    else:
        return None


def cancel_all_orders(pair):
    my_orders=get_my_orders(pair)
    for order in my_orders:
        cancel_order(order.currency_pair,order.id)
