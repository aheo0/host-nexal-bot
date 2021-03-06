from command import *
import json, pyrebase, asyncio, time


async def addReactions(message, mes_type, rea_type):
    with open("data/emojis.json") as f:
        data = json.load(f)
    data = data[mes_type]
    for i in data["essential"]:
        await message.add_reaction(i)
    for i in data[rea_type]:
        await message.add_reaction(i)

async def changeVCPerms(guild, channel_, open):
    channel = channel_
    overwrite_dict = {}
    role_name = pyc.get_item([str(guild.id), "reg-role"])
    for i in channel.overwrites:
        if (i.name == role_name):
            verified = i
        else:
            overwrite_dict[i] = channel.overwrites[i]
    a = channel.overwrites[verified]
    if (open):
        a.update(connect=True)
        overwrite_dict[verified] = a
        try:
            await channel.edit(overwrites=overwrite_dict)
        except:
            pass
    else:
        a.update(connect=False)
        overwrite_dict[verified] = a
        try:
            await channel.edit(overwrites=overwrite_dict)
        except:
            pass

class Hc(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) == 0 or self.message_keys[0] != "-h"):
            if (len(self.message_keys) > 0 and self.message_keys[0][0] == "-"):
                rea_type = self.message_keys[0][1:]
                if rea_type not in ["c", "v", "st", "vc", "o3"]:
                    title = "Invalid AFK Type"
                    description = "fancy [c] Cultist Hideout, etc printing for the different afk types"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            else:
                rea_type = pyc.get_item([str(self.message.guild.id), "type"])
                if rea_type is None:
                    title = "HC Command Error"
                    description = "In order to use this shortcut, an afk type must be set in this server. Type `.nexal type -h` to learn how to"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            if (rea_type != "e"):
                dung_name = {"c": "Cultist Hideout", "v": "Void", "st": "Secluded Thicket", "vc": "Veteran Cultist Hideout", "o3": "Oryx 3"}[rea_type]
            if (rea_type in ["vc"]):
                RSA = int(pyc.get_item([str(self.message.guild.id), "vet-rsa"]))
                if RSA is None:
                    title = "No Veteran RSA Defined"
                    description = "Type `.nexal vet-rsa set -h` to learn how to set a veteran raiding-status-announcments channel for afk checks"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            elif (rea_type == "e"):
                RSA = int(pyc.get_item([str(self.message.guild.id), "event-rsa"]))
                if RSA is None:
                    title = "No Event RSA Defined"
                    description = "Type `.nexal event-rsa set -h` to learn how to set a event-raiding-status-announcments channel for afk checks"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            else:
                RSA = int(pyc.get_item([str(self.message.guild.id), "rsa"]))
                if RSA is None:
                    title = "No RSA Defined"
                    description = "Type `.nexal rsa set -h` to learn how to set a raiding-status-announcments channel for afk checks"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            with open("data/emojis.json") as f:
                data = json.load(f)
            data = data[rea_type]

            title = "HC for `" + dung_name + "` has been started"
            description = "React to " + data["essential"][0] + " if you want to participate and react to " + data["essential"][1] + " if you are willing to pop. If you are planning to bring melees or a priest, react to the according icons."
            sent = await self.message.guild.get_channel(RSA).send("@here", embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))
            await sent.edit(content="")
            await addReactions(sent, rea_type, "hc")

            return
        if (self.message_keys[0] == "-h"):
            help_messages = {
                "help": "me"
            }
            title = "Info on command `hc`"
            description = "Starts up a hc. The different types of headcounts that can be started are listed below. After the command, type `-` and the afk type to start its respective headcount. ie. `.nexal hc -c` for a Cultist Hideout headcount"
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="BASIC", fields={"title": title, "description": description, "fields": fields}))
            return

