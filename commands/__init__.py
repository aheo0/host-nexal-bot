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

        # Check Bot Command Channel
        if (pyc.search(str(self.message.guild.id), []) and \
            not pyc.search_val(str(self.message.channel.id), [str(self.message.guild.id), "bcs"])):
            return

        # Help
        if (self.message_keys[0] == "ping"):
            await help.Ping(self.message, self.message_keys[1:]).run()
            return
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
        if (self.message_keys[0] == "vet-vcs"):
            await config.VetVCS(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "rsa"):
            await config.RSA(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "vet-rsa"):
            await config.VRSA(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "event-rsa"):
            await config.ERSA(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "lng"):
            await config.LNG(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "vet-lng"):
            await config.VLNG(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "event-lng"):
            await config.ELNG(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "role"):
            await config.Role(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "type"):
            await config.Type(self.message, self.message_keys[1:]).run()
            return
        
        # AFK
        if (self.message_keys[0] == "hc"):
            await afk.Hc(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "afk"):
            await afk.Afk(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "abortafk"):
            await afk.Abortafk(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "endafk"):
            await afk.Endafk(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "logkeys"):
            await afk.Logkeys(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "runlogs"):
            await afk.Runlogs(self.message, self.message_keys[1:]).run()
            return

        # Parse
        if (self.message_keys[0] == "parse"):
            await parse.Parse(self.message, self.message_keys[1:]).run()
            return

        # TRL Feedback
        if (self.message_keys[0] == "trl-feedback"):
            await trl_feedback.TrlFeedback().run(self.message, self.message_keys[1:])
            return

        # Misc
        if (self.message_keys[0] == "deathcount"):
            await misc.DeathCount(self.message, self.message_keys[1:]).run()
            return

    async def dms(self):
        #####
        # Special
        #####
        # - # Cults Only (715217084900180048)
        if (str(self.message.channel.type) == "private"):
            # Vet Verify
            if (len(self.message_keys) > 0 and self.message_keys[0] == "verify"):
                await cults_only.VetVerify(self.message, self.message_keys[1:]).run()
                return

    async def reaction(self, reaction, user):
        try:
            react = await afk.KeyReact(reaction, user).run()
        except:
            react = False
        if not react:
            try:
                react = await trl_feedback.TrlFeedback().KeyReact(reaction, user)
            except:
                react = False
        
    async def raw_reaction(self, payload):
        if (payload.message_id == 733141028197892179):
            react = await cults_only.KeyReact(payload).run()