import os
import asyncpg
import discord
from discord.commands import slash_command, Option
from discord.ext import commands
import logging
import json

# Logging
logging.basicConfig(
    filename="./logs/discordlogs.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Public Variables
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
LEVEL_TABLE_NAME = os.environ.get("LEVEL_TABLE_NAME")


# Initiate json
file = open("config.json")
data = json.load(file)
guildID = data["guildID"][0]
T4NK0RStaff = data["roleIDs"]["T4NK0RStaff"]


class OverrideLevel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        description="Turn bot notifications on or off! Default is on!",
        guild_ids=[guildID],
    )
    async def overridelevel(
        self,
        ctx,
        member: Option(
            discord.Member,
            "Select the member you want to make changes to!",
            required=True,
        ),
        levelname: Option(
            str,
            "Enter the level name you want to apply! Leave blank if you want to disable override",
            required=False,
        ),
    ):
        conn = await asyncpg.connect(
            f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        doOverride = await conn.fetchval(
            f"SELECT dooverridelevelname FROM {LEVEL_TABLE_NAME} WHERE userid = {member.id}"
        )
        level = await conn.execute(
            f"SELECT currentlevel FROM {LEVEL_TABLE_NAME} WHERE userid = {member.id}"
        )
        role = discord.utils.find(lambda r: r.name == T4NK0RStaff, ctx.guild.roles)
        if role in member.roles or int(level) >= 500:
            if doOverride:
                if levelname is None:
                    await conn.execute(
                        f"UPDATE {LEVEL_TABLE_NAME} SET dooverridelevelname = FALSE, overridelevelname = NULL WHERE userid = {member.id}"
                    )
                    await ctx.respond(f"{member.name}'s override has been disabled!")
                else:
                    await conn.execute(
                        f"UPDATE {LEVEL_TABLE_NAME} SET overridelevelname = '{levelname}' WHERE userid = {member.id}"
                    )
                    await ctx.respond(
                        f"Override level name set as '{levelname}' for user '{member.name}'!"
                    )
            else:
                if levelname is None:
                    await ctx.respond("You must enter a level name to enable override!")
                else:
                    await conn.execute(
                        f"UPDATE {LEVEL_TABLE_NAME} SET dooverridelevelname = TRUE, overridelevelname = '{levelname}' WHERE userid = {member.id}"
                    )
                    await ctx.respond(
                        f"Override level name set as '{levelname}' for user '{member.name}'!"
                    )
        await conn.close()

        logger.info(
            f"{ctx.author.name} has overriden the level name for user {member.name} with level name '{levelname}'!"
        )

    @overridelevel.error
    async def override_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(OverrideLevel(bot))