class Afk(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Starts up an AFK"

    async def run(self):
        if (len(self.message_keys) == 0 or self.message_keys[0] != "-h"):
            if (len(self.message_keys) > 0 and self.message_keys[0][0] == "-"):
                rea_type = self.message_keys[0][1:]
                if rea_type not in ["c", "v", "st", "vc", "o3"]:
                    title = "Invalid AFK Type"
                    description = "fancy [c] Cultist Hideout, etc printing for the different afk types"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
                keyed = 1
            else:
                rea_type = pyc.get_item([str(self.message.guild.id), "type"])
                if rea_type is None:
                    title = "AFK Command Error"
                    description = "In order to use this shortcut, an afk type must be set in this server. Type `.nexal type -h` to learn how to"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
                keyed = 0
            if (len(self.message_keys) == keyed):
                title = "No VC Set"
                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title}))
                return

            db_path_name = self.message_keys[keyed]
            if (self.message_keys[keyed][0] == "v"):
                VCS = pyc.get_item([str(self.message.guild.id), "vet-vcs"])
                self.message_keys[keyed] = self.message_keys[keyed][1:]
            else:
                VCS = pyc.get_item([str(self.message.guild.id), "vcs"])


            if (VCS is None or (int(self.message_keys[keyed]) > len(VCS))):
                title = "No VC Set"
                description = "This VC has not been set yet"
                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                return
            VC = self.message.guild.get_channel(int(VCS[int(self.message_keys[keyed])-1]))
            loc = " ".join(self.message_keys[1+keyed:])

            if pyc.search("-" + self.message_keys[keyed], [str(self.message.guild.id), "afks"]):
                title = "AFK Already Set"
                description = "An AFK already started in this vc has not had its run end"
                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                return

            if (rea_type != "e"):
                dung_name = {"c": "Cultist Hideout", "v": "Void", "st": "Secluded Thicket", "vc": "Veteran Cultist Hideout", "o3": "Oryx 3"}[rea_type]
            if (rea_type in ["vc"]):
                RSA = int(pyc.get_item([str(self.message.guild.id), "vet-rsa"]))
                if RSA is None:
                    title = "No Veteran RSA Defined"
                    description = "Type `.nexal vet-rsa set -h` to learn how to set a veteran raiding-status-announcments channel for afk checks"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            elif (rea_type == "e"):
                RSA = int(pyc.get_item([str(self.message.guild.id), "event-rsa"]))
                if RSA is None:
                    title = "No Event RSA Defined"
                    description = "Type `.nexal event-rsa set -h` to learn how to set a event-raiding-status-announcments channel for afk checks"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            else:
                RSA = int(pyc.get_item([str(self.message.guild.id), "rsa"]))
                if RSA is None:
                    title = "No RSA Defined"
                    description = "Type `.nexal rsa set -h` to learn how to set a raiding-status-announcments channel for afk checks"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            with open("data/emojis.json") as f:
                data = json.load(f)
            data = data[rea_type]

            title = "AFK for `" + dung_name + "` has been started in `" + VC.name + "`"
            description = "React to " + data["essential"][0] + " and join the respective voice channel to join the run and react to " + data["essential"][1] + " if you are willing to pop. React to the according icons if you are bringing that specific class or ability."
            sent = await self.message.guild.get_channel(RSA).send("@here", embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))

            path = pyc.child([str(self.message.guild.id)])
            path.child("afks").child("-" + db_path_name).set({
                "location": loc,
                "raid-leader": str(self.message.author.id),
                "status": "afk",
                "type": rea_type,
                "id": str(sent.id)
            })

            await sent.edit(content="")
            await changeVCPerms(self.message.guild, VC, True)
            await addReactions(sent, rea_type, "afk")
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

