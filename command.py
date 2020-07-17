import discord, json, os, pyrebase

def create_embed(type_="DEFAULT", fields={}):
    embed_dict = {
        "title": discord.Embed.Empty,
        "description": discord.Embed.Empty,
        "url": discord.Embed.Empty,
        "color": discord.Embed.Empty,
        "timestamp": discord.Embed.Empty,
        "footer": discord.Embed.Empty,
        "thumbnail": discord.Embed.Empty,
        "image": discord.Embed.Empty,
        "author": discord.Embed.Empty,
        "fields": discord.Embed.Empty,
    }

    if (type_ == "DEFAULT"):
        pass
    if (type_ == "BASIC"):
        embed_dict["color"] = 5290571
    if (type_ == "ERROR"):
        embed_dict["color"] = 15861040
    if (type_ == "HELP-MENU"):
        embed_dict["color"] = 6567912
    if (type_ == "REPLY"):
        embed_dict["color"] = 8051163
    if (type_ == "DM"):
        embed_dict["color"] = 6116280
    
    for i in fields:
        embed_dict[i] = fields[i]

    embed = discord.Embed(title=embed_dict["title"], description=embed_dict["description"], url=embed_dict["url"],
        color=embed_dict["color"], timestamp=embed_dict["timestamp"])
    
    if (embed_dict["footer"] != discord.Embed.Empty):
        print("oop")
        for i in ["text", "icon_url"]:
            embed_dict["footer"][i] = discord.Embed.Empty if embed_dict["footer"].get(i) is None else embed_dict["footer"][i]
        embed.set_footer(text=embed_dict["footer"]["text"], icon_url=embed_dict["footer"]["icon_url"])
    if (embed_dict["image"] != discord.Embed.Empty):
        for i in ["url"]:
            embed_dict["image"][i] = discord.Embed.Empty if embed_dict["image"].get(i) is None else embed_dict["image"][i]
        embed.set_image(url=embed_dict["image"]["url"])
    if (embed_dict["thumbnail"] != discord.Embed.Empty):
        for i in ["url"]:
            embed_dict["thumbnail"][i] = discord.Embed.Empty if embed_dict["thumbnail"].get(i) is None else embed_dict["thumbnail"][i]
        embed.set_thumbnail(url=embed_dict["thumbnail"]["url"])
    if (embed_dict["author"] != discord.Embed.Empty):
        for i in ["name", "url", "icon_url"]:
            embed_dict["author"][i] = discord.Embed.Empty if embed_dict["author"].get(i) is None else embed_dict["author"][i]
        embed.set_author(name=embed_dict["author"]["name"], url=embed_dict["author"]["url"], icon_url=embed_dict["author"]["icon_url"])
    if (embed_dict["fields"] != discord.Embed.Empty):
        for i in range(len(embed_dict["fields"])):
            for j in ["name", "value"]:
                embed_dict["fields"][i][j] = discord.Embed.Empty if embed_dict["fields"][i].get(j) is None else embed_dict["fields"][i][j]
            embed_dict["fields"][i]["inline"] = True if embed_dict["fields"][i].get("inline") is None else embed_dict["fields"][i]["inline"]
            embed.add_field(name=embed_dict["fields"][i]["name"], value=embed_dict["fields"][i]["value"], inline=embed_dict["fields"][i]["inline"])
    
    return embed

async def send_help_message(channel, message=None, embed=None):
    await channel.send(message, embed=embed)

class Command():
    def __init__(self, message, message_keys):
        self.message = message
        self.message_keys = message_keys
        self.help_text = ""

        self.value = ""
        
class SuperCommand(Command):
    def __init__(self, message, message_keys):
        super().__init__(message, message_keys)

class PyrebaseCommands():
    def __init__(self, database):
        self.db = database
    def search(self, item, childs):
        db = self.db
        for i in childs:
            db = db.child(i)
        temp = db.shallow().get().val()
        if temp is None:
            return None
        return item in temp
    def search_val(self, item, childs):
        db = self.db
        for i in childs:
            db = db.child(i)
        temp = db.get().val()
        if temp is None:
            return None
        return item in temp
    def child(self, childs):
        db = self.db
        for i in childs:
            db = db.child(i)
        return db
    def get_item(self, childs, if_none=None):
        data = self.child(childs).get().val()
        if data is None:
            return if_none
        return data

class Variables():
    def __init__(self):
        self.types = ["c", "v", "st", "e", "x"]
        try:
            with open("data/pyrebase-config.json") as f:
                self.pyrebase_config = json.load(f)
        except:
            self.pyrebase_config = {
                "apiKey": os.environ["PYREBASE_API_KEY"],
                "authDomain": os.environ["PYREBASE_AUTH_DOMAIN"],
                "databaseURL": os.environ["PYREBASE_DATABASE_URL"],
                "storageBucket": os.environ["PYREBASE_STORAGE_BUCKET"],
                "serviceAccount": "data/pyrebase-credentials.json"
            }
            with open(self.pyrebase_config["serviceAccount"], "w") as f:
                json.dump({
                    "type": "service_account",
                    "project_id": "nexal-discord-bot",
                    "private_key_id": os.environ["PYREBASE_PRIVATE_KEY_ID"],
                    "private_key": os.environ["PYREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
                    "client_email": os.environ["PYREBASE_CLIENT_EMAIL"],
                    "client_id": os.environ["PYREBASE_CLIENT_ID"],
                    "auth_uri": os.environ["PYREBASE_AUTH_URI"],
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.environ["PYREBASE_CLIENT_X509_CERT_URL"]
                }, f)
        
        self.db = pyrebase.initialize_app(self.pyrebase_config).database()

    async def not_nexal_admin_speech(self, channel, member):
        title = "Permission Error"
        description = "You need nexal admin permissions to run this command!"
        await channel.send(member.mention, embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))

    def get_role(self, guild, role_name):
        role = None
        for i in guild.roles:
            if (i.name == role_name):
                role = i
        return role

    def cleanse_mention(self, name):
        real_name = ""
        for i in name:
            if i in "1234567890":
                real_name += i
        return real_name


vars = Variables()
pyc = PyrebaseCommands(vars.db)

try:
    with open("bot_token.txt") as f:
        DISCORD_TOKEN = f.read()
except:
    DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

client = discord.Client()

