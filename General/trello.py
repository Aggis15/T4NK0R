import discord
from discord.commands import slash_command, Option
from discord.ext import commands
import logging
import json
import requests as r
import os
from dotenv import load_dotenv

load_dotenv()

# Logging
logging.basicConfig(filename='./logs/discordlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initiate json
file = open("config.json")
data = json.load(file)

# Public vars
TRELLO_KEY = os.environ.get("TRELLO_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")
guildID = data["guildID"][0]
trelloURL = data["trelloAPI"]["trelloAPIURL"]
trelloBugListID = data["trelloAPI"]["trelloBugListID"]
trelloFeatureListID = data["trelloAPI"]["trelloFeatureListID"]

class Trello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='Report a bug to the developers.', guild_ids=[guildID])
    async def reportbug(self, ctx, title: Option(str, "Bug title. Must be descriptive but not long", required=True),
                        description: Option(str,
                                            "Please go in detail about what the bug is. You are free to attach links with screenshots (Imgur)",
                                            required=True)):
        await ctx.respond("Processing report. Please wait...")
        query = {
            "idList": trelloBugListID,
            "name": title,
            "desc": description,
            "pos": "top"

        }
        createCard = r.post(f"{trelloURL}?key={TRELLO_KEY}&token={TRELLO_TOKEN}", json=query, headers={"Accept": "application/json"})
        trelloCardID = createCard.json()
        trelloCardID = json.dumps(trelloCardID)
        trelloCardID = json.loads(trelloCardID)
        trelloCardID = (trelloCardID["id"])
        await ctx.respond(f"Bug report submitted with ID: {trelloCardID}. You can find it [here](https://trello.com/c/{trelloCardID})!")

    @slash_command(aliases=['bug'], description='Report a bug to the developers.', guild_ids=[guildID])
    async def newfeature(self, ctx, title: Option(str, "New feature title. Must be descriptive but not long", required=True),
                        description: Option(str,
                                            "Please go in detail about what the new feature is. Please go in detail for this.",
                                            required=True)):
        await ctx.respond("Processing report. Please wait...")
        query = {
            "idList": trelloFeatureListID,
            "name": title,
            "desc": description,
            "pos": "top"

        }
        createCard = r.post(f"{trelloURL}?key={TRELLO_KEY}&token={TRELLO_TOKEN}", json=query,
                            headers={"Accept": "application/json"})
        trelloCardID = createCard.json()
        trelloCardID = json.dumps(trelloCardID)
        trelloCardID = json.loads(trelloCardID)
        trelloCardID = (trelloCardID["id"])
        await ctx.respond(
            f"Bug report submitted with ID: {trelloCardID}. You can find it [here](https://trello.com/c/{trelloCardID})!")



def setup(bot):
    bot.add_cog(Trello(bot))