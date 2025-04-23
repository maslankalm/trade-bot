#!/usr/bin/env python3

import asyncio,re
from core import kyssbot
from workers import trade_bybit as bybit, trade_gate as gate, trade_mexc as mexc, trade_xt as xt

RUNNING = False


### TRADE ###

async def app_core(client, command):
    global RUNNING

    # parse command
    cmd = re.sub(r'\s+', ' ', command).strip().split(" ")
    action = cmd[0].upper()
    ticker = cmd[1].upper() if len(cmd) > 1 else None
    price = cmd[2].upper() if len(cmd) > 2 else "Market"

    # commands
    if action == "SELL":
        if not RUNNING:
            await kyssbot.message(client,f"SELL: {ticker} (Price: {price})","cmd")
            RUNNING = True
            await asyncio.gather(
                gate.sell_on_gate(client,ticker,price,lambda:RUNNING),
                bybit.sell_on_bybit(client,ticker,price,lambda:RUNNING),
                mexc.sell_on_mexc(client,ticker,price,lambda:RUNNING),
                xt.sell_on_xt(client,ticker,price,lambda:RUNNING)
            )
            RUNNING = False
            await kyssbot.message(client,"SELL: Stopped.","cmd")
        else:
            await kyssbot.message(client,"ERROR: Running.","cmd")
            return

    elif action == "BUY":
        if not RUNNING:
            await kyssbot.message(client,f"BUY: {ticker} (Price: {price})","cmd")
            RUNNING = True
            await asyncio.gather(
                gate.buy_on_gate(client,ticker,price,lambda:RUNNING),
                bybit.buy_on_bybit(client,ticker,price,lambda:RUNNING),
                mexc.buy_on_mexc(client,ticker,price,lambda:RUNNING),
                xt.buy_on_xt(client,ticker,price,lambda:RUNNING)
            )
            RUNNING = False
            await kyssbot.message(client,"BUY: Stopped.","cmd")
        else:
            await kyssbot.message(client,"ERROR: Running.","cmd")
            return

    elif action == "PURGE":
        await kyssbot.message(client,"PURGE","cmd")
        await kyssbot.purge_all(client)
        await kyssbot.message(client,"READY","cmd")

    elif action == "PING":
        await kyssbot.message(client,"PONG","cmd")

    else:
        await kyssbot.message(client,"STOP","cmd")
        RUNNING = False

kyssbot.on_command = app_core
kyssbot.connect()
