from command import *

class Help(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Lists possible commands"

    async def run(self):
        if (len(self.message_keys) == 0):
            help_messages = {
                "HELP": {
                    "help": "Lists possible commands"
                },
                "[*] CONFIG": {
                    "setup": "Setups up bot in the server",
                    "delete-data": "Wipes all data the bot has on this server",
                    "prefix": "Modifies or lists the prefix list",
                    "admins": "Modifies or lists the nexal admins list",
                    "bcs": "Modifies or lists the bot command channels list",
                    "vcs": "Modifies or lists the raiding voice channels list",
                    "rsa": "Modifies or shows the rsa channel. ie. .nexal_rsa_1234567890 to change the rsa channel to the one with ID 123456789",
                    "lng": "Modifies or shows the AFK voice channel. ie. .nexal_lng_1234567890 to change the rsa channel to the one with ID 123456789. Set ID to 0 to just disconnect raiders. For servers without an AFK channel, this can just be Lounge if it exists",

                },
                "AFK-CHECK": {
                    "type": "[*] Sets the default type of afk checks. A cult headcount can then be started with .nexal_hc rather than .nexal_hc_c ie. nexal_type_set_c",
                    "hc": "Starts up an HC. ie. .nexal_hc",
                    "afk": "Starts up an AFK. ie. .nexal_afk_1_AustraliaSouthEast_Down Do .nexal_afk_-h for more specific commands.",
                    "endafk": "Ends AFK. ie. .nexal_endafk_1",
                    "endrun": "Ends run. ie. .nexal_endrun_1_s or .nexal_endrun_1_f",
                },
                "PARSE": {
                    "parse": "Parses raiders for requirements. ie. .nexal_parse_1 and add a screenshot of the /who command with a black background",
                    "auto-parse": "Turns on or off the bot's auto-parsing feature of the vc for requirements which will activate \"auto-time\" amount of seconds after afk has ended. ie. .nexal_auto-parse_on",
                    "auto-time": "Amount of seconds to wait before bot auto-parses, if auto-parsing is turned on. ie. .nexal_auto-time_set_30"
                }

            }
            title = "Nexal Commands"
            description = "Note: all commands must start with `.nexal` \
For further information on individual commands, type -h after the command, i.e. `.nexal help -h`. \
In each code block example, *replace underscores (_) with spaces ( )*. \
Only nexal admins may run commands with **[*]**. \
Commands with [/] afterwards have more arguments to the command that are further explained in their respective help menus."
            fields = []
            for i in help_messages:
                name = i
                inline = False
                value = "```css\n"
                for j in help_messages[i]:
                    value += "[" + j + "] " + help_messages[i][j] + "\n"
                value += "```"
                fields.append({"name": name, "value": value, "inline": inline})
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
            
