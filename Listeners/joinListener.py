import logging
from datetime import date
import discord
from discord.ext import commands
import json

# Logging
logging.basicConfig(filename='./logs/discordlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initiate json
file = open("config.json")
data = json.load(file)

# Public Variables
generalChat = data["channelIDs"]["generalChat"]
announcementsChat = data["channelIDs"]["announcementsChat"]
rulesChat = data["channelIDs"]["rulesChat"]
membersJoinedChat = data["channelIDs"]["membersJoinedChat"]
visitorRole = data["roleIDs"]["visitorRole"]


class JoinListener(commands.Cog, name="Join Listener"):
    def __init__(self, bot):
        self.bot = bot
        self.generalChatChannel = bot.get_channel(generalChat)
        self.announcementsChatChannel = bot.get_channel(announcementsChat)
        self.rulesChatChannel = bot.get_channel(rulesChat)
        self.membersJoinedChatChannel = bot.get_channel(membersJoinedChat)

    # When someone joins, welcome them in General Chat
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="New Member!",
            description=f"Welcome to **The Star Empire** {member.name}. Please go ahead and read the rules at {self.rulesChatChannel.mention}. {self.announcementsChatChannel.mention} is also a very important channel, which is where star is gonna be posting regular updates about the server. We hope you enjoy your stay! ",
            color=discord.Color.red()
        )
        embed.set_footer(text="The Star Empire!")

        # Assign the Visitor role
        await member.add_roles(discord.Object(id=visitorRole))
        await self.generalChatChannel.send(member.mention, embed=embed)

        # Log the entrance in members joined channel
        join_embed = discord.Embed(
            title="Member joined!",
            description=f"{member.mention} has joined the server!",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Member ID: {member.id} • Date: {date}")
        await self.membersJoinedChatChannel.send(embed=join_embed)
        logger.info(f"{member.name} with ID: {member.id} has joined the server!")

def setup(bot):
    bot.add_cog(JoinListener(bot))
