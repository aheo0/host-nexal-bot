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
                add_data = {
                    "admins": [self.message.author.id],
                    "bcs": [self.message.channel.id]
                }
                vars.db.child(str(self.message.guild.id)).set(add_data)
                
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
        if not pyc.search(str(self.message.guild.id), []):
            if say:
                title = "The nexal bot has not been setup yet!"
                description = "Type `.nexal setup` to start setting up the nexal bot for this server."
                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            return False
        else:
            return True

    async def delete_data(self):
        if (len(self.message_keys) == 0):
            if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                return
            
            vars.db.child(str(self.message.guild.id)).remove()
            
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
            PREFIXES = pyc.get_item([str(self.message.guild.id), "prefix"], [])
            if (self.message_keys[0] == "add"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = " ".join(self.message_keys[1:])
                        if temp not in PREFIXES:
                            pyc.child([str(self.message.guild.id), "prefix"]).set(PREFIXES + [temp])
                            
                            title = "Prefix `" + temp + "` has been successfully added"
                            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title}))
                            return
                        else:
                            title = "Prefix `" + temp + "` already exists"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                            return
                    else:
                        title = "Info on command `prefix add`"
                        description = "Adds a prefix. ie. `.nexal prefix add ;`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Prefix Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "del"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = " ".join(self.message_keys[1:])
                        if temp in PREFIXES:
                            PREFIXES.remove(temp)
                            pyc.child([str(self.message.guild.id), "prefix"]).set(PREFIXES)
                            
                            title = "Prefix `" + temp + "` has been successfully deleted"
                            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title}))
                            return
                        else:
                            title = "Prefix `" + temp + "` does not exist"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                            return
                    else:
                        title = "Info on command `prefix del`"
                        description = "Deletes a prefix. ie. `.nexal prefix del ;`"
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
                    await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description":description}))
                    return
                if (len(self.message_keys) > 0 and self.message_keys[1] == "-h"):
                    title = "Info on command `prefix list`"
                    description = "Lists all available prefixes besides the built-in prefix .nexal ie. `.nexal prefix list`"
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

