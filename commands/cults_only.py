from command import *
import aiohttp

class VetVerify:
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)
    
    async def run(self):
        CULT_COUNT = 50
        
        if (len(self.message_keys) == 0):
            pass


class KeyReact:
    def __init__(self, reaction, user):
        self.reaction = reaction
        self.user = user
    async def run(self):
        reaction, user = self.reaction, self.user
        if (str(reaction.emoji) == "✅" and reaction.message.id == 732824777223307374):
            vet_db_list = ["cults-only", "vet-verify", str(user.id)]
            verify_status = pyc.get_item(vet_db_list + ["status"])
            if verify_status is None:
                pyc.child(vet_db_list).set({
                    "status": "pending"
                })
            if (verify_status == "completed"):
                return

            if (user.dm_channel is None):
                await user.create_dm()
            title = "Verification for Veteran Runs for `Cults Only`"
            description = "Once your realmeye settings are set, type `.nexal verify <Realmeye IGN>`\n\nie. `.nexal verify MeApollo`"
            await user.dm_channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description}))
            return
        if (str(reaction.emoji) == "❌" and reaction.message.id == 732824777223307374):
            vet_db_list = ["cults-only", "vet-verify", str(user.id)]
            verify_status = pyc.get_item(vet_db_list + ["status"])
            if (verify_status == "completed"):
                return

            if (user.dm_channel is None):
                await user.create_dm()
            title = "Verification for Veteran Runs for `Cults Only`"
            description = "Once your realmeye settings are set, type `.nexal verify <Realmeye IGN>`\n\nie. `.nexal verify MeApollo`"
            await user.dm_channel.send(embed=create_embed(type_="DM", fields={"title": title, "description": description}))
        return True


