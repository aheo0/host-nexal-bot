import discord, os, json

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
    with open("data/guilds.json") as f:
        data = json.load(f)
    prefix = [".nexal "]
    if (str(message.guild.id) in data):
        for i in data[str(message.guild.id)]["prefix"]:
            prefix.append(i)
    PREFIX_TRUE = False
    for i in prefix:
        if (message.content[:len(i)] == i):
            PREFIX_TRUE = True
            PREFIX_LEN = len(i)
            break
    if PREFIX_TRUE:
        message_keys = message.content[PREFIX_LEN:].split(" ")
        await commands.Main(message, message_keys).run()

@client.event
async def on_reaction_add(reaction, user):
    await commands.Main().reaction(reaction, user)

client.run(DISCORD_TOKEN)