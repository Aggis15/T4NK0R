import logging
from datetime import date
import discord
from discord.ext import commands
import json

# Initiate json
file = open("config.json")
data = json.load(file)

# Logging
logging.basicConfig(filename='./logs/discordlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global variables
deepthinkersRole = data["roleIDs"]["deepthinkers"]
lockdownRole = data["roleIDs"]["lockdown"]
notifiedLiveRole = data["roleIDs"]["notifiedLive"]
eventsRole = data["roleIDs"]["events"]
gamersRole = data["roleIDs"]["gamers"]
votersRole = data["roleIDs"]["voters"]


class reactionListener(commands.Cog, name="Reaction Listener"):
    def __init__(self, bot):
        self.bot = bot

    # When someone leaves, log it
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 946903095097569330:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if payload.emoji.name == "Pentagram":
                role = discord.utils.find(lambda r: r.id == deepthinkersRole, guild.roles)
                if role in member.roles:
                    return
                else:
                    await member.add_roles(discord.Object(id=deepthinkersRole))
                    await member.send("You have been added to the Deep Thinkers role!")
                    logger.info(f"{member} has been added to the Deep Thinkers role!")
            elif payload.emoji.name == "TSELockdown":
                role = discord.utils.find(lambda r: r.id == lockdownRole, guild.roles)
                if role in member.roles:
                    return
                else:
                    await member.add_roles(discord.Object(id=lockdownRole))
                    await member.send("You have been added to the Lockdown role!")
                    logger.info(f"{member} has been added to the Lockdown role!")
            elif payload.emoji.name == "TSEWarning":
                role = discord.utils.find(lambda r: r.id == notifiedLiveRole, guild.roles)
                if role in member.roles:
                    return
                else:
                    await member.add_roles(discord.Object(id=notifiedLiveRole))
                    await member.send("You have been added to the Notified Live role!")
                    logger.info(f"{member} has been added to the Notified Live role!")
            elif payload.emoji.name == "BWEvents":
                role = discord.utils.find(lambda r: r.id == eventsRole, guild.roles)
                if role in member.roles:
                    return
                else:
                    await member.add_roles(discord.Object(id=eventsRole))
                    await member.send("You have been added to the Events role!")
                    logger.info(f"{member} has been added to the Events role!")
            elif payload.emoji.name == "Aces":
                role = discord.utils.find(lambda r: r.id == gamersRole, guild.roles)
                if role in member.roles:
                    return
                else:
                    await member.add_roles(discord.Object(id=gamersRole))
                    await member.send("You have been added to the Gamers role!")
                    logger.info(f"{member} has been added to the Gamers role!")
            elif payload.emoji.name == "VFive":
                role = discord.utils.find(lambda r: r.id == votersRole, guild.roles)
                if role in member.roles:
                    return
                else:
                    await member.add_roles(discord.Object(id=votersRole))
                    await member.send("You have been added to the Voters role!")
                    logger.info(f"{member} has been added to the Voters role!")
            else:
                return

def setup(bot):
    bot.add_cog(reactionListener(bot))
