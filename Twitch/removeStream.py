from discord.ext import commands
from discord.commands import slash_command, Option, permissions
import json
import os
from dotenv import load_dotenv
import logging
import requests as r
load_dotenv()
# Initiate json
file = open("config.json")
data = json.load(file)

# Logging
logging.basicConfig(filename='logs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Public vars
twitchClientID = os.environ.get('twitchClientID')
twitchClientSecret = os.environ.get('twitchClientSecret')
twitchAccessToken = os.environ.get('twitchAccessToken')
guildID = data["guildID"][0]
T4NK0RStaff = data["roleIDs"]["T4NK0RStaff"]

class removeStream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[guildID], description="Remove a stream from the notification list!")
    @permissions.has_role(T4NK0RStaff)
    async def removestream(self, ctx, requestid=Option(str, "Enter the user ID. Find it with the getuserid command", required=True)):
        headers = {"Client-ID": twitchClientID, "Authorization": f"Bearer {twitchAccessToken}", "Content-Type": "application/json"}
        r.delete(f"https://api.twitch.tv/helix/eventsub/subscriptions?id={requestid}", headers=headers)
        get_stream_request = r.get("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers)
        await ctx.respond(f"```{get_stream_request.text}```")
        logging.info(f"Stream removed from notification list by {ctx.author.name}" )


def setup(bot):
    bot.add_cog(removeStream(bot))