class Abortafk(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Aborts AFK"

    async def run(self):
        if (len(self.message_keys) == 0 or self.message_keys[0] != "-h"):
            guild = self.message.guild
            guild_id = str(guild.id)
            afks = pyc.get_item([guild_id, "afks"], [])
            if (len(self.message_keys) == 0):
                if (len(afks) == 1):
                    for i in afks:
                        if i is not None:
                            vc = i
                            break
                else:
                    title = "Abort AFK Command Error"
                    description = "In order to use this shortcut, only one afk check must be up"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            else:
                vc = "-" + self.message_keys[0]
                if not pyc.search(vc, [guild_id, "afks"]):
                    title = "Abort AFK Command Error"
                    description = "Run in this channel has not started yet"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            if (vc[1] == "v"):
                VC = guild.get_channel(int(pyc.get_item([guild_id, "vet-vcs", str(int(vc[2:])-1)])))
            else:
                VC = guild.get_channel(int(pyc.get_item([guild_id, "vcs", str(int(vc[1:])-1)])))

            await changeVCPerms(guild, VC, False)

            if pyc.get_item([guild_id, "afks", vc, "type"]) in ["vc"]:
                RSA = int(pyc.get_item([guild_id, "vet-rsa"]))
                LNG = int(pyc.get_item([guild_id, "vet-lounge"]))
            else:
                RSA = int(pyc.get_item([guild_id, "rsa"]))
                LNG = int(pyc.get_item([guild_id, "lounge"]))

            sent = await guild.get_channel(RSA).fetch_message(int(pyc.get_item([guild_id, "afks", vc, "id"])))

            # Edit Message
            title = "AFK Check for `" + VC.name + "` has been aborted"
            description = "Wait for the next afk check to start"
            await sent.edit(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))

            # Kill AFK in Database
            pyc.child([guild_id, "afks", vc]).remove()

            return
        if (len(self.message_keys) > 0 and self.message_keys[0] == "-h"):
            help_messages = {
                "help": self.help_text
            }
            title = "Info on command `abortafk`"
            description = ""
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description, "fields": fields}))
            return

class Endafk(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Ends AFK"

    async def run(self):
        if (len(self.message_keys) == 0 or self.message_keys[0] != "-h"):
            guild = self.message.guild
            guild_id = str(guild.id)
            afks = pyc.get_item([guild_id, "afks"], [])
            if (len(self.message_keys) == 0):
                if (len(afks) == 1):
                    for i in afks:
                        if i is not None:
                            vc = i
                            break
                else:
                    title = "End AFK Command Error"
                    description = "In order to use this shortcut, only one afk check must be up. To start one, type `.nexal afk -c 1`"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            else:
                vc = "-" + self.message_keys[0]
                if not pyc.search(vc, [guild_id, "afks"]):
                    title = "End AFK Command Error"
                    description = "Run in this channel has not started yet. To start one, type `.nexal afk -c 1`"
                    await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                    return
            if (vc[1] == "v"):
                VC = guild.get_channel(int(pyc.get_item([guild_id, "vet-vcs", str(int(vc[2:])-1)])))
            else:
                VC = guild.get_channel(int(pyc.get_item([guild_id, "vcs", str(int(vc[1:])-1)])))
            if (pyc.get_item([guild_id, "afks", vc, "status"]) != "afk"):
                await self.message.channel.send(self.message.author.mention + " AFK in " + VC.name + " has already ended!")
                return

            await changeVCPerms(guild, VC, False)

            if pyc.get_item([guild_id, "afks", vc, "type"]) in ["vc"]:
                RSA = int(pyc.get_item([guild_id, "vet-rsa"]))
                LNG = int(pyc.get_item([guild_id, "vet-lounge"]))
            else:
                RSA = int(pyc.get_item([guild_id, "rsa"]))
                LNG = int(pyc.get_item([guild_id, "lounge"]))

            sent = await guild.get_channel(RSA).fetch_message(int(pyc.get_item([guild_id, "afks", vc, "id"])))
            portal_icon = sent.reactions[0]
            countdown = 15
            title = "AFK Check for `" + VC.name + "` has ended"
            description = "Join `" + guild.get_channel(LNG).name + "` and re-react to " + str(portal_icon.emoji) + " to get moved back in. You have " + str(countdown) + " seconds left until post-afk ends"
            sent_embed_description = sent.embeds[0].description
            if "\n" in sent_embed_description:
                description += "\n" + "\n".join(sent_embed_description.split("\n")[1:])
            await sent.edit(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))

            # Kick people out
            reacted_users = await portal_icon.users().flatten()
            reacted_igns = [i.nick for i in reacted_users]
            for i in VC.members:
                if i.nick not in reacted_igns:
                    await i.edit(voice_channel=guild.get_channel(LNG))

            # Remove Key-Reacts/DMS in Database
            key_reacts = pyc.get_item([guild_id, "afks", vc, "key-reacts"], [])
            for i in key_reacts:
                pyc.child(["key-react-dms", str(i)]).remove()
            pyc.child([guild_id, "afks", vc, "key-reacts"]).remove()

            # Countdown untill Post-AFK Ends
            while (countdown > 1):
                await asyncio.sleep(1)
                countdown -= 1
                title = "AFK Check for `" + VC.name + "` has ended"
                description = "Join `" + guild.get_channel(LNG).name + "` and re-react to " + str(portal_icon.emoji) + " to get moved back in. You have " + str(countdown) + " seconds left until post-afk ends"
                sent_embed_description = sent.embeds[0].description
                if "\n" in sent_embed_description:
                    description += "\n" + "\n".join(sent_embed_description.split("\n")[1:])
                await sent.edit(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))

            await asyncio.sleep(1)
            title = "Post-AFK Check for `" + VC.name + "` has ended"
            description = "Wait for the next run to begin"
            await sent.edit(embed=create_embed(type_="BASIC", fields={"title": title, "description": description}))

            # Kill AFK in Database
            pyc.child([guild_id, "afks", vc]).remove()

            return
        if (len(self.message_keys) > 0 and self.message_keys[0] == "-h"):
            help_messages = {
                "help": self.help_text
            }
            title = "Info on command `endafk`"
            description = ""
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description, "fields": fields}))
            return

