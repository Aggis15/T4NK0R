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
logging.basicConfig(filename='./logs/discordlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Public variables
guildID = data["guildID"][0]
T4NK0RStaff = data["roleIDs"]["T4NK0RStaff"]
statuses = data["statuses"]


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statusloop.start()

    @tasks.loop(hours=1.0)
    async def statusloop(self):
        statusName = r.choice(statuses)
        await self.bot.change_presence(activity=discord.Game(name=statusName))
        logger.info(f"Status changed to '{statusName}'")

    @statusloop.before_loop
    async def beforeStatusLoop(self):
        logger.info("Waiting before starting status loop.")
        await self.bot.wait_until_ready()

    @slash_command(guild_ids=[guildID], description="A way to change the status on the bot! Usable only by staff.")
    @permissions.has_role(T4NK0RStaff)
    async def changestatus(self, ctx, status: Option(str, description="Your status name", required=False), time: Option(int, required=False, description="How long the status should last, in seconds. Default is 4 hours.", default=14400)):
        if status is None:
            status = r.choice(statuses)
        if self.statusloop.is_running() is True:
            self.statusloop.cancel()
            await self.bot.change_presence(activity=discord.Game(name=status))
            await ctx.respond(f"Status has been successfully changed to {status} for {time} seconds!")
            await asyncio.sleep(float(time))
            await self.statusloop.start()
        else:
            await ctx.respond(f"Status change is already in progress.")

    @statusloop.error
    async def statusloop_error(self, ctx, error):
        await ctx.respond(f"`{error}`")

def setup(bot):
    bot.add_cog(Status(bot))
