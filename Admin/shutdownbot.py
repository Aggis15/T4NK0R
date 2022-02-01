import sys
from discord.ext import commands
from discord.commands import slash_command, permissions
import json

import logging

# Initiate json
file = open("config.json")
data = json.load(file)

# Logging
logging.basicConfig(filename='logs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Public vars
guildID = data["guildID"][0]
T4NK0RStaff = data["roleIDs"]["T4NK0RStaff"]
warningTSE = data["emojiIDs"]["warningTSE"]


class rebootBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[guildID], description="Reboots the bot. Quite dangerous!")
    @permissions.has_role(T4NK0RStaff)
    async def shutdownbot(self, ctx):
        await ctx.respond(f"{warningTSE} This is a dangerous command to execute. Please be aware that if you use this, you must manually turn the bot on again. If you are sure about this, type '**Yes, I agree to killing the bot!**'. You have 20 seconds, starting now.{warningTSE}")

        def check(author):
            def inner_check(message):
                return message.author == author
            return inner_check

        verification = await self.bot.wait_for("message", check=check(ctx.author), timeout=20)
        if verification.content == "Yes, I agree to killing the bot!":
            await ctx.respond("Bot is dying. Goodbye.")
            sys.exit()

def setup(bot):
    bot.add_cog(rebootBot(bot))
