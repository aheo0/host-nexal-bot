from command import *

class Ping(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        await self.message.channel.send("Pong!")

class Help(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Lists possible commands"

    async def run(self):
        if (len(self.message_keys) == 0):
            help_messages = {
                "MAIN": {
                    "help": "Lists possible commands",
                    "ping": "Replies pong! Can be used to check if bot is online"
                },
                "[*] CONFIG": {
                    "setup": "Setups up bot in the server",
                    "delete-data": "Wipes all data the bot has on this server",
                    "prefix": "Modifies or lists the prefix list",
                    "admin": "Modifies or lists the nexal admins list",
                    "bcs": "Modifies or lists the bot command channels list",
                    "vcs": "Modifies or lists the raiding voice channels list",
                    "rsa": "Modifies or shows the rsa channel. ie. .nexal_rsa_set_1234567890 to change the rsa channel to the one with ID 123456789",
                    "vet-rsa": "Same as .nexal_rsa but for veteran runs",
                    "event-rsa": "Same as .nexal_rsa but for event runs"
                },
                "[*] CONFIG 2": {
                    "lng": "Modifies or shows the AFK voice channel. ie. .nexal_lng_set_1234567890 to change the rsa channel to the one with ID 123456789. Set ID to 0 to just disconnect raiders. For servers without an AFK channel, this can just be Lounge if it exists",
                    "vet-lng": "Same as .nexal_lng but for veteran runs",
                    "event-lng": "Same as .nexal_lng but for event runs",
                    "role": "Modifies or shows the name of the verified role. ie. .nexal_role_set_Verified_Raider if the name of the role with general permissions is \"Verified Raider\"",
                    "type": "Sets the default type of afk checks. A cultist hideout headcount can then be started with .nexal_hc rather than .nexal_hc_c ie. .nexal_type_set_c Type .nexal_type_-h to see all possible afk check types",
                },
                "AFK-CHECK": {
                    "hc": "Starts up an headcount. ie. .nexal_hc or .nexal_c_hc for a cultist hideout headcount. Type .nexal_hc_-h to see the different HC/AFKs you can start",
                    "afk": "Starts up an AFK check. ie. .nexal_afk_1_AustraliaSouthEast_Down",
                    "endafk": "Ends AFK. ie. .nexal_endafk_1",
                    "abortafk": "Aborts AFK. ie. .nexal_abortafk_1",
                    "logkeys": "Logs keys",
                    "runlogs": "Logs runs"
                },
                "PARSE": {
                    "parse": "Parses raiders for requirements. ie. .nexal_parse_1 and add a screenshot of the /who command with a black background. You can also list the raiders after the command separated by either a comma, period, space, or a newline ie. .nexal_parse_1_MeApollo_nexal",
                    "auto-parse": "Turns on or off the bot's auto-parsing feature of the vc for requirements which will activate \"auto-time\" amount of seconds after afk has ended. ie. .nexal_auto-parse_on",
                    "auto-time": "Amount of seconds to wait before bot auto-parses, if auto-parsing is turned on. ie. .nexal_auto-time_set_30",
                    "parselist": "Lists everyone currently in the voice channel. This can be used to track down alts of crashers/draggers in vc. ie. .nexal_parselist_1"
                },
                "MISCELLANEOUS": {
                    "deathcount": "Tracks staff kills in runs. A fun way to see how many times one staff has killed another"
                }

            }
            title = "Nexal Commands"
            description = "Note: all commands must start with `.nexal` \
For further information on individual commands, type -h after the command, i.e. `.nexal help -h`. \
In each code block example, *replace underscores (_) with spaces ( )*. \
Only nexal admins may run commands with **[*]**."
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
            title = "Info on command `help`"
            description = "Lists possible commands"
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
            return
            

