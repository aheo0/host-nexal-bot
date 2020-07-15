import discord, os, json, pyrebase, asyncio

import commands

loop = asyncio.get_event_loop()

@commands.client.event
async def on_ready():
    print("Ready!")


@commands.client.event
async def on_message(message):
    if (message.guild is not None):
        prefix = [".nexal "]
        if commands.pyc.search(str(message.guild.id), []):
            for i in commands.pyc.get_item([str(message.guild.id), "prefix"], []):
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

@commands.client.event
async def on_reaction_add(reaction, user):
    await commands.Main().reaction(reaction, user)

commands.client.run(commands.DISCORD_TOKEN)