class Logkeys(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            guild = self.message.guild
            guild_id = str(guild.id)          
            if (self.message_keys[0][0] == "-"):
                type_char = self.message_keys[0][1:]
                self.message_keys = self.message_keys[1:]
            else:
                type_char = pyc.get_item([guild_id, "type"])
            type_ = vars.dung_types[type_char]

            key_popper_id = vars.cleanse_mention(self.message_keys[0])
            if (key_popper_id == ""):
                return
            key_add = 1
            if (len(self.message_keys) > 1):
                key_add = int(self.message_keys[1])
            key_total_count = pyc.get_item([guild_id, "logs", "key-logs", key_popper_id, "total"], 0) + key_add
            key_type_count = pyc.get_item([guild_id, "logs", "key-logs", key_popper_id, type_], 0) + key_add
            pyc.child([guild_id, "logs", "key-logs", key_popper_id, "total"]).set(key_total_count)
            pyc.child([guild_id, "logs", "key-logs", key_popper_id, type_]).set(key_type_count)

            await self.message.add_reaction("✅")
            if (type_ in vars.vets):
                RSA = pyc.get_item([guild_id, "vet-rsa"])
            elif (type_ in vars.events):
                RSA = pyc.get_item([guild_id, "event-rsa"])
            else:
                RSA = pyc.get_item([guild_id, "rsa"])
            channel = guild.get_channel(int(RSA))
            name = guild.get_member(int(key_popper_id)).display_name
            await channel.send("**" + name + "** has popped " + str(key_type_count) + " " + type_ + " keys for the raiders! Her/his total key pop: " + str(key_total_count))
            return
        if (len(self.message_keys) == 0 and self.message_keys[0] == "-h"):
            title = "Info on command `logkeys`"
            description = ""
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
            return

class Runlogs(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def add(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            guild = self.message.guild
            guild_id = str(guild.id)          
            if (self.message_keys[0][0] == "-"):
                type_char = self.message_keys[0][1:]
                self.message_keys = self.message_keys[1:]
            else:
                type_char = pyc.get_item([guild_id, "type"])
            type_ = vars.dung_types[type_char]

            if self.message_keys[0] not in  ["s", "f"]:
                return
            run_type = self.message_keys[0]
            self.message_keys = self.message_keys[1:]

            leader = vars.cleanse_mention(self.message_keys[0])
            assists = []
            if (len(self.message_keys) > 1):
                for i in self.message_keys[1:]:
                    assists.append(vars.cleanse_mention(i))
            if (leader == ""):
                return

            guild = self.message.guild
            guild_id = str(guild.id)
            total_count = pyc.get_item([guild_id, "logs", "run-logs", "members", leader, "count"], {})
            if (run_type == "s"):
                if "Leads" in total_count:
                    total_count["Leads"] += 1
                else:
                    total_count["Leads"] = 1
                if "types" in total_count and type_ in total_count["types"]:
                    total_count["types"][type_] += 1
                elif "types" in total_count:
                    total_count["types"][type_] = 1
                else:
                    total_count["types"] = {type_: 1}
            elif (run_type == "f"):
                if "Fails" in total_count:
                    total_count["Fails"] += 1
                else:
                    total_count["Fails"] = 1
            pyc.child([guild_id, "logs", "run-logs", "members", leader, "count"]).set(total_count)

            for i in assists:
                total_count = pyc.get_item([guild_id, "logs", "run-logs", "members", i, "count"], {})
                if "Assists" in total_count:
                    total_count["Assists"] += 1
                else:
                    total_count["Assists"] = 1
                pyc.child([guild_id, "logs", "run-logs", "members", i, "count"]).set(total_count)

            log = {
                "Lead": leader,
                "Assists": assists,
                "Time": str(int(time.time())),
                "Type": type_,
                "Success": 1 if (run_type == "s") else 0
            }
            logs = pyc.get_item([guild_id, "logs", "run-logs", "logs"], [])
            logs.append(log)
            pyc.child([guild_id, "logs", "run-logs", "logs"]).set(logs)            

            await self.message.add_reaction("✅")
            return
        if (len(self.message_keys) == 0 and self.message_keys[0] == "-h"):
            title = "Info on command `runlogs add`"
            description = ""
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
            return

    async def recent(self):
        if (len(self.message_keys) == 0 or self.message_keys[0] != "-h"):
            guild = self.message.guild
            guild_id = str(guild.id)          
            
            week_before = int(time.time()) - 7*86400
            i = -1
            logs = pyc.get_item([str(self.message.guild.id), "logs", "run-logs", "logs"], [])
            data = {}
            while (i * -1 <= len(logs)):
                temp = logs[i]
                if (int(temp["Time"]) < week_before):
                    break
                assists = []
                if ("Assists" in temp):
                    assists = temp["Assists"]
                for j in [temp["Lead"]] + assists:
                    if j not in data:
                        data[j] = {
                            "Leads": 0,
                            "Assists": 0,
                            "Vet Leads": 0,
                            "Fails": 0
                        }

                if (temp["Success"] == 1):
                    data[temp["Lead"]]["Leads"] = data[temp["Lead"]]["Leads"] + 1
                    if (temp["Type"].split(" ")[0] == "Veteran"):
                        data[temp["Lead"]]["Vet Leads"] = data[temp["Lead"]]["Vet Leads"] + 1
                else:
                    data[temp["Lead"]]["Fails"] = data[temp["Lead"]]["Fails"] + 1
                for j in assists:
                    data[j]["Assists"] = data[j]["Assists"] + 1

                i -= 1

            title = "Run Statistics of the Last 7 Days"
            if (len(logs) == 0):
                description = "No runs have occurred in the last 7 days"
            else:
                description = "Runs occurred in the last 7 days"

            fields = []
            for i in data:
                member = self.message.guild.get_member(int(i))
                fields.append({
                    "name": "Leads: " + str(data[i]["Leads"]) + " Assists: " + str(data[i]["Assists"]),
                    "value": member.mention + " Vet Leads: " + str(data[i]["Vet Leads"]) + " Fails: " + str(data[i]["Fails"]),
                    "inline": False
            })

            await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description": description, "fields": fields}))

            return
        if (len(self.message_keys) > 0 and self.message_keys[0] == "-h"):
            title = "Info on command `runlogs recent`"
            description = "Displays the runs logged in the last week"
            fields = [{"name": i, "value": help_messages[i], "inline": True} for i in help_messages]
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
            return
 

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            if (len(self.message_keys) == 0):
                return
            if (self.message_keys[0] == "add"):
                self.message_keys = self.message_keys[1:]
                await self.add()
                return
            if (self.message_keys[0] == "recent"):
                self.message_keys = self.message_keys[1:]
                await self.recent()
                return
            return
        if (len(self.message_keys) == 0 and self.message_keys[0] == "-h"):
            title = "Info on command `runlogs`"
            description = ""
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
            return


class KeyReact:
    def __init__(self, reaction, user):
        self.reaction = reaction
        self.user = user
        self.key_types = {
            "<:ThicketKey:578181852154691594>": ["st"],
            "<:lh_key:715219618469380108>": ["c", "v", "vc"],
            "<:inc:738955715552608316>": ["o3"],
            "<:sword:738954924225724416>": ["o3"],
            "<:shield:738954978248360058>": ["o3"],
            "<:helm:738954951824375820>": ["o3"],
        }
        self.portals = {
            "<:ThicketPortal:578181776095051788>": ["st"],
            "<:cultist:715219618876227674>": ["c", "vc"],
            "<:O3:738186778829258854>": ["o3"]
        }
        self.extras = {
            "o3": {
                "<:inc:738955715552608316>": "wine incantation",
                "<:sword:738954924225724416>": "sword rune",
                "<:shield:738954978248360058>": "shield rune",
                "<:helm:738954951824375820>": "helm rune"
            }
        }
        self.keys = {
            "c": "<:cultist:715219618876227674>",
            "v": "",
            "st": "<:ThicketPortal:578181776095051788>",
            "vc": "<:cultist:715219618876227674>",
            "o3": "<:O3:738186778829258854>"
        }
    async def run(self):
        reaction, user = self.reaction, self.user
        # Key React
        if (reaction.message.author.id != user.id and str(reaction.emoji) in self.key_types):
            is_afk = False
            guild_id = str(reaction.message.guild.id)
            for i in pyc.get_item([guild_id, "afks"]):
                if ((pyc.get_item([guild_id, "afks", i, "id"]) == str(reaction.message.id)) and \
                    (pyc.get_item([guild_id, "afks", i, "type"]) in self.key_types[str(reaction.emoji)]) and \
                    (pyc.get_item([guild_id, "afks", i, "status"]) == "afk")):
                    is_afk = i
                    break
            if (is_afk == False):
                return
            current_afk_list = [guild_id, "afks", is_afk]
            key_dms = pyc.get_item(current_afk_list + ["key-reacts"], [])
            for i in key_dms:
                if (user.id == client.get_channel(int(i)).recipient.id):
                    return
            if (user.dm_channel is None):
                await user.create_dm()
            key_type = "key"
            key_emoji = str(reaction.emoji)
            if key_emoji in self.extras["o3"]:
                key_type = self.extras["o3"][key_emoji]
            sent_dm = await user.dm_channel.send("Thank you for reacting to the " + key_type + ". React to the :white_check_mark: to confirm your intention. Note: Fake reacts will result in a suspension")
            await sent_dm.add_reaction("✅")

            key_dms.append(str(sent_dm.channel.id))
            pyc.child(current_afk_list + ["key-reacts"]).set(key_dms)
            vars.db.child("key-react-dms").child(str(sent_dm.id)).set({
                "guild": str(reaction.message.guild.id),
                "afk-number": is_afk,
                "key": str(reaction.emoji)
            })
            return True
        # Confirm Key
        if (reaction.message.author.id != user.id and str(reaction.emoji) == "✅"):
            if not pyc.search(str(reaction.message.id), ["key-react-dms"]):
                return
            is_afk = pyc.get_item(["key-react-dms", str(reaction.message.id), "afk-number"])
            guild_id = str(pyc.get_item(["key-react-dms", str(reaction.message.id), "guild"]))
            current_afk_list = [guild_id, "afks", is_afk]
            key_reacts = pyc.get_item(current_afk_list + ["keys"], [])
            key_dms = pyc.get_item(current_afk_list + ["key-reacts"], [])

            if pyc.get_item([guild_id, "afks", is_afk, "type"]) in ["vc"]:
                channel = client.get_channel(int(pyc.get_item([guild_id, "vet-rsa"])))
            else:
                channel = client.get_channel(int(pyc.get_item([guild_id, "rsa"])))

            sent = await channel.fetch_message(int(pyc.get_item([guild_id, "afks", is_afk, "id"])))
            sent_embed = sent.embeds[0]
            loc = pyc.get_item(current_afk_list + ["location"])
            key_emoji = pyc.get_item(["key-react-dms", str(reaction.message.id), "key"])
            key_type = "key"
            afk_type = pyc.get_item(current_afk_list + ["type"], [])
            if key_emoji in self.extras["o3"]:
                key_type = self.extras["o3"][key_emoji]
            if (loc == ""):
                loc = "nonexistent"
            if (user.dm_channel is None):
                await user.create_dm()

            #Normal Key
            if (key_type == "key"):
                if (len(key_reacts) == 0):
                    await user.dm_channel.send("The location is `" + loc + "` You are the main key")
                elif (len(key_reacts) < 3):
                    await user.dm_channel.send("You are the backup key. If the RL wants backup keys to come to the location, he or she will DM you")
                else:
                    await user.dm_channel.send("We already have 3 key reacts at the moment")

                if (len(key_reacts) < 3):
                    key_reacts.append(str(user.id))
                    pyc.child(current_afk_list + ["keys"]).set(key_reacts)
                    key_dms.remove(str(reaction.message.channel.id))
                    pyc.child(current_afk_list + ["key-reacts"]).set(key_dms)
                    vars.db.child("key-react-dms").child(str(reaction.message.id)).remove()
            else:
                temp_reacts = pyc.get_item(current_afk_list + [key_type], [])
                if (len(temp_reacts) == 0):
                    await user.dm_channel.send("The location is `" + loc + "` You are the main `" + key_type + "`")
                elif (len(temp_reacts) < 1):
                    await user.dm_channel.send("The location is `" + loc + "` You are the backup `" + key_type + "`")
                else:
                    await user.dm_channel.send("We already have 2 `" + key_type + "` reacts at the moment")

                if (len(key_reacts) < 2):
                    temp_reacts.append(str(user.id))
                    pyc.child(current_afk_list + [key_type]).set(temp_reacts)
                    key_dms.remove(str(reaction.message.channel.id))
                    pyc.child(current_afk_list + ["key-reacts"]).set(key_dms)
                    vars.db.child("key-react-dms").child(str(reaction.message.id)).remove()

            #Edit Message
            main_message = sent_embed.description.split("\n\n")[0] + "\n"
            key_reacts = pyc.get_item([guild_id, "afks", is_afk, "keys"])
            if (key_type != "key"):
                key_ = self.keys[afk_type]
            else:
                key_ = key_emoji
            if key_reacts is not None:
                main_message += "\nMain " + key_emoji + ": " + client.get_guild(int(guild_id)).get_member(int(key_reacts[0])).mention
                if (len(key_reacts) > 1):
                    main_message += "\nBackup " + key_emoji + ": " + client.get_guild(int(guild_id)).get_member(int(key_reacts[1])).mention
                if (len(key_reacts) > 2):
                    main_message += "\nBackup " + key_emoji + ": " + client.get_guild(int(guild_id)).get_member(int(key_reacts[2])).mention
            if afk_type in self.extras:
                for i in self.extras[afk_type]:
                    if pyc.search(self.extras[afk_type][i], current_afk_list):
                        main_message += "\nMain " + i + ": " + client.get_guild(int(guild_id)).get_member(int(pyc.get_item(current_afk_list + [self.extras[afk_type][i]])[0])).mention

            await sent.edit(embed=create_embed(type_="basic", fields={"title": sent_embed.title, "description": main_message}))
            return True
        # Move Raiders Back
        if (reaction.message.author.id != user.id and str(reaction.emoji) in self.portals):
            print(str(reaction.emoji))
            guild = reaction.message.guild
            if guild is None:
                return
            guild_id = str(guild.id)
            afks = pyc.get_item([guild_id, "afks"], {})
            foundAFK = False
            for i in afks:
                if (int(afks[i]["id"]) == reaction.message.id):
                    foundAFK = i
            if not foundAFK:
                return

            if (foundAFK[1] == "v" and foundAFK != "-v"):
                VC_id = pyc.get_item([guild_id, "vet-vcs"])[int(foundAFK[2:])-1]
            else:
                VC_id = pyc.get_item([guild_id, "vcs"])[int(foundAFK[1:])-1]
            await user.edit(voice_channel=guild.get_channel(int(VC_id)))
            return True
        return

