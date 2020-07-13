import os, glob
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if os.path.isfile(f) and not f.endswith("__init__.py")]
from . import *
from command import *

class Main(SuperCommand):
    def __init__(self, message=None, message_keys=None):
        super().__init__(message, message_keys)

    async def run(self):
        if (self.message_keys[0] == ""):
            pass
            return

        # Check Bot Command Channel
        with open("data/guilds.json") as f:
            data = json.load(f)
        if (str(self.message.guild.id) in data and self.message.channel.id not in data[str(self.message.guild.id)]["bcs"]):
            return
        
        # Help
        if (self.message_keys[0] == "help"):
            await help.Help(self.message, self.message_keys[1:]).run()
            return

        # Config
        if (self.message_keys[0] == "setup"):
            await config.Setup(self.message, self.message_keys[1:]).run()
            return
        IS_BOT_SETUP = await config.Setup(self.message, self.message_keys[1:]).check()
        if not IS_BOT_SETUP:
            return
        if (self.message_keys[0] == "delete-data"):
            await config.Setup(self.message, self.message_keys[1:]).delete_data()
            return
        if (self.message_keys[0] == "prefix"):
            await config.Prefix(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "admin"):
            await config.Admin(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "bcs"):
            await config.BCS(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "vcs"):
            await config.VCS(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "rsa"):
            await config.RSA(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "lng"):
            await config.LNG(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "role"):
            await config.Role(self.message, self.message_keys[1:]).run()
            return
        
        # AFK
        if (self.message_keys[0] == "type"):
            await afk.Type(self.message, self.message_keys[1:]).run()
            return
        #if (self.message_keys[0] == "hc"):
        #    await afk.Hc(self.message, self.message_keys[1:]).run()
        #    return
        #if (self.message_keys[0] == "afk"):
        #    await afk.Afk(self.message, self.message_keys[1:]).run()
        #    return
        #if (self.message_keys[0] == "endafk"):
        #    await afk.Endafk(self.message, self.message_keys[1:]).run()
        #    return
        #if (self.message_keys[0] == "endrun"):
        #    await afk.Endrun(self.message, self.message_keys[1:]).run()
        #    return

        # Parse
        if (self.message_keys[0] == "parse"):
            await parse.Parse(self.message, self.message_keys[1:]).run()
            return

    #async def reaction(self, reaction, user):
    #    await afk.KeyReact(reaction, user).run()