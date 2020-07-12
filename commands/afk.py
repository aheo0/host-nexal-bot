from command import *
import json



class Type(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            with open("data/guilds.json") as f:
                data = json.load(f)
            TYPE = data[str(self.message.guild.id)]["type"]
            if (self.message_keys[0] == "set"):
                if (len(self.message_keys) > 1):
                    if (self.message_keys[1] != "-h"):
                        if not vars.check_nexal_admin(self.message.guild.id, self.message.author.id):
                            await vars.not_nexal_admin_speech(self.message.channel, self.message.author)
                            return
                        temp = self.message_keys[1]
                        if (temp not in ["c", "v", "st"]):
                            title = "Type Error"
                            description = "No type exists with those acronyms. Type `.nexal type -h` to learn how to set an AFK type in this server"
                            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                            return                   
                        data[str(self.message.guild.id)]["type"] = temp
                        with open("data/guilds.json", "w") as f:
                            json.dump(data, f)
                        
                        title = "The default AFK type has been set to `" + {"c": "Cultist Hideout", "v": "Void", "st": "Secluded Thicket"}[temp] + "`"
                        await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title}))
                        return
                    else:
                        title = "Info on command `type set`"
                        description = "Sets the default type of AFKs. After the command type in the following characters for the respective types: (c) for Cult, (v) for Void, (st) for Secluded Thicket. ie. `.nexal type set c`"
                        await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                        return
                else:
                    title = "No Channel ID Entered"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                    return
            if (self.message_keys[0] == "list"):
                if (len(self.message_keys) == 1):
                    if (TYPE == ""):
                        title = "No types are currently set"
                        description = "Type `.nexal type -h` to learn how to set an AFK type in this server"
                        await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description":description}))
                        return
                    title = "Current AFK Type"
                    description = "`" + {"c": "Cultist Hideout", "v": "Void", "st": "Secluded Thicket"}[TYPE] + "`"
                    await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description":description}))
                    return
                if (len(self.message_keys) > 0 and self.message_keys[1] == "-h"):
                    title = "Info on command `type list`"
                    description = "Displays the default type of AFKs. ie. `.nexal type list`"
                    await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
                    return

        if (self.message_keys[0] == "-h"):
            help_messages = {
                "COMMANDS": {
                    "set": "Sets the default type of AFKs. After the command type in the following characters for the respective types: (c) for Cult, (v) for Void, (st) for Secluded Thicket. ie. .nexal_type_set_c",
                    "list": "Displays the default type of AFKs. ie. .nexal_type_list"
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

