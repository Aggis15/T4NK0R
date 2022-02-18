import os
import asyncpg
from discord.commands import slash_command, Option
from discord.ext import commands
import logging
import json

# Logging
logging.basicConfig(filename='logs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Public Variables
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
TABLE_NAME = os.environ.get("TABLE_NAME")


# Initiate json
file = open("config.json")
data = json.load(file)
guildID = data["guildID"][0]


class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Turn bot notifications on or off! Default is on!", guild_ids=[guildID])
    async def notifications(self, ctx, value: Option(str, "Make your choice!", choices=["on", "off"])):
        conn = await asyncpg.connect(f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        if value == "off":
            await conn.execute(f"UPDATE {TABLE_NAME} SET doNotify = false WHERE userid = {ctx.author.id}")
        else:
            await conn.execute(f"UPDATE {TABLE_NAME} SET doNotify = true WHERE userid = {ctx.author.id}")
        await ctx.respond(f"Notifications have now been turned {value}")
        await conn.close()
        logger.info(f"{ctx.author.name} turned their notifications {value}!")

    @notifications.error
    async def notifications_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(Notifications(bot))
