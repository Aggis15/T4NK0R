import logging
import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import wavelink
from wavelink.ext import spotify
load_dotenv()

# Logging
logging.basicConfig(filename='./logs/discordlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


# Initiate json
file = open("config.json")
data = json.load(file)

# Public vars
BOT_TOKEN = os.environ.get("BOT_TOKEN")
prefix = data["prefix"]
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

# Initiate the bot
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"Bot has successfully started as {bot.user}")
    await wavelink.NodePool.create_node(bot=bot,
                                        host='0.0.0.0',
                                        port=2333,
                                        password='a579c5f06b24f0e61f18b8226d414ed3',
                                        spotify_client=spotify.SpotifyClient(client_id=SPOTIFY_CLIENT_ID,
                                                                             client_secret=SPOTIFY_CLIENT_SECRET))

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")



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

for filename in os.listdir("./Music"):
    if filename.endswith(".py"):
        bot.load_extension(f"Music.{filename[:-3]}")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
