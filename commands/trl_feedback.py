from command import *
import pyrebase, asyncio

class TrlFeedback:
    def __init__(self):
        self.emojis_x = [
            ["⚪", "⚫", "🔴", "🔵"],
            ["2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"],
            ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤"],
            ["🍈", "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆"]
        ]
        self.emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        self.next = "✅"
        self.cancel = "❌"
        self.items = {
            "AFK Check": [
                "Called for rushers and DM’d them the location",
                "Traded and Confirmed key, also announcing it in VC",
                "When ending AFK, announced in VC that if you are moved out, to re-react in order to get moved back",
                "The whole AFK process took under 5 minutes. (Do not mark off if RL was waiting for keys/rushers/classes)",
                "RL told the key to pop at the number of people in VC"
            ], "Halls": [
                "Started clearing immediately after everyone loaded in",
                "Listened to rushers while map reading",
                "Crusades: Called for stuns and slows; decoys and stasises when necessary + the wall/direction the crusade should be dragged",
                "Oryx rooms: Called to clear/decoy outers, and where the Mario was. RL called for stasises when skipping, and exercised good judgement on when to skip by peeking rooms for upcoming splits",
                "Slime rooms: Called to push in and stun the slime, and stasises on mini slimes when necessary. RL called the group to clear the small slimes after the big one died",
                "Golem rooms: Called the locations of angry boys, mseal deep and for knights to push in and stun the big boy + cleared dangerous golems before moving on",
                "Spooky: Informed group when a rusher called it. When spooky in group: Called for decoys and dealt calmly",
                "T-Room: Informed raiders that troom was active (if applicable). RL called for dazes and stasises, + counted down from 3 for the mystics"
            ], "Hideout": [
                "Started clearing immediately, regardless if there were rushers",
                "Red demon: Called for decoys top-right and dazes + warned group of the danger of the flames",
                "Three-headed demon: Called for slows on Red and Green, and told the group when to back up + decoys into the middle",
                "Beginning of shotgun phase: Told everyone to back off for 1/3/5 shotguns",
                "Each shotgun phase: Called for knights to focus Red, White and Purple  + location of the cultists for group to focus",
                "Called the shape/color Malus + appropriate callouts",
                "During shape/color, called out to focus minions (if applicable)",
                "Countdowned 5 Shotguns in Last Phase"
            ]
        }
        self.feedback_boxes = {
            "c": ["Cultist Hideout", "AFK Check", "Halls", "Hideout"]
        }
        
    async def run(self, message, message_keys):
        if (message.channel.id != 733045203946176612):
            title = "TRL Feedback Bot does not work here"
            description = "Go to " + client.get_channel(pyc.get_item(["cults-only", "feedback", "bcs"])).mention
            await message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            return
        run_char = "c"
        run_type = self.feedback_boxes[run_char]
        count = pyc.get_item(["cults-only", "feedback", "trls", str(message_keys[0]), "count"], 0)
        if (len(message_keys) > 1):
            count = int("".join(message_keys[1:])) - 1
        trl_name = message.guild.get_member(int(message_keys[0][3:-1])).nick
        title = "TRL Feedback #" + str(count+1) + " started for " + trl_name
        description = "React to the according emojis " + self.emojis[0] + ", " + self.emojis[1] + ", " + self.emojis[2] + ", etc. to mark the respective choice(s)"
        current_items = self.items[self.feedback_boxes["c"][1]]
        fields = [{
            "name": self.feedback_boxes["c"][1] + " (Mark ones the TRL did NOT do)",
            "value": "\n".join([self.emojis[i] + " " + current_items[i] for i in range(len(current_items))])
        }]
        sent = await message.channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description, "fields": fields}))
        for i in range(len(current_items)):
            await sent.add_reaction(self.emojis[i])
        await sent.add_reaction(self.next)
        await sent.add_reaction(self.cancel)
        pyc.child(["cults-only", "feedback", "trls", str(message_keys[0])]).set(count)
        pyc.child(["cults-only", "feedback", "commands", str(sent.id)]).set({
            "trl": message_keys[0],
            "id": str(sent.id),
            "status": "1",
            "trl-name": trl_name,
            "rl": message.author.mention
        })
        return

    async def KeyReact(self, reaction, user):
        db = pyc.get_item(["cults-only", "feedback", "commands", str(reaction.message.id)])
        if (reaction.message.author.id == user.id or db["status"] == "comments"):
            return
        if (str(reaction.emoji) == self.next):
            if (db["status"] == "overall"):
                rating = 1
                for i in reaction.message.reactions:
                    if (i.count > 1 and str(i.emoji) != self.next):
                        break
                    rating += 1
                command_list = ["cults-only", "feedback", "commands", str(reaction.message.id)]
                pyc.child(command_list + ["Overall", "rating"]).set(rating)
                sent = await reaction.message.channel.fetch_message(pyc.get_item(command_list + ["id"]))
                print(pyc.get_item(["cults-only", "feedback", "feedback-channel"]))
                new_description = "Now type in any __Additional Feedback__ below. Note: This is **required**. After this, the feedback will be posted in " + \
                    reaction.message.guild.get_channel(int(pyc.get_item(["cults-only", "feedback", "feedback-channel"]))).mention
                pyc.child(["cults=only", "feedback", "commands", str(reaction.message.id), "status"]).set("comments")
                await sent.edit(embed=create_embed(type_="DM", fields={"title": sent.embeds[0].title, "description": new_description}))
                await sent.clear_reactions()
            elif ("." in db["status"]):
                new_status = int(db["status"][:-2]) + 1
                command_list = ["cults-only", "feedback", "commands", str(reaction.message.id)]
                old_name = self.feedback_boxes["c"][new_status-1]
                rating = 1
                for i in reaction.message.reactions:
                    if (i.count > 1 and str(i.emoji) != self.next):
                        break
                    rating += 1
                pyc.child(command_list + [old_name, "rating"]).set(rating)
                if (new_status < len(self.feedback_boxes["c"])):
                    new_name = self.feedback_boxes["c"][new_status]
                    pyc.child(command_list + ["status"]).set(str(new_status))

                    sent = await reaction.message.channel.fetch_message(pyc.get_item(command_list + ["id"]))
                    current_items = self.items[new_name]
                    fields = [{
                        "name": new_name + " (Mark ones the TRL diid NOT do)",
                        "value": "\n".join([self.emojis[i] + " " + current_items[i] for i in range(len(current_items))])
                    }]
                    await sent.edit(embed=create_embed(type_="DM", fields={"title": sent.embeds[0].title, "description": sent.embeds[0].description, "fields": fields}))
                    await sent.clear_reactions()
                    for i in range(len(current_items)):
                        await sent.add_reaction(self.emojis[i])
                    await sent.add_reaction(self.next)
                    await sent.add_reaction(self.cancel)
                else:
                    pyc.child(command_list + ["status"]).set("overall")
                    sent = await reaction.message.channel.fetch_message(pyc.get_item(command_list + ["id"]))
                    new_field = {
                        "name": "Rate Overall (Choose 1 to give a rating out of 10)",
                        "value": "1️⃣ for worst, 🔟 for best"
                    }
                    await sent.edit(embed=create_embed(type_="DM", fields={"title": sent.embeds[0].title, "description": sent.embeds[0].description, "fields": [new_field]}))
                    await sent.clear_reactions()
                    for i in self.emojis + [self.next] + [self.cancel]:
                        await sent.add_reaction(i)
            else:
                answers = []
                counter = 0
                for i in reaction.message.reactions:
                    if (i.count > 1 and str(i.emoji) != self.next):
                        answers.append(counter)
                    counter += 1
                await reaction.message.clear_reactions()
                command_list = ["cults-only", "feedback", "commands", str(reaction.message.id)]
                pyc.child(command_list + [self.feedback_boxes["c"][int(db["status"])], "reactions"]).set(answers)
                pyc.child(command_list + ["status"]).set(db["status"] + ".5")
                sent = await reaction.message.channel.fetch_message(pyc.get_item(command_list + ["id"]))
                new_field = {
                    "name": "Rate " + self.feedback_boxes["c"][int(db["status"])] + " (Choose 1 to give a rating out of 10)",
                    "value": "1️⃣ for worst, 🔟 for best"
                }
                await sent.edit(embed=create_embed(type_="DM", fields={"title": sent.embeds[0].title, "description": sent.embeds[0].description, "fields": [new_field]}))
                for i in self.emojis + [self.next] + [self.cancel]:
                    await sent.add_reaction(i)
            return True
        if (str(reaction.emoji) == self.cancel):
            return True

        return


    async def post_message(self, message_id, content):
        db = pyc.get_item(["cults-only", "feedback", "commands", message_id])
        count = pyc.get_item(["cults-only", "feedback", "trls", db["trl"]])
        title = "TRL Feedback #" + str(count+1) + " for " + db["trl-name"] + " (" + str(db["Overall"]["rating"]) + "/10)"
        description = "Given by: " + db["rl"]
        fields = []
        for i in db:
            if (i in self.items):
                name = i + " (" + str(db[i]["rating"]) + "/10)"
                value = ""
                for j in db[i]["reactions"]:
                    value += self.cancel + " " + self.items[i][j] + "\n"
                fields.append({"name": name, "value": value, "inline" :False})
        fields.append({
            "name": "Additional Feedback",
            "value": content,
            "inline": False
        })
        await client.get_channel(int(pyc.get_item(["cults-only", "feedback", "feedback-channel"]))).send(db["trl"], embed=create_embed(type_="DM", fields={"title": title, "description": description, "fields": fields}))
        sent = await client.get_channel(int(pyc.get_item(["cults-only", "feedback", "bcs"]))).fetch_message(int(message_id))
        await sent.edit(embed=create_embed(type_="REPLY", fields={"title": "TRL Feedback #" + str(count+1) + " for " + db["trl-name"] + " has ended"}))
        
        pyc.child(["cults-only", "feedback", "commands", message_id]).remove()
        pyc.child(["cults-only", "feedback", "trls", db["trl"]]).set(count + 1)
        return

