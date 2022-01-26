import asyncio
import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, Option, permissions
import json
import random as r
import logging

# Initiate json
file = open("config.json")
data = json.load(file)

# Logging
logging.basicConfig(filename='logs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Public vars
statuses = data["Statuses"]
statusName = r.choice(statuses)
guildID = data["guildID"][0]
T4NK0RStaff = data["roleIDs"]["T4NK0RStaff"]

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statusloop.start()

    @tasks.loop(hours=4.0)
    async def statusloop(self):
        await self.bot.change_presence(activity=discord.Game(name=statusName))
        logger.info(f"Status changed to {statusName}")

    @statusloop.before_loop
    async def beforeStatusLoop(self):
        logger.info("Waiting before starting status loop.")
        await self.bot.wait_until_ready()

    @slash_command(guild_ids=[guildID], description="A way to change the status on the bot! Usable only by staff.")
    @permissions.has_role(T4NK0RStaff)
    async def changestatus(self, ctx, status: Option(str, description="Your status name", default=statusName), time: Option(int, required=False, description="How long the status should last, in seconds. Default is 4 hours.", default=4)):
        self.statusloop.cancel()
        await self.bot.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(float(time))
        await self.statusloop.start()


def setup(bot):
    bot.add_cog(Status(bot))
