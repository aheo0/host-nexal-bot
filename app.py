import discord, os

import commands

try:
    with open("bot_token.txt") as f:
        DISCORD_TOKEN = f.read()
except:
    DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

client = discord.Client()

@client.event
async def on_ready():
    print("Ready!")

@client.event
async def on_message(message):
    if (message.content[:7] == ".nexal "):
        message_keys = message.content.split(" ")[1:]
        await commands.Main(message, message_keys).run()

client.run(DISCORD_TOKEN)