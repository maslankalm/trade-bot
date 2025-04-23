#!/usr/bin/env python3

import asyncio,math
from core import kyssbot
from exchanges import spot_xt as xt

TOKENS = ["ETH"]


## xt ###

def apply_precision(amount, precision=0, multiplier=None):
    if multiplier:
        rounded = math.floor(float(amount) / int(multiplier)) * int(multiplier)
    else:
        factor = 10 ** precision
        rounded = math.floor(float(amount) * factor) / factor
    return rounded


async def sell_on_xt(client,ticker,sell_price,running):
    if ticker not in TOKENS:
        await kyssbot.message(client,f"INFO: {ticker} not supported.","xt")
        await kyssbot.message(client,"SELL: Stopped.","xt")
        return

    await kyssbot.message(client,f"SELL: {ticker} (Price: {sell_price})","xt")
    base_precision, price_multiple = xt.get_symbol_info(f"{ticker}_USDT")

    # validate sell price > highest bid - market buy
    orders = await asyncio.to_thread(xt.get_order_book,f"{ticker}_USDT")
    max_bid = orders["bids"][0][0]
    if sell_price == "Market":
        sell_price = 0
    if float(sell_price) < float(max_bid):
        sell_price = max_bid
        await kyssbot.message(client,f"SELL: {ticker} (Market: {sell_price})","xt")

    while running():
        # get xt orders
        orders = await asyncio.to_thread(xt.get_order_book,f"{ticker}_USDT")
        price = orders["bids"][0][0]
        amount = orders["bids"][0][1]

        # proceed with new orders
        if float(price) >= float(sell_price):
            # check minimum order < amount < wallet balance
            balance = await asyncio.to_thread(xt.get_balance,f"{ticker}")
            # try to release funds from existing orders
            if float(amount) > float(balance):
                await asyncio.to_thread(xt.cancel_all_orders,f"{ticker}_USDT")
                balance = await asyncio.to_thread(xt.get_balance,f"{ticker}")
            # use all available funds
            if float(amount) > float(balance):
                amount = float(balance)
            # validate total vs minimum order
            total = float(price) * float(amount)
            if total < 3:
                total = 5
                amount = total / float(price)
            # stop if there is nothing we can do
            if float(amount) > float(balance):
                await kyssbot.message(client,f"INFO: Not enough {ticker} to sell.","xt")
                break

            # apply precision
            if price_multiple:
                rounded = apply_precision(amount,multiplier=price_multiple)
            else:
                rounded = apply_precision(amount,base_precision)

            # put sell order if rounded > 0
            if rounded:
                await kyssbot.message(client,f"ORDER: Price: {price} | Amount: {rounded} | Total: {total:.2f}","xt")
                await asyncio.to_thread(xt.put_sell_order,f"{ticker}_USDT",rounded,price) # str,float,str

        # wait then repeat
        await asyncio.sleep(2)
    await kyssbot.message(client,"SELL: Stopped.","xt")


async def buy_on_xt(client,ticker,buy_price,running):
    if ticker not in TOKENS:
        await kyssbot.message(client,f"INFO: {ticker} not supported.","xt")
        await kyssbot.message(client,"BUY: Stopped.","xt")
        return

    await kyssbot.message(client,f"BUY: {ticker} (Price: {buy_price})","xt")
    base_precision, price_multiple = xt.get_symbol_info(f"{ticker}_USDT")

    # validate buy price < lowest ask - market buy
    orders = await asyncio.to_thread(xt.get_order_book,f"{ticker}_USDT")
    min_ask = orders["asks"][0][0]
    if buy_price == "Market":
        buy_price = 1000000
    if float(buy_price) > float(min_ask):
        buy_price = min_ask
        await kyssbot.message(client,f"BUY: {ticker} (Market: {buy_price})","xt")

    while running():
        # get xt orders
        orders = await asyncio.to_thread(xt.get_order_book,f"{ticker}_USDT")
        price = orders["asks"][0][0]
        amount = orders["asks"][0][1]

        # proceed with new orders
        if float(price) <= float(buy_price):
            # check minimum order < amount < usdt balance
            balance = apply_precision(await asyncio.to_thread(xt.get_balance,"USDT"))
            total = float(price) * float(amount)
            # try to release funds from existing orders
            if float(total) > float(balance):
                await asyncio.to_thread(xt.cancel_all_orders,f"{ticker}_USDT")
                balance = apply_precision(await asyncio.to_thread(xt.get_balance,"USDT"))
            # use all available funds
            if float(total) > float(balance):
                total = float(balance)
            # validate total vs minimum order
            if total < 3:
                total = 5
            # stop if there is nothing we can do
            if total > float(balance):
                await kyssbot.message(client,f"INFO: Not enough USDT to buy.","xt")
                break
            else:
                amount = total / float(price)

            # apply precision
            if price_multiple:
                rounded = apply_precision(amount,multiplier=price_multiple)
            else:
                rounded = apply_precision(amount,base_precision)

            # put buy order if rounded > 0
            if rounded:
                await kyssbot.message(client,f"ORDER: Price: {price} | Amount: {rounded} | Total: {total:.2f}","xt")
                await asyncio.to_thread(xt.put_buy_order,f"{ticker}_USDT",rounded,price) # str,float,str

        # wait then repeat
        await asyncio.sleep(2)
    await kyssbot.message(client,"BUY: Stopped.","xt")
