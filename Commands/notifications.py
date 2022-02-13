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
dbHost = os.environ.get("dbHost")
dbUser = os.environ.get("dbUser")
dbPass = os.environ.get("dbPass")
dbName = os.environ.get("dbName")
dbPort = os.environ.get("dbPort")
tableName = os.environ.get("tableName")


# Initiate json
file = open("config.json")
data = json.load(file)
guildID = data["guildID"][0]


class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Turn bot notifications on or off! Default is on!", guild_ids=[guildID])
    async def notifications(self, ctx, value: Option(str, "Make your choice!", choices=["on", "off"])):
        conn = await asyncpg.create_pool(f'postgres://{dbUser}:{dbPass}@{dbHost}:{dbPort}/{dbName}')
        if value == "off":
            await conn.execute(f"UPDATE {tableName} SET doNotify = false WHERE userid = {ctx.author.id}")
        else:
            await conn.execute(f"UPDATE {tableName} SET doNotify = true WHERE userid = {ctx.author.id}")
        await ctx.respond(f"Notifications have now been turned {value}")
        await conn.close()
        logger.info(f"{ctx.author.name} turned their notifications {value}!")

    @notifications.error
    async def notifications_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(Notifications(bot))
