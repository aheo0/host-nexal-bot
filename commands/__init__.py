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
        
        # Help
        if (self.message_keys[0] == "help"):
            await help.Help(self.message, self.message_keys[1:]).run()
            return

        NEXAL_ADMIN = vars.check_nexal_admin(self.message.guild.id, self.message.author.id)

        # Setup
        if NEXAL_ADMIN:
            if (self.message_keys[0] == "setup"):
                await setup.Setup(self.message, self.message_keys[1:]).run()
                return
            IS_BOT_SETUP = await setup.Setup(self.message, self.message_keys[1:]).check()
            if not IS_BOT_SETUP:
                return
            if (self.message_keys[0] == "delete-data"):
                await setup.Setup(self.message, self.message_keys[1:]).delete_data()
                return
        
        # AFK
        if (self.message_keys[0] == "hc"):
            await afk.Hc(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "afk"):
            await afk.Afk(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "endafk"):
            await afk.Endafk(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "endrun"):
            await afk.Endrun(self.message, self.message_keys[1:]).run()
            return

    async def reaction(self, reaction, user):
        await afk.KeyReact(reaction, user).run()