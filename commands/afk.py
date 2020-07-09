from command import *

afks = {}
runs = {}

async def addReactions(message, type):
    await message.add_reaction(message.guild.fetch_emoji(730415225815433238))
    await message.add_reaction(message.guild.fetch_emoji(730415225815433238))
    pass

class Afk(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Starts up an AFK"

    async def run(self):
        if (len(self.message_keys) > 0):
            if (message_keys[0] in afks):
                await self.message.channel.send(message.author.mention + " AFK in Raiding " + message_keys[keys[0]] + " already exists.")
                return
            afks[message_keys[0]] = {"location": message_keys[1:], "raid-leader": message.author}
            title = "AFK Check in Raiding " + message_keys[keys[0]] + " has started"
            description = "React to :Secluded_Thicket: and join the respective voice channel to join the run and react to :SecludedThicketKey: if you are willing to pop."
            await self.message.channel.send("@here", embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
            return
        if (self.message_keys[0] == "-h"):
            help_messages = {
                "help": self.help_text
            }
            title = "Info on command `afk`"
            description = ""
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description, "fields": fields}))
            return
            
