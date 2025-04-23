#!/usr/bin/env python3

import os,time
from pyxt.spot import Spot


XT_KEY = os.getenv("XT_KEY")
XT_SECRET = os.getenv("XT_SECRET")


def create_spot_api(key=XT_KEY,secret=XT_SECRET):
    spot_api = Spot(host="https://sapi.xt.com", access_key=key, secret_key=secret)
    return spot_api


def get_my_balances():
    spot_api = create_spot_api()
    for i in range(5):
        try:
            balances = spot_api.balances()
            return balances
        except Exception as e:
            print("Error:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_order_book(pair: str):
    spot_api = create_spot_api()
    for i in range(5):
        try:
            order_book = spot_api.get_depth(
                symbol=pair.lower()
            )
            return order_book
        except Exception as e:
            print("Error:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def cancel_order(order_id):
    spot_api = create_spot_api()
    for i in range(5):
        try:
            cancel_order = spot_api.cancel_order(
                order_id=order_id
            )
            return cancel_order
        except Exception as e:
            print("Error:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_my_orders(pair: str):
    spot_api = create_spot_api()
    for i in range(5):
        try:
            open_orders = spot_api.get_open_orders(
                symbol=pair.lower()
            )
            return open_orders
        except Exception as e:
            print("Error:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def put_buy_order(pair: str, amount: float, price: str):
    spot_api = create_spot_api()
    for i in range(5):
        try:
            buy_order = spot_api.order(
                symbol=pair.lower(),
                price=str(price),
                quantity=str(amount),
                side="BUY",
                type="LIMIT"
            )
            return buy_order
        except Exception as e:
            print("Error:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def put_sell_order(pair: str, amount: float, price: str):
    spot_api = create_spot_api()
    for i in range(5):
        try:
            sell_order = spot_api.order(
                symbol=pair.lower(),
                price=str(price),
                quantity=str(amount),
                side="SELL",
                type="LIMIT"
            )
            return sell_order
        except Exception as e:
            print("Error:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_balance(ticker):
    spot_api = create_spot_api()
    for i in range(5):
        try:
            balance = spot_api.balance(
                ticker.lower()
            )
            return balance["availableAmount"]
        except Exception as e:
            print("Error:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def cancel_all_orders(pair):
    spot_api = create_spot_api()
    for i in range(5):
        try:
            cancel_orders = spot_api.cancel_open_orders(
                symbol=pair.lower()
            )
            return cancel_orders
        except Exception as e:
            print("Error:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_symbol_info(pair):
    spot_api = create_spot_api()
    for i in range(5):
        try:
            symbol_info = spot_api.get_symbol_config(
                symbol=pair.lower()
            )
            quantity_precision = symbol_info[0]["quantityPrecision"]
            for filter in symbol_info[0]["filters"]:
                if filter["filter"] == "PROTECTION_ONLINE":
                    if "maxPriceMultiple" in filter:
                        price_multiple = filter["maxPriceMultiple"]
                        break
            else:
                price_multiple = None
            return quantity_precision, price_multiple
        except Exception as e:
            print("Error:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None

