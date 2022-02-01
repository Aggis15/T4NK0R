import os
import psycopg2
import discord
from discord.commands import slash_command, Option
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

# Public vars
dbHost = os.environ.get("dbHost")
dbUser = os.environ.get("dbUser")
dbPass = os.environ.get("dbPass")
dbName = os.environ.get("dbName")
dbPort = os.environ.get("dbPort")
tableName = os.environ.get("tableName")
conn = psycopg2.connect(host=dbHost, database=dbName, user=dbUser, password=dbPass, port=dbPort)
cur = conn.cursor()


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Show the level leaderboard!", guild_ids=[guildID])
    async def leaderboard(self, ctx):
        global embed
        cur.execute(f"SELECT username, currentxp, currentlevel FROM {tableName} ORDER BY currentxp DESC")
        res = cur.fetchall()
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


def setup(bot):
    bot.add_cog(Leaderboard(bot))