class Admin(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            ADMINS = pyc.get_item([str(self.message.guild.id), "admins"], [])
            if (self.message_keys[0] == "add"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = self.message_keys[1]
                        try:
                            temp = int(temp)
                        except:
                            title = "User ID Error"
                            description = "No user with this ID exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        if temp not in ADMINS:
                            if (self.message.guild.get_member(temp) is None):
                                title = "User ID Error"
                                description = "No user with this ID exists in this server"
                                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                                return
                            pyc.child([str(self.message.guild.id), "admins"]).set(ADMINS + [temp])
                            
                            title = "New nexal admin " + self.message.guild.get_member(temp).mention + " has been successfully added"
                            description = self.message.guild.get_member(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
                            return
                        else:
                            title = "Nexal admin " + self.message.guild.get_member(temp).mention + " already exists"
                            description = self.message.guild.get_member(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                    else:
                        title = "Info on command `admin add`"
                        description = "Adds a new nexal admin. Enter the ID of the user after the command. ie. `.nexal admin add 1234567890`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No User ID Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "del"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = self.message_keys[1]
                        try:
                            temp = int(temp)
                        except:
                            title = "User ID Error"
                            description = "No user with this ID exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        if temp in ADMINS:
                            if (self.message.guild.get_member(temp) is None):
                                title = "User ID Error"
                                description = "No user with this ID exists in this server"
                                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                                return
                            ADMINS.remove(temp)
                            pyc.child([str(self.message.guild.id), "admins"]).set(ADMINS)
                            
                            title = "Nexal admin " + self.message.guild.get_member(temp).mention + " has been successfully deleted"
                            description = self.message.guild.get_member(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
                            return
                        else:
                            title = "Nexal admin " + self.message.guild.get_member(temp).mention + " does not exist"
                            description = self.message.guild.get_member(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                    else:
                        title = "Info on command `admin del`"
                        description = "Deletes a nexal admin. Enter the ID of the user after the command. ie. `.nexal admin del 1234567890`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No User ID Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "list"):
                if (len(self.message_keys) == 1):
                    title = "Available Admins"
                    description = ""
                    for i in ADMINS:
                        description += self.message.guild.get_member(i).mention + " "
                    await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description":description}))
                    return
                if (len(self.message_keys) > 0 and self.message_keys[1] == "-h"):
                    title = "Info on command `admin list`"
                    description = "Lists all nexal admins in this server. ie. `.nexal admin list`"
                    await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                    return

        if (self.message_keys[0] == "-h"):
            help_messages = {
                "COMMANDS": {
                    "add": "Adds a new nexal admin. Enter the ID of the user after the command. ie. .nexal_admin_add_1234567890",
                    "del": "Deletes a nexal admin. Enter the ID of the user after the command. ie. .nexal_admin_del_1234567890",
                    "list": "Lists all nexal admins in this server. ie. .nexal_admin_list"
                }
            }
            title = "Info on command `admin`"
            description = "Modifies or lists the nexal admins in this server"
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

class BCS(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            BCS = pyc.get_item([str(self.message.guild.id), "bcs"], [])
            if (self.message_keys[0] == "add"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = self.message_keys[1]
                        try:
                            temp = int(temp)
                        except:
                            title = "Channel ID Error"
                            description = "No channel with this ID exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        if temp not in BCS:
                            if (self.message.guild.get_channel(temp) is None):
                                title = "Channel ID Error"
                                description = "No channel with this ID exists in this server"
                                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                                return
                            pyc.child([str(self.message.guild.id), "bcs"]).set(BCS + [temp])
                            
                            title = "New bot command channel " + self.message.guild.get_channel(temp).mention + " has been successfully added"
                            description = self.message.guild.get_channel(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
                            return
                        else:
                            title = "Bot command channel " + self.message.guild.get_channel(temp).mention + " already exists"
                            description = self.message.guild.get_channel(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                    else:
                        title = "Info on command `bcs add`"
                        description = "Adds a new bot command channel. Enter the ID of the text channel after the command. ie. `.nexal bcs add 1234567890`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Channel ID Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "del"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = self.message_keys[1]
                        try:
                            temp = int(temp)
                        except:
                            title = "Channel ID Error"
                            description = "No channel with this ID exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        if temp in BCS:
                            if (self.message.guild.get_channel(temp) is None):
                                title = "Channel ID Error"
                                description = "No channel with this ID exists in this server"
                                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                                return
                            BCS.remove(temp)
                            pyc.child([str(self.message.guild.id), "bcs"]).set(BCS)
                            
                            title = "Bot command channel " + self.message.guild.get_channel(temp).mention + " has been successfully deleted"
                            description = self.message.guild.get_channel(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
                            return
                        else:
                            title = self.message.guild.get_channel(temp).mention + " is not a bot command channel"
                            description = self.message.guild.get_channel(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                    else:
                        title = "Info on command `bcs del`"
                        description = "Deletes a bot command channel. Enter the ID of the text channel after the command. ie. `.nexal bcs del 1234567890`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Channel ID Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "list"):
                if (len(self.message_keys) == 1):
                    title = "Available Bot Command Channels"
                    description = ""
                    for i in BCS:
                        description += self.message.guild.get_channel(i).mention + " "
                    await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description":description}))
                    return
                if (len(self.message_keys) > 0 and self.message_keys[1] == "-h"):
                    title = "Info on command `bcs list`"
                    description = "Lists all bot command channels. ie. .nexal bcs list"
                    await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                    return

        if (self.message_keys[0] == "-h"):
            help_messages = {
                "COMMANDS": {
                    "add": "Adds a new bot command channel. Enter the ID of the text channel after the command. ie. .nexal_bcs_add_1234567890",
                    "del": "Deletes a bot command channel. Enter the ID of the text channel after the command. ie. .nexal_bcs_del_1234567890",
                    "list": "Lists all bot command channels. ie. .nexal_bcs_list"
                }
            }
            title = "Info on command `bcs`"
            description = "Modifies or lists the bot command channels"
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

class VCS(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            VCS = pyc.get_item([str(self.message.guild.id), "vcs"], [])
            if (self.message_keys[0] == "add"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = self.message_keys[1]
                        try:
                            temp = int(temp)
                        except:
                            title = "Channel ID Error"
                            description = "No channel with this ID exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        if temp not in VCS:
                            if (self.message.guild.get_channel(temp) is None):
                                title = "Channel ID Error"
                                description = "No channel with this ID exists in this server"
                                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                                return
                            if (str(self.message.guild.get_channel(temp).type) != "voice"):
                                title = "Channel ID Error"
                                description = "This channel is not a voice channel"
                                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                                return
                            pyc.child([str(self.message.guild.id), "vcs"]).set(VCS + [temp])
                            
                            title = "New raiding voice channel " + self.message.guild.get_channel(temp).mention + " has been successfully added"
                            description = self.message.guild.get_channel(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
                            return
                        else:
                            title = "Raiding voice channel " + self.message.guild.get_channel(temp).mention + " already exists"
                            description = self.message.guild.get_channel(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                    else:
                        title = "Info on command `vcs add`"
                        description = "Adds a new raiding voice channel. Enter the ID of the voice channel after the command. ie. `.nexal vcs add 1234567890`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Channel ID Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "del"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = self.message_keys[1]
                        try:
                            temp = int(temp)
                        except:
                            title = "Channel ID Error"
                            description = "No channel with this ID exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        if temp in VCS:
                            if (self.message.guild.get_channel(temp) is None):
                                title = "Channel ID Error"
                                description = "No channel with this ID exists in this server"
                                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                                return
                            VCS.remove(temp)
                            pyc.child([str(self.message.guild.id), "vcs"]).set(VCS)
                            
                            title = "Raiding voice channel " + self.message.guild.get_channel(temp).mention + " has been successfully deleted"
                            description = self.message.guild.get_channel(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
                            return
                        else:
                            title = self.message.guild.get_channel(temp).mention + " is not a raiding voice channel"
                            description = self.message.guild.get_channel(temp).mention
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                    else:
                        title = "Info on command `vcs del`"
                        description = "Deletes a raiding voice channel. Enter the ID of the voice channel after the command. ie. `.nexal vcs del 1234567890`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Channel ID Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "list"):
                if (len(self.message_keys) == 1):
                    title = "Available Raiding Voice Channels"
                    description = ""
                    for i in VCS:
                        description += self.message.guild.get_channel(i).mention + " "
                    await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description":description}))
                    return
                if (len(self.message_keys) > 0 and self.message_keys[1] == "-h"):
                    title = "Info on command `vcs list`"
                    description = "Lists all raiding voice channels. ie. `.nexal vcs list`"
                    await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                    return

        if (self.message_keys[0] == "-h"):
            help_messages = {
                "COMMANDS": {
                    "add": "Adds a new raiding voice channel. Enter the ID of the voice channel after the command. ie. .nexal_vcs_add_1234567890",
                    "del": "Deletes a raiding voice channel. Enter the ID of the voice channel after the command. ie. .nexal_vcs_del_1234567890",
                    "list": "Lists all raiding voice channels. ie. .nexal_vcs_list"
                }
            }
            title = "Info on command `vcs`"
            description = "Modifies or lists the raiding voice channels"
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

class RSA(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            RSA = pyc.get_item([str(self.message.guild.id), "rsa"], 0)
            if (self.message_keys[0] == "set"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = self.message_keys[1]
                        try:
                            temp = int(temp)
                        except:
                            title = "Channel ID Error"
                            description = "No channel with this ID exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        if (self.message.guild.get_channel(temp) is None):
                            title = "Channel ID Error"
                            description = "No channel with this ID exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        if (str(self.message.guild.get_channel(temp).type) != "text"):
                            title = "Channel ID Error"
                            description = "This channel is not a text channel"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        pyc.child([str(self.message.guild.id), "rsa"]).set(temp)
                        
                        title = "Channel " + self.message.guild.get_channel(temp).mention + " has been successfully set as the raiding status announcements channel"
                        description = self.message.guild.get_channel(temp).mention
                        await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
                        return
                    else:
                        title = "Info on command `rsa set`"
                        description = "Sets the raiding status announcements text channel. Enter the ID of the text channel after the command. ie. `.nexal rsa set 1234567890`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Channel ID Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "list"):
                if (len(self.message_keys) == 1):
                    if (RSA == 0):
                        title = "No Raiding Status Announcement Channels are currently set"
                        description = "Type `.nexal rsa set 1234567890`, replacing 1234567890 with the text channel id to set one"
                        await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description":description}))
                        return
                    title = "Current Raiding Status Announcement Channel"
                    description = self.message.guild.get_channel(RSA).mention
                    await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description":description}))
                    return
                if (len(self.message_keys) > 0 and self.message_keys[1] == "-h"):
                    title = "Info on command `rsa list`"
                    description = "Displays the current raiding status announcements channel. ie. `.nexal rsa list`"
                    await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                    return

        if (self.message_keys[0] == "-h"):
            help_messages = {
                "COMMANDS": {
                    "set": "Sets the raiding status announcements text channel. Enter the ID of the text channel after the command. ie. .nexal_rsa_set_1234567890",
                    "list": "Displays the current raiding status announcements channel. ie. .nexal_rsa_list"
                }
            }
            title = "Info on command `rsa`"
            description = "Sets or displays the raiding status announcements channel"
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

class LNG(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            LNG = pyc.get_item([str(self.message.guild.id), "lounge"], [])
            if (self.message_keys[0] == "set"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = self.message_keys[1]
                        try:
                            temp = int(temp)
                        except:
                            title = "Channel ID Error"
                            description = "No channel with this ID exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        if (self.message.guild.get_channel(temp) is None):
                            title = "Channel ID Error"
                            description = "No channel with this ID exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        if (str(self.message.guild.get_channel(temp).type) != "voice"):
                            title = "Channel ID Error"
                            description = "This channel is not a voice channel"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        pyc.child([str(self.message.guild.id), "lounge"]).set(temp)
                        
                        title = "Channel " + self.message.guild.get_channel(temp).mention + " has been successfully set as the afk channel"
                        description = self.message.guild.get_channel(temp).mention
                        await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
                        return
                    else:
                        title = "Info on command `lng set`"
                        description = "Sets the afk voice channel. Enter the ID of the voice channel after the command. ie. `.nexal lng set 1234567890`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Channel ID Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "list"):
                if (len(self.message_keys) == 1):
                    if (LNG == 0):
                        title = "No AFK Channels are currently set"
                        description = "Type `.nexal lng set 1234567890`, replacing 1234567890 with the text channel id to set one"
                        await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description":description}))
                        return
                    title = "Current AFK Channel"
                    description = self.message.guild.get_channel(LNG).mention
                    await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description":description}))
                    return
                if (len(self.message_keys) > 0 and self.message_keys[1] == "-h"):
                    title = "Info on command `lng list`"
                    description = "Displays the current afk channel. ie. `.nexal lng list`"
                    await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                    return

        if (self.message_keys[0] == "-h"):
            help_messages = {
                "COMMANDS": {
                    "set": "Sets the afk voice channel. Enter the ID of the voice channel after the command. ie. .nexal_lng_set_1234567890",
                    "list": "Displays the current afk channel. ie. .nexal_lng_list"
                }
            }
            title = "Info on command `lng`"
            description = "Sets or displays the afk voice channel"
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

class Role(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            ROLE = pyc.get_item([str(self.message.guild.id), "reg-role"], "")
            if (self.message_keys[0] == "set"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not pyc.search_val(self.message.author.id, [str(self.message.guild.id), "admins"]):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = " ".join(self.message_keys[1:])
                        role_object = vars.get_role(self.message.guild, temp)
                        if (role_object is None):
                            title = "Role Name Error"
                            description = "No role with this name exists in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return
                        pyc.child([str(self.message.guild.id), "reg-role"]).set(temp)
                        
                        title = "Role `" + temp + "` has been successfully set as the regular raider role"
                        role_object = vars.get_role(self.message.guild, temp)
                        description = role_object.mention if role_object.mentionable else ""
                        await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
                        return
                    else:
                        title = "Info on command `role set`"
                        description = "Sets the name of the regular raider role. Enter the name of the role after the command. ie. `.nexal role set Verified Raider`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Channel ID Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "list"):
                if (len(self.message_keys) == 1):
                    if (ROLE == ""):
                        title = "No regular raider roles are currently set"
                        description = "Type `.nexal role set Verified Raider` if regular raiders have the role Verified Raider"
                        await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description":description}))
                        return
                    title = "Current Regular Raider Role"
                    role_object = vars.get_role(self.message.guild, ROLE)
                    description = role_object.mention if role_object.mentionable else ROLE
                    await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description":description}))
                    return
                if (len(self.message_keys) > 0 and self.message_keys[1] == "-h"):
                    title = "Info on command `role list`"
                    description = "Displays the current raider role. ie. `.nexal role list`"
                    await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                    return

        if (self.message_keys[0] == "-h"):
            help_messages = {
                "COMMANDS": {
                    "set": "Sets the name of the regular raider role. Enter the name of the role after the command. ie. .nexal_role_set_Verified_Raider",
                    "list": "Displays the current raider role. ie. .nexal_role_list"
                }
            }
            title = "Info on command `role`"
            description = "Sets or displays the regular raider role name"
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

