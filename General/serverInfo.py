import logging
import discord
from discord.ext import commands
from discord.commands import slash_command
import json
import requests
from PIL import Image, ImageDraw, ImageFont
from resizeimage import resizeimage

# Logging
logging.basicConfig(
    filename="./logs/discordlogs.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initiate json
file = open("config.json")
data = json.load(file)

# Public variables
guildID = data["guildID"][0]


class serverInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        guild_ids=[guildID], description="A command to check the server information!"
    )
    async def server(self, ctx):
        guild = ctx.guild
        serverLevel = guild.premium_tier
        serverBoosts = guild.premium_subscription_count
        serverMembers = len(guild.members)
        serverTextChannels = len(guild.text_channels)
        serverVoiceChannels = len(guild.voice_channels)
        serverEmojis = len(guild.emojis)
        serverRoles = len(guild.roles)
        # Download the avatar
        getGuildAvatar = requests.get(guild.icon.url)
        with open(f"./Images/avatarCache/{guild.id}.png", "wb") as outfile:
            outfile.write(getGuildAvatar.content)
        guildAvatarImage = Image.open(f"./Images/avatarCache/{guild.id}.png")
        # Crop the avatar to make it a circle
        width, height = guildAvatarImage.size
        x = width - height
        img_cropped = guildAvatarImage.crop((x, 0, x + height, height))
        mask = Image.new("L", img_cropped.size)
        mask_draw = ImageDraw.Draw(mask)
        width, height = img_cropped.size
        mask_draw.ellipse((0, 0, width, height), fill=255)
        img_cropped.putalpha(mask)
        img_cropped.save(f"./Images/avatarCache/{guild.id}.png")
        # Resize the avatar to fit the image
        resizeAvatar = Image.open(f"./Images/avatarCache/{guild.id}.png")
        resizeAvatar = resizeimage.resize_width(resizeAvatar, 100)
        resizeAvatar.save(f"./Images/avatarCache/{guild.id}.png", resizeAvatar.format)
        defaultImage = Image.open("./Images/serverInfo.png")
        draw = ImageDraw.Draw(defaultImage)
        font = ImageFont.truetype("Bungee-Regular.ttf", 36)
        draw.text((438, 38), str(serverLevel), (157, 156, 157), font=font)
        draw.text((332, 85), str(serverBoosts), (157, 156, 157), font=font)
        draw.text((246, 148), str(serverMembers), (157, 156, 157), font=font)
        draw.text((370, 199), str(serverTextChannels), (157, 156, 157), font=font)
        draw.text((394, 243), str(serverVoiceChannels), (157, 156, 157), font=font)
        draw.text((388, 288), str(serverEmojis), (157, 156, 157), font=font)
        draw.text((357, 334), str(serverRoles), (157, 156, 157), font=font)
        avatarImage = Image.open(f"./Images/avatarCache/{guild.id}.png")
        defaultImage.paste(avatarImage, (40, 40), avatarImage)
        defaultImage.save("./Images/serverImageReady.png")
        await ctx.respond(file=discord.File("./Images/serverImageReady.png"))

        logger.info(
            f"{ctx.author.name} with ID: {ctx.author.id} has used the info slash command"
        )

    @server.error
    async def server_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(serverInfo(bot))
