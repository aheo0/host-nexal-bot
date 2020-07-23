import discord, os, json, pyrebase, asyncio

import commands

loop = asyncio.get_event_loop()

@commands.client.event
async def on_ready():
    print("Ready!")
    if False:
        title = "Verify for Veteran Cult Runs"
        description = "The long awaited veteran cultist hideout runs have finally arrived in the realm of Cults Only. Steps for verification are listed below"
        fields = [{
            "name": "Requirements",
            "value": "<:cultist:715219618876227674> **50 Cultist Hideout completitions**\n<:brain:715219618842542182> Visible Realmeye Graveyard",
            "inline": False
        }]
        fields.append({
            "name": "Visible Realmeye",
            "value": "Log into your `realmeye account` and under `Settings` scroll down to the `Who can see my graveyard?` and set it to `Everyone`",
            "inline": False
        })
        fields.append({
            "name": "To Finish...",
            "value": "React to ✅ to finish the verification process via a DM from the bot",
            "inline": False
        })
        fields.append({
            "name": "If You're Leaving...",
            "value": "React to ❌ to discontinue your veteran raiding experience",
            "inline": False
        })

        sent = await commands.client.get_channel(732946226571640852).send("@here", embed=commands.create_embed(type_="DM", fields={"title": title, "description": description, "fields": fields}))
        await sent.add_reaction("✅")
        await sent.add_reaction("❌")
        print(sent.id)


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
    else:
        if (message.content[:7] == ".nexal "):
            message_keys = message.content[7:].split(" ")
            await commands.Main(message, message_keys).dms()
    if (message.channel.id == 733163168960086117):
        active_commands = commands.pyc.get_item(["cults-only", "feedback", "commands"])
        if active_commands is not None:
            for i in active_commands:
                if (active_commands[i]["status"] == "comments"):
                    await commands.trl_feedback.TrlFeedback().post_message(i, message.content)
                    break

@commands.client.event
async def on_reaction_add(reaction, user):
    await commands.Main().reaction(reaction, user)

@commands.client.event
async def on_raw_reaction_add(payload):
    await commands.Main().raw_reaction(payload)

commands.client.run(commands.DISCORD_TOKEN)