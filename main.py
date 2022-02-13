import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import asyncpg
load_dotenv()

# Initiate json
file = open("config.json")
data = json.load(file)

# Public vars
botToken = os.environ.get("botToken")
prefix = data["prefix"]

# Initiate the bot
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

#async def create_connection_pool():
#    bot.pg_conn = await asyncpg.create_pool('postgres://devuser:postgres@localhost:5432/devdb')

@bot.event
async def on_ready():
    print(f"Bot has successfully started as {bot.user}")


# Loads the cogs
for filename in os.listdir("./Join_Leave_Listeners"):
    if filename.endswith(".py"):
        bot.load_extension(f"Join_Leave_Listeners.{filename[:-3]}")

for filename in os.listdir("./Commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"Commands.{filename[:-3]}")

for filename in os.listdir("./Levels"):
    if filename.endswith(".py"):
        bot.load_extension(f"Levels.{filename[:-3]}")

for filename in os.listdir("./Admin"):
    if filename.endswith(".py"):
        bot.load_extension(f"Admin.{filename[:-3]}")

for filename in os.listdir("./Twitch"):
    if filename.endswith(".py"):
        bot.load_extension(f"Twitch.{filename[:-3]}")


if __name__ == "__main__":
    bot.run(botToken)
