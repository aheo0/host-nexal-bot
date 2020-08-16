from command import *
import aiohttp

class Verify(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
    
    async def run(self):
        db_list = ["wonderland", "verify", str(self.message.author.id)]
        status = pyc.get_item(db_list + ["status"])
        if (status is None):
            return True
        if (status == "pending"):
            IGN = self.message_keys[0]
            for i in IGN.lower():
                if i not in "qwertyuiopasdfghjklzxcvbnm":
                    return
            pyc.child(db_list + ["IGN"]).set(IGN)
            counter = 1
            pyc.child(db_list).child("counter").set(counter)
            veri_id = pyc.get_item(db_list + ["veri_id"])
            channel = await client.fetch_channel(735308975586934864)
            await channel.send(self.message.author.mention + " has started the verification process with IGN " + IGN + " and verification id " + veri_id)

            title = "Verification for 'Wonderland' with IGN `" + IGN + "` has Started"
            description = "Please follow the instructions. React with ✅ once you're done"
            fields = [
                {
                    "name": "Type in `Wonderland_" + veri_id + "` in one your Realmeye descriptions",
                    "value": "Note it is case-sensitive",
                    "inline": False
                }
            ]
            sent = await self.message.author.dm_channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description, "fields": fields}))
            pyc.child(db_list + ["msg_id"]).set(str(self.message.id))
            await sent.add_reaction("✅")

            pyc.child(db_list + ["status"]).set("realmeye")
            return True
        if (status == "realmeye"):
            counter = int(pyc.get_item(db_list + ["counter"])) + 1
            pyc.child(db_list).child("counter").set(counter)
            if (counter == 15):
                channel = await client.fetch_channel(735308975586934864)
                await channel.send(self.message.author.mention + " has been banned from verifying. Reason: `spamming the verification bot`")
                return
            pyc.child(db_list).child("counter").set(counter)

            IGN = self.message_keys[0]
            for i in IGN.lower():
                if i not in "qwertyuiopasdfghjklzxcvbnm":
                    return
            pyc.child(db_list + ["IGN"]).set(IGN)
            
            veri_id = int(pyc.get_item(["wonderland", "veri_id"])) + 1
            pyc.child(["wonderland", "veri_id"]).set(str(veri_id))
            pyc.child(db_list).child("veri_id").set(str(veri_id))
            veri_id = pyc.get_item(db_list + ["veri_id"])
            channel = await client.fetch_channel(735308975586934864)
            await channel.send(self.message.author.mention + " has started the verification process with IGN " + IGN + " and verification id " + veri_id)

            title = "Verification for 'Wonderland' with IGN `" + IGN + "` has Started"
            description = "Please follow the instructions. React with ✅ once you're done"
            fields = [
                {
                    "name": "Type in `Wonderland_" + veri_id + "` in one your Realmeye descriptions",
                    "value": "Note it is case-sensitive",
                    "inline": False
                }
            ]
            sent = await self.message.author.dm_channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description, "fields": fields}))
            pyc.child(db_list + ["msg_id"]).set(str(self.message.id))
            await sent.add_reaction("✅")
            return True
        return
        

class KeyReact:
    def __init__(self, payload):
        self.payload = payload
        self.headers = {"User-Agent": "Mozilla/5.0"}
    async def run(self):
        payload, user = self.payload, self.payload.member
        if (str(payload.emoji) != "✅"):
            return
        if (payload.message_id == 744479057026089030):
            vet_db_list = ["wonderland", "verify", str(user.id)]
            verify_status = pyc.get_item(vet_db_list + ["status"])
            if verify_status is None:
                veri_id = int(pyc.get_item(["wonderland", "veri_id"])) + 1
                pyc.child(vet_db_list).set({
                    "status": "pending",
                    "veri_id": str(veri_id)
                })
                pyc.child(["wonderland", "veri_id"]).set(str(veri_id))

            if (user.dm_channel is None):
                await user.create_dm()

            title = "Verification for 'Wonderland' has Started"
            description = "Please follow the instructions. If this verification stops working at any point, restart the verification via re-reacting in the verify channel."
            fields = [
                {
                    "name": "Type in your RotMG In-Game-Name (IGN)",
                    "value": "i.e. MeApollo",
                    "inline": False
                }
            ]
            await user.dm_channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description, "fields": fields}))
            veri_id = pyc.get_item(vet_db_list + ["veri_id"])
            channel = await client.fetch_channel(735308975586934864)
            await channel.send(user.mention + " has started the verification process with verification id " + veri_id)
            return True
        channel_ = await client.fetch_channel(payload.channel_id)
        if (str(channel_.type) == "private"):
            user = client.get_user(payload.user_id)
            vet_db_list = ["wonderland", "verify", str(user.id)]
            verify_status = pyc.get_item(vet_db_list + ["status"])
            if verify_status is None:
                return
            if (verify_status == "done"):
                return
            IGN = pyc.get_item(vet_db_list + ["IGN"])
            try:
                url = "https://www.realmeye.com/player/" + IGN
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(url, headers=self.headers) as r:
                        text = await r.text()
            except:
                title = "Realmeye for user `" + IGN + '` was not found'
                description = "Check the IGN you entered and your realmeye settings, and re-react to the ✅ in the above message"
                await channel_.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                return

            veri_id = pyc.get_item(vet_db_list + ["veri_id"])
            if "Wonderland_" + veri_id not in text:
                title = "Realmeye for user `" + IGN + '` was invalid'
                description = "Add `Wonderland_" + veri_id + "`, and re-react to the ✅ in the above message. If you have already updated your Realmeye, just wait for Realmeye to update it on their servers, and re-react"
                await channel_.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
                return
            
            guild = client.get_guild(666063675416641539)
            member = guild.get_member(user.id)

            roles = member.roles
            roles.append(guild.get_role(689460753178296365))
            try:
                await member.edit(nick=IGN)
            except:
                pass
            try:
                await member.edit(roles=roles)
            except:
                pass

            title = "Verification for `Wonderland` Complete"
            if user.dm_channel is None:
                await user.create_dm()
            await channel_.send(embed=create_embed(type_="REPLY", fields={"title": title}))

            channel = await client.fetch_channel(735308975586934864)
            await channel.send(user.mention + " has been verified")

            pyc.child(vet_db_list + ["status"]).set("done")
            return True
        return


