import logging
from datetime import date
import discord
from discord.ext import commands
import json

# Initiate json
file = open("config.json")
data = json.load(file)

# Logging
logging.basicConfig(
    filename="./logs/discordlogs.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Public Vars
date = date.today()
dateToday = date.strftime("%m-%d-%Y")

# Public vars
leaveChat = data["channelIDs"]["leaveChat"]


class LeaveListener(commands.Cog, name="Leave Listener"):
    def __init__(self, bot):
        self.bot = bot
        self.leaveChatChannel = bot.get_channel(leaveChat)

    # When someone leaves, log it
    @commands.Cog.listener()
    async def on_member_leave(self, member):
        embed = discord.Embed(
            title="Member left",
            description=f"{member.mention} has left the server. RIP.",
            color=discord.Color.red(),
        )
        embed.set_footer(text=f"Member ID: {member.id} • Date: {dateToday}")
        await self.leaveChatChannel.send(embed=embed)
        logger.info(f"{member.name} with ID: {member.id} has left the server!")


def setup(bot):
    bot.add_cog(LeaveListener(bot))
