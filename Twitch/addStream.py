import asyncio

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
logging.basicConfig(filename='./logs/discordlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Public variables
TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')
TWITCH_ACCESS_TOKEN = os.environ.get('TWITCH_ACCESS_TOKEN')
TWITCH_SECRET = os.environ.get('TWITCH_SECRET')
guildID = data["guildID"][0]
T4NK0RStaff = data["roleIDs"]["T4NK0RStaff"]


class addStream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[guildID], description="Add a stream to the notification list!")
    @permissions.has_role(T4NK0RStaff)
    async def addstream(self, ctx, userid: Option(str, "Enter the ID. Find it with getuserid", required=True)):
        await ctx.respond("Adding stream... More information will be provided shortly.")
        headers = {"Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}", "Content-Type": "application/json"}
        info_json = {
            "type": "stream.online",
            "version": "1",
            "condition": {
                "broadcaster_user_id": userid
            },
            "transport": {
                "method": "WEBHOOK_URL",
                "callback": "https://2b64-91-132-132-53.ngrok.io/twitch/live",
                "secret": TWITCH_SECRET}
        }
        r.post("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers, json=info_json)
        await asyncio.sleep(10)
        req = r.get("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers)
        req = req.json()
        if req["data"][-1]["status"] == "enabled":
            await ctx.respond("Stream added!")
        else:
            await ctx.respond("Stream not added! Please try again.")

    @addstream.error
    async def addstream_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(addStream(bot))