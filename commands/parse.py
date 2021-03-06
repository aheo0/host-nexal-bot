from command import *
import json, re, aiohttp, requests
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from io import BytesIO



class Parse(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.help_text = "Lists possible commands"
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.max_dps_stats = {
            "Rogue": [50, 75],
            "Archer": [75, 50],
            "Wizard": [75, 75],
            "Priest": [50, 55],
            "Warrior": [75, 50],
            "Knight": [50, 50],
            "Paladin": [50, 45],
            "Assassin": [60, 75],
            "Necromancer": [75, 60],
            "Huntress": [75, 50],
            "Mystic": [60, 55],
            "Trickster": [65, 75],
            "Sorcerer": [70, 60],
            "Ninja": [70, 70],
            "Samurai": [75, 50],
            "Bard": [55, 70]
        }
        self.vet = False
        self.dung_type = pyc.get_item([str(self.message.guild.id), "type"], "")

    async def checkStats(self, guild, igns, users=None, dung_type="c", vet=False):
        with open("data/reqs.json") as f:
            banned = json.load(f)
        type_char = dung_type
        if vet:
            type_char = "v" + type_char
        banned = banned[type_char]
        invisible = []
        meets = []
        doesnt = []
        reasons = []
        if (len(igns)!=0):
            counter = -1
            for i in range(len(igns)):
                counter += 1
                worked = False
                reason = []
                try:
                    IGN = igns[i]
                    url = "https://www.realmeye.com/player/" + IGN
                    #request = requests.get(url=url, headers=self.headers)
                    #text = request.text
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(url, headers=self.headers) as r:
                            text = await r.text()

                    data = text.split("<tbody>")
                    data = data[1].split("<tr>")
                    data = data[1].split("<td>")
                    class_ = data[3].split("</td>")
                    class_ = class_[0]
                    equipment = data[9].split("item-wrapper")
                    weapon = equipment[1].split("/wiki/")
                    if (len(weapon) == 1):
                        weapon = ""
                    else:
                        weapon = weapon[1].split("\"")
                        weapon = weapon[0]
                    ability = equipment[2].split("/wiki/")
                    if (len(ability) == 1):
                        ability = ""
                    else:
                        ability = ability[1].split("\"")
                        ability = ability[0]
                    armor = equipment[3].split("/wiki/")
                    if (len(armor) == 1):
                        armor = ""
                    else:
                        armor = armor[1].split("\"")
                        armor = armor[0]
                    ring = equipment[4].split("/wiki/")
                    if (len(ring) == 1):
                        ring = ""
                    else:
                        ring = ring[1].split("\"")
                        ring = ring[0]
                    stats = data[10].split("data-stats=\"[")
                    stats = stats[1].split("]")
                    stats = stats[0].split(",")
                    bonus = data[10].split("data-bonuses=\"[")
                    bonus = bonus[1].split("]")
                    bonus = bonus[0].split(",")
                    worked = True
                except:
                    invisible.append(IGN)
                    pass

                if (type_char == "c"):
                    # Stats
                    if (not worked):
                        continue
                    if (not (int(stats[2])-int(bonus[2]) == self.max_dps_stats[class_][0])):
                        reason.append("Att")
                    if (not (int(stats[7])-int(bonus[7]) == self.max_dps_stats[class_][1])):
                        reason.append("Dex")
                        
                    # Equipment
                    if weapon in banned[class_][0]:
                        if (weapon == ""):
                            reason.append("Weapon: not equipped")
                        else:
                            words = [i[0].upper() + i[1:] for i in weapon.split("-")]
                            reason.append("Weapon: " + " ".join(words))
                    if ability in banned[class_][1]:
                        if (ability == ""):
                            reason.append("Ability: not equipped")
                        else:
                            words = [i[0].upper() + i[1:] for i in ability.split("-")]
                            reason.append("Ability: " + " ".join(words))
                    if armor in banned[class_][2]:
                        if (armor == ""):
                            reason.append("Armor: not equipped")
                        else:
                            words = [i[0].upper() + i[1:] for i in armor.split("-")]
                            reason.append("Armor: " + " ".join(words))
                    if ring in banned[class_][3]:
                        if (ring == ""):
                            reason.append("Ring: not equipped")
                        else:
                            words = [i[0].upper() + i[1:] for i in ring.split("-")]
                            reason.append("Ring: " + " ".join(words))
                    
                    # Meets Reqs
                    if (len(reason) == 0):
                        if users is None:
                            meets.append(IGN)
                        else:
                            meets.append([users[i], IGN])
                    else:
                        if users is None:
                            doesnt.append(IGN)
                        else:
                            doesnt.append([users[i], IGN])
                        reasons.append(reason)
                if (type_char == "vc"):
                    # Stats
                    if (not worked):
                        continue
                    if (not (int(stats[2])-int(bonus[2]) == self.max_dps_stats[class_][0])):
                        reason.append("Att")
                    if (not (int(stats[7])-int(bonus[7]) == self.max_dps_stats[class_][1])):
                        reason.append("Dex")
                        
                    # Equipment
                    if weapon in banned[class_][0]:
                        if (weapon == ""):
                            reason.append("Weapon: not equipped")
                        else:
                            words = [i[0].upper() + i[1:] for i in weapon.split("-")]
                            reason.append("Weapon: " + " ".join(words))
                    if ability in banned[class_][1]:
                        if (ability == ""):
                            reason.append("Ability: not equipped")
                        else:
                            words = [i[0].upper() + i[1:] for i in ability.split("-")]
                            reason.append("Ability: " + " ".join(words))
                    if armor in banned[class_][2]:
                        if (armor == ""):
                            reason.append("Armor: not equipped")
                        else:
                            words = [i[0].upper() + i[1:] for i in armor.split("-")]
                            reason.append("Armor: " + " ".join(words))
                    if ring in banned[class_][3]:
                        if (ring == ""):
                            reason.append("Ring: not equipped")
                        else:
                            words = [i[0].upper() + i[1:] for i in ring.split("-")]
                            reason.append("Ring: " + " ".join(words))
                    
                    # Meets Reqs
                    if (len(reason) == 0):
                        if users is None:
                            meets.append(IGN)
                        else:
                            meets.append([users[i], IGN])
                    else:
                        if users is None:
                            doesnt.append(IGN)
                        else:
                            doesnt.append([users[i], IGN])
                        reasons.append(reason)
                if (type_char == "st"):
                    # Stats
                    if (not worked):
                        continue
                    if (not (int(stats[2])-int(bonus[2]) == self.max_dps_stats[class_][0]) and not (int(stats[7])-int(bonus[7]) == self.max_dps_stats[class_][1])):
                        reason.append("Att")
                        reason.append("Dex")
                        
                    # Equipment
                    if weapon in banned[class_][0]:
                        if (weapon == ""):
                            reason.append("Weapon: not equipped")
                        else:
                            words = [i[0].upper() + i[1:] for i in weapon.split("-")]
                            reason.append("Weapon: " + " ".join(words))
                    
                    # Meets Reqs
                    if (len(reason) == 0):
                        if users is None:
                            meets.append(IGN)
                        else:
                            meets.append([users[i], IGN])
                    else:
                        if users is None:
                            doesnt.append(IGN)
                        else:
                            doesnt.append([users[i], IGN])
                        reasons.append(reason)
        return ([invisible, meets, doesnt, reasons])

    async def run(self):
        if(len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            # Reqs
            if (self.message_keys[0][0] == "-"):
                self.vet = self.message_keys[0][1:]
                self.message_keys = self.message_keys[1:]

            # VC Number + Reqs
            try:
                channel_number = int(self.message_keys[0]) - 1
            except:
                title = "Invalid Raiding VC Number"
                description = "Type `.nexal parse -h` for more information about the command"
                await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                return

            # People in Dungeon
            if (len(self.message_keys) > 1):
                raiders = " ".join(self.message_keys[1:])
                raiders = raiders.replace("\n", " ").replace(",", " ").replace(".", " ").replace("  ", " ")
                raiders = re.sub(" +", " ", raiders).split(" ")
            else:
                raiders = []
            if (self.message.attachments is not None and len(self.message.attachments)>0):
                pil_image = Image.open(BytesIO(requests.get(self.message.attachments[0].url).content))
                #ocr_text = pytesseract.image_to_string(pil_image, config='--psm 6 --oem 0 tessedit_char_whitelist=1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM():')
                ocr_text = pytesseract.image_to_string(pil_image)
                if (":" in ocr_text):
                    ocr_text = " ".join(ocr_text.split(":")[1:])
                raiders_list = ocr_text.replace("\n", " ").replace(",", " ").replace(".", " ").replace("  ", " ")
                raiders_ = re.sub(" +", " ", raiders_list).split(" ")
                raiders = []
                for i in raiders_:
                    if (i != ""):
                        raiders.append(i)

            # People in VC
            vc_people = self.message.guild.get_channel(int(pyc.get_item([str(self.message.guild.id), "vcs"])[channel_number])).members

            crashers = []
            non_crashers = []

            not_in_server = []
            server_crashers = []

            invisible = []

            if ((len(self.message_keys) > 1 or len(self.message.attachments) > 0)):
                # Check Crashers
                for i in raiders:
                    crashing = True
                    id = 0
                    for j in vc_people:
                        staff = False
                        discord_name = j.display_name.lower()
                        if (discord_name[0].lower() not in 'qwertyuiopasdfghjklzxcvbnm'):
                            staff = True
                        alts = discord_name.split(" | ")
                        if (staff):
                            while alts[0][0] not in 'qwertyuiopasdfghjklzxcvbnm':
                                alts[0] = alts[0][1:]
                        if (i.lower() in alts):
                            crashing = False
                            id = j.id
                            break
                    if (crashing):
                        crashers.append(i)
                    else:
                        non_crashers.append([id, i.lower()])

                # Check if Crasher is in Server
                for i in crashers:
                    in_server = False
                    id = 0
                    for j in self.message.guild.members:
                        staff = False
                        discord_name = j.display_name.lower()
                        if (discord_name[0].lower() not in 'qwertyuiopasdfghjklzxcvbnm'):
                            staff = True
                        alts = discord_name.split(" | ")
                        if (staff):
                            alts[0] = alts[0][1:]
                        if (i.lower() in alts):
                            in_server = True
                            id = j.id
                            break
                    if (in_server):
                        server_crashers.append([id, i.lower()])
                    else:
                        not_in_server.append(i)

                # Check if Raiders Meet Reqs.
                temp1 = []
                temp2 = []
                for i in server_crashers:
                    temp1.append(i[0])
                    temp2.append(i[1])
                temp3, only_crashing, crashing_without_reqs, crashing_without_reqs_reasons = await self.checkStats(self.message.guild.id, temp2, temp1, dung_type=self.dung_type, vet=self.vet)
                for i in temp3:
                    invisible.append(i)

                temp1 = []
                temp2 = []
                for i in non_crashers:
                    temp1.append(i[0])
                    temp2.append(i[1])
                temp3, temp4, only_noreqs, only_noreqs_reasons = await self.checkStats(self.message.guild.id, temp2, temp1, dung_type=self.dung_type, vet=self.vet)
                for i in temp3:
                    invisible.append(i)

                temp3, only_not_in_server, not_in_server_reqs, not_in_server_reqs_reasons = await self.checkStats(self.message.guild.id, not_in_server, dung_type=self.dung_type, vet=self.vet)
                for i in temp3:
                    invisible.append(i)
            else:
                IGNS = []
                for i in vc_people:
                    if (i.display_name.lower()[0] not in 'qwertyuiopasdfghjklzxcvbnm'):
                        j = i.display_name[1:]
                    else:
                        j = i.display_name
                    
                    alts = j.lower().split(" | ")
                    for k in alts:
                        IGNS.append(k)
                        raiders.append(i.id)

                invisible, temp, only_noreqs, only_noreqs_reasons = await self.checkStats(self.message.guild.id, IGNS, raiders, dung_type=self.dung_type, vet=self.vet)
                only_crashing, crashing_without_reqs, only_not_in_server, not_in_server_reqs = [[], [], [], []]

            # Send Message
            title = "Parse of `" + self.message.guild.get_channel(int(pyc.get_item([str(self.message.guild.id), "vcs"], [])[channel_number])).name + "` is done"
            description = "Parse by: " + self.message.author.mention
            send_messages = {}
            if (len(invisible) != 0):
                temp = {invisible[0]: ""}
                if (len(invisible) > 1):
                    for i in invisible[1:]:
                        temp[invisible[0]] += "[" + i + "] "
                send_messages["Invisible Realmeyes:"] = temp
            if (len(only_not_in_server) != 0):
                temp = {only_not_in_server[0]: ""}
                if (len(only_not_in_server) > 1):
                    for i in only_not_in_server[1:]:
                        temp[only_not_in_server[0]] += "[" + i + "] "
                send_messages["Not-In-Server Crashers:"] = temp
            fields = []
            if (len(not_in_server_reqs)!=0):
                temp = {not_in_server_reqs[0]: ""}
                if (len(not_in_server_reqs) > 1):
                    for i in not_in_server_reqs[1:]:
                        temp[not_in_server_reqs[0]] += "[" + i + "] "
                send_messages["Not-In-Server Crashers without Reqs:"] = temp
            for i in send_messages:
                name = i
                inline = False
                value = "```css\n"
                for j in send_messages[i]:
                    value += "[" + j + "] " + send_messages[i][j] + "\n"
                value += "```"
                fields.append({"name": name, "value": value, "inline": inline})
            if (len(only_crashing) != 0):
                value = ""
                for i in only_crashing:
                    name = self.message.guild.get_member(i[0])
                    if ("|" not in name.display_name):
                        value += self.message.guild.get_member(i[0]).mention + " "
                    else:
                        value += self.message.guild.get_member(i[0]).mention + " (" + i[1] + ") "
            if (len(only_noreqs) != 0):
                value = ""
                counter = -1
                for i in only_noreqs:
                    counter += 1
                    name = self.message.guild.get_member(i[0])
                    if ("|" not in name.display_name):
                        value += self.message.guild.get_member(i[0]).mention + " "
                    else:
                        value += self.message.guild.get_member(i[0]).mention + " (" + i[1] + ") "
                    for j in only_noreqs_reasons[counter]:
                        value += "[" + j + "] "
                fields.append({"name": "Not Reqs:", "value": value, "inline": False})
            if (len(crashing_without_reqs) != 0):
                value = ""
                counter = -1
                for i in crashing_without_reqs:
                    counter += 1
                    name = self.message.guild.get_member(i[0])
                    if ("|" not in name.display_name):
                        value += self.message.guild.get_member(i[0]).mention + " "
                    else:
                        value += self.message.guild.get_member(i[0]).mention + " (" + i[1] + ") "
                    for j in crashing_without_reqs_reasons[counter]:
                        value += "[" + j + "] "
                fields.append({"name": "Crashing without Reqs:", "value": value, "inline": False})
            if (len(fields) == 0):
                fields.append({"name": "All Good!", "value": "Everybody parsed is in the voice channel and meets reqs", "inline": False})
            
            await self.message.channel.send(self.message.author.mention, embed=create_embed(type_="BASIC", fields={"title": title, "description": description, "fields": fields}))

            if (self.message.guild.id == 713844220728967228):
                # Cults Only Bouncers Output
                bouncer = False
                for i in self.message.author.roles:
                    if (str(i.name) == "Bouncer"):
                        bouncer = True
                        break

                if bouncer:
                    await client.get_guild(713844220728967228).get_channel(713844221530079273).send(self.message.author.mention + " parsed for stats in vc # " + str(int(channel_number)+1))
            return
        if (len(self.message_keys) > 0 and self.message_keys[0] == "-h"):
            help_messages = {
                "COMMANDS": {
                    "parse vc": "Only parses for stats and equipment from the people in vc. ie. .nexal_parse_1 Beware for parses on alts not in the run. These are denoted with (alt)",
                    "parse vc (+screenshot)": "ie. .nexal_parse_1 and add a screenshot of the /who command with a black background",
                    "parse vc (*raiders)": "You can also list the raiders after the command separated by either a comma, period, space, or a newline ie. .nexal_parse_1_MeApollo_nexal"
                }
            }
            title = "Info on command `parse`"
            description = "Parses raiders for requirements"
            fields = []
            for i in help_messages:
                name = i
                inline = False
                value = "```css\n"
                for j in help_messages[i]:
                    value += "[" + j + "] " + help_messages[i][j] + "\n"
                value += "```"
                fields.append({"name": name, "value": value, "inline": inline})
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description, "fields": fields}))
            return


