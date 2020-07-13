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

class Hc(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Starts up an HC"

    async def run(self):
        if (len(self.message_keys) == 0):
            title = "HC has been started"
            description = "React to <:ThicketPortal:578181776095051788> if you want to participate and react to <:ThicketKey:578181852154691594> if you are willing to pop. If you are planning to bring melees or a priest, react to the according icons."
            sent = await self.message.guild.get_channel(rsa).send("@here", embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
            await addReactions(sent, "afk")

            return
        if (self.message_keys[0] == "-h"):
            help_messages = {
                "help": self.help_text
            }
            title = "Info on command `hc`"
            description = ""
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description, "fields": fields}))
            return

class Afk(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Starts up an AFK"

    async def run(self):
        if (self.message_keys[0] != "-h"):
            with open("info.json") as f:
                data = json.load(f)
            afks = data["afk"]
            if (self.message_keys[0] in afks):
                await self.message.channel.send(self.message.author.mention + " AFK in Raiding " + self.message_keys[0] + " already exists.")
                return
            afks[self.message_keys[0]] = {"location": " ".join(self.message_keys[1:]), "raid-leader": self.message.author.id, "status": "afk", "keys": 0}
            title = "AFK Check in Raiding " + self.message_keys[0] + " has started"
            description = "React to <:ThicketPortal:578181776095051788> and join the respective voice channel to join the run and react to <:ThicketKey:578181852154691594> if you are willing to pop. If you are planning to bring melees or a priest, react to the according icons."
            sent = await self.message.guild.get_channel(rsa).send("@here", embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
            await addReactions(sent, "afk")
            afks[self.message_keys[0]]["id"] = sent.id

            await chagneVCPerms(self.message.guild, self.message_keys[0], True)

            data["afk"] = afks
            with open("info.json", "w") as f:
                json.dump(data, f)
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

class Endafk(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Ends AFK"

    async def run(self):
        if (self.message_keys[0] != "-h"):
            with open("info.json") as f:
                data = json.load(f)
            afks = data["afk"]
            if (self.message_keys[0] not in afks):
                await self.message.channel.send(self.message.author.mention + " Run in Raiding " + self.message_keys[0] + " has not started yet.")
                return
            if (afks[self.message_keys[0]]["status"] != "afk"):
                await self.message.channel.send(self.message.author.mention + " AFK in Raiding " + self.message_keys[0] + "has already ended!")
                return
            afks[self.message_keys[0]]["status"] = "endafk"

            data["afk"] = afks
            with open("info.json", "w") as f:
                json.dump(data, f)

            await chagneVCPerms(self.message.guild, self.message_keys[0], False)

            sent = await self.message.guild.get_channel(rsa).fetch_message(afks[self.message_keys[0]]["id"])
            title = "AFK Check in Raiding " + self.message_keys[0] + " has ended"
            description = "Join Lounge and ask an RL to drag you in."
            await sent.edit(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
            
            await self.message.channel.send("AFK has ended!")

            # Kick people out
            for i in sent.reactions:
                if str(i.emoji) == "<:ThicketPortal:578181776095051788>":
                    portal_icon = i
            reacted_users = await portal_icon.users().flatten()
            reacted_igns = [i.nick for i in reacted_users]
            print(reacted_igns)
            for i in self.message.guild.get_channel(afk_vcs[int(self.message_keys[0])-1]).members:
                if i.nick not in reacted_igns:
                    print(i.nick)
                    await i.edit(voice_channel=self.message.guild.get_channel(afk_vcs[-1]))


            return
        if (len(self.message_keys) > 0 and self.message_keys[0] == "-h"):
            help_messages = {
                "help": self.help_text
            }
            title = "Info on command `endrun`"
            description = ""
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description, "fields": fields}))
            return

class Endrun(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Ends runs"

    async def run(self):
        if (self.message_keys[0] != "-h"):
            with open("info.json") as f:
                data = json.load(f)
            afks = data["afk"]
            if (self.message_keys[0] not in afks):
                await self.message.channel.send(self.message.author.mention + " Run in Raiding " + self.message_keys[0] + " has not started yet.")
                return
            if (afks[self.message_keys[0]]["status"] == "afk"):
                await self.message.channel.send(self.message.author.mention + " End the AFK check first in Raiding " + self.message_keys[0] + "!")
                return
            sent = await self.message.guild.get_channel(rsa).fetch_message(afks[self.message_keys[0]]["id"])
            title = "Run in Raiding " + self.message_keys[0] + " has ended"
            description = ""
            await sent.edit(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
            if (self.message_keys[1] == "s"):
                if (str(afks[self.message_keys[0]]["raid-leader"]) in data["runs"]):
                    data["runs"][str(afks[self.message_keys[0]]["raid-leader"])] += 1
                else:
                    data["runs"][str(afks[self.message_keys[0]]["raid-leader"])] = 1
            afks.pop(self.message_keys[0])
            await self.message.channel.send("Run has ended!")

            data["afk"] = afks
            print(data)
            with open("info.json", "w") as f:
                json.dump(data, f)
            return
        if (self.message_keys[0] == "-h"):
            help_messages = {
                "help": self.help_text
            }
            title = "Info on command `endrun`"
            description = "Ends run"
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description, "fields": fields}))
            return

class KeyReact:
    def __init__(self, reaction, user):
        self.reaction = reaction
        self.user = user
    async def run(self):
        reaction, user = self.reaction, self.user
        if (reaction.message.author.id == 727405649633214545 and reaction.message.author.id != user.id and len(reaction.message.embeds) > 0 and reaction.message.embeds[0].title[:3] == "AFK"):
            if (str(reaction.emoji) == "<:ThicketKey:578181852154691594>"):
                vc = " ".join(reaction.message.embeds[0].title.split(" ")[4:-2])
                with open("info.json") as f:
                    data = json.load(f)
                if (user.dm_channel is None):
                    await user.create_dm()
                if (vc in data["afk"] and data["afk"][vc]["keys"] < 3):
                    data["afk"][vc]["keys"] += 1
                    if (data["afk"][vc]["keys"] == 1):
                        await user.dm_channel.send("Thank you for reacting to the key. Your location is " + data["afk"][vc]["location"] + ". You are the main key.")
                        await reaction.message.guild.get_channel(cmd_c).send(user.mention + " has reacted with a key and is main key!")
                    else:
                        await user.dm_channel.send("Thank you for reacting to the key. Your location is " + data["afk"][vc]["location"] + ". You are the backup key.")
                        await reaction.message.guild.get_channel(cmd_c).send(user.mention + " has reacted with a key and is backup key!")
                else:
                    await user.dm_channel.send("Thank you for reacting to the key. However, we already have 3 key reacts at the moment or the afk check is already over.")
                    await reaction.message.guild.get_channel(cmd_c).send(user.mention + " has reacted with a key but we already have 3 key reacts!")

                with open("info.json", "w") as f:
                    json.dump(data, f)
                return
            if (str(reaction.emoji) == "<:revolving_hearts:>"):
                perm = False
                pass


