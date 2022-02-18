import os
import asyncpg
import discord
from discord.commands import slash_command
from discord.ext import commands
import logging
import json

# Logging
logging.basicConfig(filename='logs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initiate json
file = open("config.json")
data = json.load(file)
guildID = data["guildID"][0]

# Public variables
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
TABLE_NAME = os.environ.get("TABLE_NAME")


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Show the level leaderboard!", guild_ids=[guildID])
    async def leaderboard(self, ctx):
        conn = await asyncpg.connect(f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        global embed
        res = await conn.fetch(f"SELECT username, currentxp, currentlevel FROM {TABLE_NAME} ORDER BY currentxp DESC")
        nameList = []
        xpList = []
        levelList = []
        counter = 0
        embed = discord.Embed(title="Server Leaderboard", description="**# • Name • XP • Level**", color=discord.Color.blue())
        for people in res:
            name = people[0]
            xp = people[1]
            level = people[2]
            nameList.append(name)
            xpList.append(xp)
            levelList.append(level)
            counter = counter + 1
            embed.add_field(name="\u200b", value=f"#{counter} • {name} • {xp} • {level}", inline=False)
        await ctx.respond(embed=embed)
        await conn.close()

    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(Leaderboard(bot))
