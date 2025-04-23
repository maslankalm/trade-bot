#!/usr/bin/env python3

import asyncio
from core import kyssbot
from exchanges import spot_gate as gate

TOKENS = ["ETH"]


## GATE ###

async def sell_on_gate(client,ticker,sell_price,running):
    if ticker not in TOKENS:
        await kyssbot.message(client,f"INFO: {ticker} not supported.","gate")
        await kyssbot.message(client,"SELL: Stopped.","gate")
        return

    await kyssbot.message(client,f"SELL: {ticker} (Price: {sell_price})","gate")

    # validate sell price > highest bid - market buy
    orders = await asyncio.to_thread(gate.get_order_book,f"{ticker}_USDT")
    max_bid = orders.bids[0][0]
    if sell_price == "Market":
        sell_price = 0
    if float(sell_price) < float(max_bid):
        sell_price = max_bid
        await kyssbot.message(client,f"SELL: {ticker} (Market: {sell_price})","gate")

    while running():
        # get gate orders
        orders = await asyncio.to_thread(gate.get_order_book,f"{ticker}_USDT")
        price = orders.bids[0][0]
        amount = orders.bids[0][1]

        # proceed with new orders
        if float(price) >= float(sell_price):
            # check minimum order < amount < wallet balance
            balance = await asyncio.to_thread(gate.get_balance,f"{ticker}")
            # try to release funds from existing orders
            if float(amount) > float(balance):
                await asyncio.to_thread(gate.cancel_all_orders,f"{ticker}_USDT")
                balance = await asyncio.to_thread(gate.get_balance,f"{ticker}")
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
                await kyssbot.message(client,f"INFO: Not enough {ticker} to sell.","gate")
                break

            # put sell order
            await kyssbot.message(client,f"ORDER: Price: {price} | Amount: {amount} | Total: {total:.2f}","gate")
            await asyncio.to_thread(gate.put_sell_order,f"{ticker}_USDT",amount,price) # str,float,str

        # wait then repeat
        await asyncio.sleep(2)
    await kyssbot.message(client,"SELL: Stopped.","gate")


async def buy_on_gate(client,ticker,buy_price,running):
    if ticker not in TOKENS:
        await kyssbot.message(client,f"INFO: {ticker} not supported.","gate")
        await kyssbot.message(client,"BUY: Stopped.","gate")
        return

    await kyssbot.message(client,f"BUY: {ticker} (Price: {buy_price})","gate")

    # validate buy price < lowest ask - market buy
    orders = await asyncio.to_thread(gate.get_order_book,f"{ticker}_USDT")
    min_ask = orders.asks[0][0]
    if buy_price == "Market":
        buy_price = 1000000
    if float(buy_price) > float(min_ask):
        buy_price = min_ask
        await kyssbot.message(client,f"BUY: {ticker} (Market: {buy_price})","gate")

    while running():
        # get gate orders
        orders = await asyncio.to_thread(gate.get_order_book,f"{ticker}_USDT")
        price = orders.asks[0][0]
        amount = orders.asks[0][1]

        # proceed with new orders
        if float(price) <= float(buy_price):
            # check minimum order < amount < usdt balance
            balance = await asyncio.to_thread(gate.get_balance,"USDT")
            total = float(price) * float(amount)
            # try to release funds from existing orders
            if float(total) > float(balance):
                await asyncio.to_thread(gate.cancel_all_orders,f"{ticker}_USDT")
                balance = await asyncio.to_thread(gate.get_balance,"USDT")
            # use all available funds
            if float(total) > float(balance):
                total = float(balance)
            # validate total vs minimum order
            if total < 3:
                total = 5
            # stop if there is nothing we can do
            if total > float(balance):
                await kyssbot.message(client,f"INFO: Not enough USDT to buy.","gate")
                break
            else:
                amount = total / float(price)

            # put buy order
            await kyssbot.message(client,f"ORDER: Price: {price} | Amount: {amount} | Total: {total:.2f}","gate")
            await asyncio.to_thread(gate.put_buy_order,f"{ticker}_USDT",amount,price) # str,float,str

        # wait then repeat
        await asyncio.sleep(2)
    await kyssbot.message(client,"BUY: Stopped.","gate")
