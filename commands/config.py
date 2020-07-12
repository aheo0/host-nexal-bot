from command import *
import json, os

class Setup(Command):
    def __init__(self, message=None, message_keys=None):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) == 0):
            IS_BOT_SETUP = await self.check(False)
            if IS_BOT_SETUP:
                title = "The nexal bot has already been setup in this server!"
                description = "If you wish to re-setup the server, first delete the server's data with the command `.nexal delete-data`."
                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            else:
                with open("data/guilds.json", "r") as f:
                    data = json.load(f)
                data[str(self.message.guild.id)] = {
                    "prefix": [],
                    "admins": [self.message.author.id],
                    "rsa": 0,
                    "bcs": [],
                    "vcs": [],
                    "lounge": 0,
                    "reg-role": "",
                    "type": ""
                }
                with open("data/guilds.json", "w") as f:
                    json.dump(data, f)

                dir_path = "data/" + str(self.message.guild.id)
                os.makedirs(dir_path)
                with open(dir_path + "/afks.json", "w") as f:
                    json.dump({}, f)
                with open(dir_path + "/run-logs.json", "w") as f:
                    json.dump({}, f)
                
                title = "Setup complete!"
                description = "Now add nexal admins, voice channels, and text channels for the bot commands!"
                await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
            return
        if (self.message_keys[0] == "-h"):
            title = "Info on command `setup`"
            description = "Setups up bot in the server"
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
            return

    async def check(self, say=True):
        with open("data/guilds.json") as f:
            data = json.load(f)

        if str(self.message.guild.id) not in data:
            if say:
                title = "The nexal bot has not been setup yet!"
                description = "Type `.nexal setup` to start setting up the nexal bot for this server."
                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            return False
        else:
            return True

    async def delete_data(self):
        if (len(self.message_keys) == 0):
            with open("data/guilds.json", "r") as f:
                data = json.load(f)
            data.pop(str(self.message.guild.id))
            with open("data/guilds.json", "w") as f:
                json.dump(data, f)

            dir_path = "data/" + str(self.message.guild.id)
            os.remove(dir_path + "/afks.json")
            os.remove(dir_path + "/run-logs.json")
            os.rmdir(dir_path)
            
            title = "Server data has been wiped!"
            description = "Type `.nexal setup` to re-setup the nexal bot for this server."
            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
            return
        if (self.message_keys[0] == "-h"):
            title = "Info on command `delete-data`"
            description = "Wipes all data the bot has on this server. \
This allows the user to re-setup the bot on the server if desired or can be used when the bot's usage in the server will be discontinued."
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
            return

class Prefix(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            with open("data/guilds.json") as f:
                data = json.load(f)
            PREFIXES = data[str(self.message.guild.id)]["prefix"]
            if (self.message_keys[0] == "add"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        temp = " ".join(self.message_keys[1:])
                        if temp not in PREFIXES:
                            data[str(self.message.guild.id)]["prefix"].append(temp)
                            with open("data/guilds.json", "w") as f:
                                json.dump(data, f)
                            
                            title = "Prefix `" + temp + "` has been successfully added"
                            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title}))
                            return
                        else:
                            title = "Prefix `" + temp + "` already exists"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                            return
                    else:
                        title = "Info on command `prefix add`"
                        description = "Adds a prefix. ie. `.nexal_prefix_add_;`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Prefix Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "del"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        temp = " ".join(self.message_keys[1:])
                        if temp in PREFIXES:
                            data[str(self.message.guild.id)]["prefix"].remove(temp)
                            with open("data/guilds.json", "w") as f:
                                json.dump(data, f)
                            
                            title = "Prefix `" + temp + "` has been successfully deleted"
                            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title}))
                            return
                        else:
                            title = "Prefix `" + temp + "` does not exist"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                            return
                    else:
                        title = "Info on command `prefix del`"
                        description = "Deletes a prefix. ie. `.nexal_prefix_del_;`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Prefix Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "list"):
                if (len(self.message_keys) == 1):
                    title = "Available Prefixes"
                    description = "```css\n[.nexal ]"
                    for i in PREFIXES:
                        description += " [" + i + "]"
                    description += "\n```"
                    await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description":description}))
                    return
                if (len(self.message_keys) > 0 and self.message_keys[1] == "-h"):
                    title = "Info on command `prefix list`"
                    description = "Lists all available prefixes besides the built-in prefix .nexal ie. `.nexal_prefix_list`"
                    await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                    return

        if (self.message_keys[0] == "-h"):
            help_messages = {
                "COMMANDS": {
                    "add": "Adds a prefix. ie. .nexal_prefix_add_;",
                    "del": "Deletes a prefix. ie. .nexal_prefix_del_;",
                    "list": "Lists all available prefixes besides the built-in prefix .nexal ie. .nexal_prefix_list"
                }
            }
            title = "Info on command `prefix`"
            description = "Modifies or lists the available prefixes in this server. Note: Prefixes may include spaces and special characters"
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
