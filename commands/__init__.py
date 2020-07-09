import os, glob
modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if os.path.isfile(f) and not f.endswith("__init__.py")]
from . import *
from command import *

class Main(SuperCommand):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

    async def run(self):
        if (self.message_keys[0] == ""):
            pass
            return
        
        # Help
        if (self.message_keys[0] == "help"):
            await help.Help(self.message, self.message_keys[1:]).run()
            return
        
        # AFK
        if (self.message_keys[0] == "hc"):
            await afk.HC(self.message, self.message_keys[1:]).run()
            return
        if (self.message_keys[0] == "afk"):
            await afk.AFK(self.message, self.message_keys[1:]).run()
            return