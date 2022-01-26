from discord.commands import slash_command
from discord.ext import commands
import logging


# Logging
logging.basicConfig(filename='logs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Check the bot's ping!")
    async def ping(self, ctx):
        if self.bot.latency <= 150:
            await ctx.respond(f"Bot latency is `{round(self.bot.latency * 1000)}ms`. That's great!")
        else:
            await ctx.respond(f"Bot latency is `{round(self.bot.latency * 1000)}ms`. That's not so great!")
        logger.info(f"{ctx.author.name} with ID: {ctx.author.id} has checked the bot ping!")


def setup(bot):
    bot.add_cog(PingCommand(bot))
