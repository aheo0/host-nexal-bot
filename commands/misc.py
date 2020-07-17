from command import *
import json, pyrebase, asyncio

class DeathCount(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def incorrectCommand(self):
        title = "Incorrect Command"
        description = "Type `.nexal deathcount -h` to see how to use the command"
        await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description": description}))
        return


    async def add(self, message_keys):
        if (len(message_keys) < 2):
            await self.incorrectCommand()
            return
        killer = message_keys[0][3:-1]
        dead = [i[3:-1] for i in message_keys[1:]]

        current_dead = pyc.get_item([str(self.message.guild.id), "death-count", killer], {})
        for i in dead:
            temp = 1
            if i in current_dead:
                temp += current_dead[i]
            pyc.child([str(self.message.guild.id), "death-count", killer, i]).set(temp)

        title = str(len(dead)) + " Kills Logged"
        description = "Congratz on the following kills:"
        guild = self.message.guild
        fields = [{"name": guild.get_member(int(i)).nick, "value": guild.get_member(int(i)).mention, "inline": False} for i in dead]
        await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description": description, "fields": fields}))
        return

    async def list(self, message_keys):
        if (len(message_keys) < 1):
            await self.incorrectCommand()
            return
        killer = message_keys[0][3:-1]
        current_dead = pyc.get_item([str(self.message.guild.id), "death-count", killer], {})

        total_deaths = 0
        for i in current_dead:
            total_deaths += current_dead[i]

        killer_member = self.message.guild.get_member(int(killer))
        title = str(killer_member.nick) + " has " + str(total_deaths) + " Kills Logged"
        description = "Congratz on the following kills " + killer_member.mention + ":"
        guild = self.message.guild
        fields = [{"name": guild.get_member(int(i)).nick, "value": guild.get_member(int(i)).mention + " " + str(current_dead[i]), "inline": False} for i in current_dead]
        await self.message.channel.send(embed=create_embed(type_="REPLY", fields={"title": title, "description": description, "fields": fields}))
        return


    async def help(self):
        return


    async def run(self):
        if (len(self.message_keys) == 0):
            return
        if (self.message_keys[0] == "add"):
            await self.add(self.message_keys[1:])
            return
        if (self.message_keys[0] == "list"):
            await self.list(self.message_keys[1:])
            return
        if (self.message_keys[0] == "-h"):
            await self.help()
            return
