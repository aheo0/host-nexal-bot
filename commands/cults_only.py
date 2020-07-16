from command import *
import aiohttp

class VetVerify(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.vet_rules = 728483562009133076
    
    async def run(self, author=None):
        CULT_COUNT = 50
        if author is None:
            user = message.author
        else:
            user = author
        
        if (len(self.message_keys) == 0):
            title = "Incorrect Command"
            description = "Please type your IGN. ie. `.nexal verify MeApollo`"
            await user.dm_channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            return

        try:
            IGN = self.message_keys[0]
            url = "https://www.realmeye.com/graveyard-summary-of-player/" + IGN
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url, headers=self.headers) as r:
                    text = await r.text()
            text = text.split("<td>Cultist Hideouts completed</td><td>")[1]
            text = text.split("</td>")[0]
            amount = int(text)
        except:
            title = "Realmeye for user `" + IGN + '` was not found'
            description = "Check the IGN you entered and your realmeye settings, and try again"
            await user.dm_channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            return

        if (amount < CULT_COUNT):
            title = "Realmeye for user `" + IGN + "`has less than `" + CULT_COUNT + "` cultist hideout completions"
            description = "If this was a mistake or you have more completitions on your alive characters that total up to the required amount, DM a staff in the server about it"
            await user.dm_channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            return

        pyc.child(["cults-only", "vet-verify", str(user.id)]).remove()
        guild = client.get_guild(713844220728967228)
        member = guild.get_member(user.id)

        if IGN.lower() not in member.nick.lower():
            title = "Invalid IGN"
            description = "This IGN is not verified with your account"
            await user.dm_channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            return

        roles = []
        already = False
        for i in member.roles:
            if (i.name == "Veteran Raider"):
                already = True
                break
            roles.append(i)
        if not already:
            roles.append(guild.get_role(733173709308821516))
            await member.edit(roles=roles)

        title = "Veteran Verification for `Cults Only` Complete"
        description = "Check " + client.get_channel(self.vet_rules).mention + " as veteran rules differ from its regular counterpart"
        await user.dm_channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description}))
        return
        


class KeyReact:
    def __init__(self, payload):
        self.payload = payload
    async def run(self):
        payload, user = self.payload, self.payload.member
        if (payload.message_id != 733141028197892179):
            return
        if (str(payload.emoji) == "✅"):
            vet_db_list = ["cults-only", "vet-verify", str(user.id)]
            verify_status = pyc.get_item(vet_db_list + ["status"])
            if verify_status is None:
                pyc.child(vet_db_list).set({
                    "status": "pending"
                })

            if (user.dm_channel is None):
                await user.create_dm()
            #title = "Verification for Veteran Runs for `Cults Only`"
            #description = "Once your realmeye settings are set, type `.nexal verify <Realmeye IGN>`\n\nie. `.nexal verify MeApollo`"
            #await user.dm_channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description}))

            IGN = user.nick.split(" ")[0].lower()
            while IGN[0] not in "qwertyuiopasdfghjklzxcvbnm":
                IGN = IGN[1:]
            await VetVerify(None, [IGN]).run(author=user)

            return True
        if (str(payload.emoji) == "❌"):
            isVet = False
            roles = []
            for i in user.roles:
                if (i.name == "Veteran Raider"):
                    isVet = i
                else:
                    roles.append(i)
            if not isVet:
                return
            await user.edit(roles=roles)

            if (user.dm_channel is None):
                await user.create_dm()
            title = "You are no longer a veteran raider in `Cults Only`"
            description = "If you ever want to re-apply, you know how!"
            await user.dm_channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description}))
            return True
        return


