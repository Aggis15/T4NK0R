import logging
from discord.ext import commands
from discord.commands import slash_command, Option, permissions
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
twitchClientID = os.environ.get('twitchClientID')
twitchClientSecret = os.environ.get('twitchClientSecret')
twitchAccessToken = os.environ.get('twitchAccessToken')
T4NK0RStaff = data["roleIDs"]["T4NK0RStaff"]
guildID = data["guildID"][0]


class getUserID(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[guildID], description="Get the user ID of a Twitch user. Useful for adding streams.")
    @permissions.has_role(T4NK0RStaff)
    async def getuserid(self, ctx, user: Option(str, "Enter the username", required=True)):
        headers = {"Client-ID": twitchClientID, "Authorization": f"Bearer {twitchAccessToken}"}
        req = r.get(f"https://api.twitch.tv/helix/users?login={user}", headers=headers)
        req = json.loads(req.text)
        userID = req["data"][0]["id"]
        await ctx.respond(f"{user}'s ID is {userID}")
        logger.info(f"{ctx.author} used getuserid command for {user}")

    @getuserid.error
    async def getuserid_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(getUserID(bot))
