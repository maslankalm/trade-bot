#!/usr/bin/env python3

import asyncio,math
from core import kyssbot
from exchanges import spot_bybit as bybit

TOKENS = ["ETH"]


### BYBIT ###

async def sell_on_bybit(client,ticker,sell_price,running):
    if ticker not in TOKENS:
        await kyssbot.message(client,f"INFO: {ticker} not supported.","bybit")
        await kyssbot.message(client,"SELL: Stopped.","bybit")
        return

    await kyssbot.message(client,f"SELL: {ticker} (Price: {sell_price})","bybit")
    base_precision,_ = bybit.get_precision(f"{ticker}USDT")

    # validate sell price > highest bid - market buy
    orders = await asyncio.to_thread(bybit.get_order_book,f"{ticker}USDT")
    max_bid = orders['b'][0][0]
    if sell_price == "Market":
        sell_price = 0
    if float(sell_price) < float(max_bid):
        sell_price = max_bid
        await kyssbot.message(client,f"SELL: {ticker} (Market: {sell_price})","bybit")

    while running():
        # get bybit orders
        orders = await asyncio.to_thread(bybit.get_order_book,f"{ticker}USDT")
        price = orders['b'][0][0]
        amount = orders['b'][0][1]

        # proceed with new orders
        if float(price) >= float(sell_price):
            # check minimum order < amount < wallet balance
            balance = await asyncio.to_thread(bybit.get_balance,f"{ticker}")
           # try to release funds from existing orders
            if float(amount) > float(balance):
                await asyncio.to_thread(bybit.cancel_all_orders,f"{ticker}USDT")
                balance = await asyncio.to_thread(bybit.get_balance,f"{ticker}")
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
                await kyssbot.message(client,f"INFO: Not enough {ticker} to sell.","bybit")
                break

            # apply precision
            factor = 10 ** base_precision
            rounded = math.floor(amount * factor) / factor

            # put sell order
            await kyssbot.message(client,f"ORDER: Price: {price} | Amount: {rounded} | Total: {total:.2f}","bybit")
            await asyncio.to_thread(bybit.put_sell_order,f"{ticker}USDT",rounded,price) # str,float,str

        # wait then repeat
        await asyncio.sleep(2)
    await kyssbot.message(client,"SELL: Stopped.","bybit")


async def buy_on_bybit(client,ticker,buy_price,running):
    if ticker not in TOKENS:
        await kyssbot.message(client,f"INFO: {ticker} not supported.","bybit")
        await kyssbot.message(client,"BUY: Stopped.","bybit")
        return

    await kyssbot.message(client,f"BUY: {ticker} (Price: {buy_price})","bybit")
    base_precision,_ = bybit.get_precision(f"{ticker}USDT")

    # validate buy price < lowest ask - market buy
    orders = await asyncio.to_thread(bybit.get_order_book,f"{ticker}USDT")
    min_ask = orders["a"][0][0]
    if buy_price == "Market":
        buy_price = 1000000
    if float(buy_price) > float(min_ask):
        buy_price = min_ask
        await kyssbot.message(client,f"BUY: {ticker} (Market: {buy_price})","bybit")

    while running():
        # get bybit orders
        orders = await asyncio.to_thread(bybit.get_order_book,f"{ticker}USDT")
        price = orders["a"][0][0]
        amount = orders["a"][0][1]

        # proceed with new orders
        if float(price) <= float(buy_price):
            # check minimum order < amount < usdt balance
            balance = await asyncio.to_thread(bybit.get_balance,"USDT")
            total = float(price) * float(amount)
            # try to release funds from existing orders
            if float(total) > float(balance):
                await asyncio.to_thread(bybit.cancel_all_orders,f"{ticker}USDT")
                balance = await asyncio.to_thread(bybit.get_balance,"USDT")
            # use all available funds
            if float(total) > float(balance):
                total = float(balance)
            # validate total vs minimum order
            if total < 3:
                total = 5
            # stop if there is nothing we can do
            if total > float(balance):
                await kyssbot.message(client,f"INFO: Not enough USDT to buy.","bybit")
                break
            else:
                amount = total / float(price)

            # apply precision
            factor = 10 ** base_precision
            rounded = math.floor(amount * factor) / factor

            # put buy order
            await kyssbot.message(client,f"ORDER: Price: {price} | Amount: {rounded} | Total: {total:.2f}","bybit")
            await asyncio.to_thread(bybit.put_buy_order,f"{ticker}USDT",rounded,price) # str,float,str

        # wait then repeat
        await asyncio.sleep(2)
    await kyssbot.message(client,"BUY: Stopped.","bybit")
