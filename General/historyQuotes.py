import logging
from discord.ext import commands
from discord.commands import slash_command
import json
import random as r

# Logging
logging.basicConfig(filename='./logs/discordlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initiate json
file = open("config.json")
data = json.load(file)

# Public variables
guildID = data["guildID"][0]


class historyQuote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quote = data["quotes"]

    @slash_command(guild_ids=[guildID], description="A command to show a famous quote StarDelivery has said!")
    async def historyquote(self, ctx):
        statusName = r.choice(self.quote)
        await ctx.respond(f"Here's one! \n{statusName}")

        logger.info(f"{ctx.author.name} has requested a quote!")

def setup(bot):
    bot.add_cog(historyQuote(bot))
