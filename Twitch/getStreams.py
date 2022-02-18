import logging
from discord.ext import commands
from discord.commands import slash_command, permissions
from dotenv import load_dotenv
import requests as r
import json
import os
load_dotenv()

# Initiate json
file = open("config.json")
data = json.load(file)

# Logging
logging.basicConfig(filename='logs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Public Variables
TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')
TWITCH_ACCESS_TOKEN = os.environ.get('TWITCH_ACCESS_TOKEN')
T4NK0RStaff = data["roleIDs"]["T4NK0RStaff"]
guildID = data["guildID"][0]


class getStreams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[guildID], description="Get the user ID of a Twitch user. Useful for adding streams.")
    @permissions.has_role(T4NK0RStaff)
    async def getstreams(self, ctx):
        endpoint = "https://api.twitch.tv/helix/eventsub/subscriptions"
        headers = {"Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}", "Content-Type": "application/json"}
        get_request = r.get(url=endpoint, headers=headers)
        await ctx.respond(f"```{get_request.text}```")
        logger.info(f"{ctx.author} used getstreams command")

    @getstreams.error
    async def getstreams_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(getStreams(bot))