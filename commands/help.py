from command import *

class Help(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Lists possible commands"

    async def run(self):
        if (len(self.message_keys) == 0):
            help_messages = {
                "help": "Lists possible commands",
                "afk": "Starts up an AFK"
            }
            title = "nexal Commands"
            description = "Note: all commands must start with `.nexal` For further information on individual commands, type -h after the command, i.e. `.nexal help -h`"
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description, "fields": fields}))
            return
        if (self.message_keys[0] == "-h"):
            help_messages = {
                "help": self.help_text
            }
            title = "Info on command `help`"
            description = ""
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description, "fields": fields}))
            return
            
