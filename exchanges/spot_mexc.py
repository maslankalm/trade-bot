#!/usr/bin/env python3

import os,time
import requests
import hmac
import hashlib
import json

MEXC_KEY = os.getenv("MEXC_KEY")
MEXC_SECRET = os.getenv("MEXC_SECRET")


def sign_message(message: str, secret_key=MEXC_SECRET) -> str:
    """
    Generate HMAC-SHA256 signature for a given message and secret key.

    :param message: The message to sign
    :param secret_key: The secret key used for signing
    :return: The HMAC-SHA256 signature as a hexadecimal string
    """
    timestamp = (int(time.time() * 1000))
    to_sign = message + f"&timestamp={timestamp}" if message else f"timestamp={timestamp}"

    signature = hmac.new(secret_key.encode(), to_sign.encode(), hashlib.sha256).hexdigest()
    signed_message = f"{to_sign}&signature={signature}"
    return signed_message


def generic_request(endpoint,message="",method="GET",signed=False):
    url = f"https://api.mexc.com/{endpoint}"

    for i in range(5):
        try:
            if signed:
                headers = {"X-MEXC-APIKEY": MEXC_KEY}
                params = sign_message(message)
            else:
                headers = {}
                params = message

            if method == "GET":
                response = requests.get(url,headers=headers,params=params)
            elif method == "POST":
                response = requests.post(url,headers=headers,params=params)
            elif method == "DELETE":
                response = requests.delete(url,headers=headers,params=params)

            # breaking a request rate limit
            if response.status_code in [418,429]:
                print(f"Mexc: Rate Limit: {response.status_code}")
                time.sleep(1)
                continue
            else:
                return json.loads(response.text)
        except Exception as e:
            print("Error:", e)
            print(f"Retrying: {i+1}/5")
            time.sleep(1)
    else:
        return None


def get_order_book(pair: str):
    endpoint = "/api/v3/depth"
    message = f"symbol={pair}"
    response = generic_request(
        endpoint,
        message=message
    )

    return response


def get_my_balances():
    endpoint = "/api/v3/account"
    response = generic_request(
        endpoint,
        signed=True
    )

    return response["balances"]


def get_balance(ticker):
    balances = get_my_balances()
    for balance in balances:
        if balance["asset"] == ticker:
            return balance["free"]
    else:
        return 0


def get_my_orders(pair: str):
    endpoint = "/api/v3/openOrders"
    message = f"symbol={pair}"
    response = generic_request(
        endpoint,
        message=message,
        signed=True
    )

    return response


def put_buy_order(pair: str, amount: float, price: str):
    endpoint = "/api/v3/order"
    message = f"symbol={pair}&side=BUY&type=LIMIT&quantity={amount}&price={price}"
    response = generic_request(
        endpoint,
        message=message,
        signed=True,
        method="POST"
    )
    print(response)
    return response


def put_sell_order(pair: str, amount: float, price: str):
    endpoint = "/api/v3/order"
    message = f"symbol={pair}&side=SELL&type=LIMIT&quantity={amount}&price={price}"
    response = generic_request(
        endpoint,
        message=message,
        signed=True,
        method="POST"
    )

    return response


def cancel_order(pair: str, order_id: str):
    endpoint = "/api/v3/order"
    message = f"symbol={pair}&orderId={order_id}"
    response = generic_request(
        endpoint,
        message=message,
        signed=True,
        method="DELETE"
    )

    return response


def cancel_all_orders(pair):
    endpoint = "/api/v3/openOrders"
    message = f"symbol={pair}"
    response = generic_request(
        endpoint,
        message=message,
        signed=True,
        method="DELETE"
    )

    return response


def get_precision(pair):
    endpoint = "/api/v3/exchangeInfo"
    message = f"symbol={pair}"
    response = generic_request(
        endpoint,
        message=message
    )
    base_precision = response["symbols"][0]["baseAssetPrecision"]
    quote_precision = response["symbols"][0]["quotePrecision"]

    return base_precision, quote_precision
