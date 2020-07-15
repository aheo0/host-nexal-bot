from command import *
import aiohttp

class VetVerify(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.vet_rules = 732835519913787422
    
    async def run(self):
        CULT_COUNT = 50
        
        if (len(self.message_keys) == 0):
            title = "Incorrect Command"
            description = "Please type your IGN. ie. `.nexal verify MeApollo`"
            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
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
            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            return

        if (amount < CULT_COUNT):
            title = "Realmeye for user `" + IGN + "`has less than `" + CULT_COUNT + "` cultist hideout completions"
            description = "If this was a mistake or you have more completitions on your alive characters that total up to the required amount, DM a staff in the server about it"
            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            return

        pyc.child(["cults-only", "vet-verify", str(self.message.author.id)]).remove()
        guild = client.get_guild(715217084900180048)
        member = guild.get_member(self.message.author.id)

        if IGN.lower() not in member.nick.lower():
            title = "Invalid IGN"
            description = "This IGN is not verified with your account"
            await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))
            return

        roles = []
        already = False
        for i in member.roles:
            if (i.name == "Veteran Raider"):
                already = True
                print("role id")
                print(i.id)
                break
            roles.append(i)
        if not already:
            roles.append(guild.get_role(715217084900180054))
            await member.edit(roles=roles)

        title = "Veteran Verification for `Cults Only` Complete"
        description = "Check " + client.get_channel(self.vet_rules).mention + " as veteran rules differ from its regular counterpart"
        await self.message.channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description}))
        return
        


class KeyReact:
    def __init__(self, payload):
        self.payload = payload
    async def run(self):
        payload, user = self.payload, self.payload.member
        if (str(payload.emoji) == "✅"):
            vet_db_list = ["cults-only", "vet-verify", str(user.id)]
            verify_status = pyc.get_item(vet_db_list + ["status"])
            if verify_status is None:
                pyc.child(vet_db_list).set({
                    "status": "pending"
                })

            if (user.dm_channel is None):
                await user.create_dm()
            title = "Verification for Veteran Runs for `Cults Only`"
            description = "Once your realmeye settings are set, type `.nexal verify <Realmeye IGN>`\n\nie. `.nexal verify MeApollo`"
            await user.dm_channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description}))
            return
        if (str(payload.emoji) == "❌"):
            isVet = False
            roles = []
            member = user.guild
            for i in member.roles:
                if (i.name == "Veteran Raider"):
                    isVet = i
                    print(i.id)
                    break
                else:
                    roles.append(i)
            if not isVet:
                return
            await member.edit(roles=roles)

            if (user.dm_channel is None):
                await user.create_dm()
            title = "You are no longer a veteran raider in `Cults Only`"
            description = "If you ever want to re-apply, you know how!"
            await user.dm_channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description}))
            return
        return True

