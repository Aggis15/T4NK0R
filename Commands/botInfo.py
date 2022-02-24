import discord
from discord.commands import slash_command
from discord.ext import commands
import logging
import json
import platform
import psutil
from psutil._common import bytes2human
import math
from datetime import datetime

# Logging
logging.basicConfig(filename='./logs/discordlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initiate json
file = open("config.json")
data = json.load(file)

# Public Variables
guildID = data["guildID"][0]


class botInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #def convert_size(size_bytes, prefix="b"):
    #    if size_bytes == 0:
    #        return "0B"
    #    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    #    i = int(math.floor(math.log(size_bytes, 1024)))
    #    p = math.pow(1024, i)
    #    s = round(size_bytes / p, 2)
    #    return "%s %s" % (s, size_name[i])

    @slash_command(guild_ids=[guildID], description="Check the bot's ping!")
    async def botinfo(self, ctx):
        # Define the info in variables
        uname = platform.uname()
        system = uname.system
        release = uname.release
        version = uname.version
        machine = uname.machine
        cores = psutil.cpu_count(logical=True)
        cpuUsage = psutil.cpu_percent()
        totalMemory = bytes2human(psutil.virtual_memory().total)
        availableMemory = bytes2human(psutil.virtual_memory().available)
        usedMemory = bytes2human(psutil.virtual_memory().used)
        bootTime = datetime.fromtimestamp(psutil.boot_time())
        ping = round(self.bot.latency * 1000)
        # Define the embed
        embed = discord.Embed(title="Bot Info", description=f"""
        **System:**
        - **System:** `{system}`
        - **Version:** `{version}`
        - **Release:** `{release}`
        - **Machine:** `{machine}`
        **CPU:**
        - **Cores:** `{cores}`
        - **Usage:** `{cpuUsage}%`
        **Memory:**
        - **Total:** `{totalMemory}`
        - **Used:** `{usedMemory}`
        - **Available:** `{availableMemory}`
        **Boot Time:** `{bootTime}`
        **Bot Ping:** `{ping}ms`
        """, color=0x00ff00)
        await ctx.respond(embed=embed)
        logger.info(f"{ctx.author.name} with ID: {ctx.author.id} has checked the bot ping!")

    @botinfo.error
    async def ping_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(botInfoCommand(bot))