class ParseList(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (len(self.message_keys) > 0 and self.message_keys[0] != "-h"):
            channel_number = self.message_keys[0]
            if (channel_number[0] == "v"):
                channel_id = pyc.get_item([str(self.message.guild.id), "vet-vcs"])[int(channel_number[1:]) - 1]
            else:
                channel_id = pyc.get_item([str(self.message.guild.id), "vcs"])[int(channel_number) - 1]
            vc_people = self.message.guild.get_channel(int(channel_id)).members

            IGNS = []
            for i in vc_people:
                temp = i.display_name
                while temp[0].lower() not in "qwertyuiopasdfghjklzxcvbnm":
                    temp = temp[1:]
                if "|" in temp:
                    for i in temp.split("|"):
                        IGNS.append(i.replace(" ", "")).upper()
                else:
                    IGNS.append(temp.upper())
            IGNS = sorted(IGNS)

            title = "Raiders in `" + self.message.guild.get_channel(int(channel_id)).name + "`"
            description = ", ".join(IGNS)
            await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description": description}))
            return

        if (len(self.message_keys) > 0 and self.message_keys[0] == "-h"):
            title = "Info on command `parselist`"
            description = "Type `.nexal parselist 1` or replace 1 with the vc number to list the raiders in vc"
            await self.message.channel.send(embed=create_embed(type_="HELP-MENU", fields={"title": title, "description": description}))
            return

