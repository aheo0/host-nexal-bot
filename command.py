import discord, json

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

class Variables():
    def __init__(self):
        self.types = ["c", "v", "st", "e", "x"]

    def get_dir_path(self, guild_id):
        return("data/" + str(guild_id) + "/")

    def check_nexal_admin(self, guild_id, member_id):
        with open("data/guilds.json") as f:
            data = json.load(f)
        return member_id in data[str(guild_id)]["admins"]

    async def not_nexal_admin_speech(self, channel, member):
        title = "Permission Error"
        description = "You need nexal admin permissions to run this command!"
        await self.message.channel.send(embed=create_embed(type_="ERROR", fields={"title": title, "description": description}))

vars = Variables()