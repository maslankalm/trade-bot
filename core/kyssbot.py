#!/usr/bin/env python3

import os
import discord
import socket

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

CHANNELS = {
    "general": 9876543210987654321,
    "bybit": 8765432109876543210,
    "gate": 7654321098765432109,
    "mexc": 6543210987654321098,
    "xt": 5432109876543210987,
    "cmd": 4321098765432109876
}

ID = {
    "server": 3210987654321098765,
    "channel": CHANNELS["cmd"],
    "user": 2109876543210987654
}


def create_client():
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    intents.message_content = True
    client = discord.Client(intents=intents)
    return client


def connect():
    client.run(DISCORD_TOKEN)


async def message(client, message, channel="general"):
    channel_id = CHANNELS.get(channel)
    if not channel_id:
        print(f"Channel '{channel}' not found.")
        return

    channel = client.get_channel(channel_id)
    if channel:
        await channel.send(message)
        print(f"{channel}: {message}")
    else:
        print(f"Could not find the channel with ID: {channel_id}")


async def purge_channel(client, channel="general"):
    channel_id = CHANNELS.get(channel)
    channel = client.get_channel(channel_id)

    if channel:
        await channel.purge(limit=None)
        print(f"Purged all messages in {channel}.")
    else:
        print(f"Could not find the channel with ID: {channel_id}")


async def purge_all(client):
    for channel, _ in CHANNELS.items():
        await purge_channel(client, channel)


### discord events ###

client = create_client()
on_command = None


@client.event
async def on_ready():
    if on_command:
        await message(client,f"Connected ({socket.gethostname()})")


@client.event
async def on_message(message):
    if message.guild and message.guild.id == ID["server"]:
        if message.channel.id == ID["channel"] and message.author.id == ID["user"]:
            if on_command:
                await on_command(client, message.content)
