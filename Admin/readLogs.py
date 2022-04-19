import discord
from discord.ext import commands
from discord.commands import slash_command, permissions
import json

# Initiate json
file = open("config.json")
data = json.load(file)

# Public Variables
T4NK0RStaff = data["roleIDs"]["T4NK0RStaff"]
guildID = data["guildID"][0]


class ReadLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        guild_ids=[guildID],
        description="Get a copy of the log file. Useful for troubleshooting",
    )
    @permissions.has_role(T4NK0RStaff)
    async def readlogs(self, ctx):
        await ctx.respond(file=discord.File("./logs/discordlogs.log"))

    @readlogs.error
    async def readlogs_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(ReadLogs(bot))
