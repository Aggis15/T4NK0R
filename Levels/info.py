import logging
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from PIL import Image, ImageFont, ImageDraw
from resizeimage import resizeimage
import requests
import json
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


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

# Public Variables
guildID = data["guildID"][0]
startingXP = data["XP"]["startingXP"]
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
LEVEL_TABLE_NAME = os.environ.get("LEVEL_TABLE_NAME")


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.startingXP = startingXP

    @slash_command(
        guild_ids=[guildID],
        description="A command to check yours or someone else's profile information!",
    )
    async def info(
        self,
        ctx,
        user: Option(
            discord.Member,
            required=False,
            description="Choose the member you want to look at, or leave blank if you want to see info about yourself!",
        ),
    ):
        conn = await asyncpg.connect(
            f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        user = user if user is not None else ctx.author
        accountCreatedAt = f"{user.created_at.strftime('%d/%m/%y')}"
        joinedServerAt = f"{user.joined_at.strftime('%d/%m/%y')}"
        isBoosting = "Yes" if user.premium_since is True else "No"
        currentLevel = await conn.fetchval(
            f"SELECT currentlevel FROM {LEVEL_TABLE_NAME} where userid = {user.id}"
        )
        currentXP = await conn.fetchval(
            f"SELECT currentxp FROM {LEVEL_TABLE_NAME} where userid = {user.id}"
        )
        doOverride = await conn.fetchval(
            f"SELECT dooverridelevelname FROM {LEVEL_TABLE_NAME} where userid = {user.id}"
        )
        if doOverride:
            currentLevelName = await conn.fetchval(
                f"SELECT overridelevelname FROM {LEVEL_TABLE_NAME} where userid = {user.id}"
            )
        else:
            currentLevelName = await conn.fetchval(
                f"SELECT levelname FROM {LEVEL_TABLE_NAME} where userid = {user.id}"
            )
        untilLevelUp = await conn.fetchval(
            f"SELECT neededxp FROM {LEVEL_TABLE_NAME} where userid = {user.id}"
        )
        doNotify = await conn.fetchval(
            f"SELECT doNotify FROM {LEVEL_TABLE_NAME} where userid = {user.id}"
        )
        defaultImage = Image.open("./Images/infoImage.png")
        # If the user's avatar is not in the cache, download it
        if not os.path.isfile(f"./Images/avatarCache/{user.id}"):
            getAvatar = requests.get(user.avatar.url)
            with open(f"./Images/avatarCache/{user.id}.png", "wb") as outfile:
                outfile.write(getAvatar.content)
            avatarImage = Image.open(f"./Images/avatarCache/{user.id}.png")
            # Crop the avatar to make it a circle
            width, height = avatarImage.size
            x = width - height
            img_cropped = avatarImage.crop((x, 0, x + height, height))
            mask = Image.new("L", img_cropped.size)
            mask_draw = ImageDraw.Draw(mask)
            width, height = img_cropped.size
            mask_draw.ellipse((0, 0, width, height), fill=255)
            img_cropped.putalpha(mask)
            img_cropped.save(f"./Images/avatarCache/{user.id}.png")
            # Resize the avatar to fit the image
            resizeAvatar = Image.open(f"./Images/avatarCache/{user.id}.png")
            resizeAvatar = resizeimage.resize_width(resizeAvatar, 100)
            resizeAvatar.save(
                f"./Images/avatarCache/{user.id}.png", resizeAvatar.format
            )
        draw = ImageDraw.Draw(defaultImage)
        font = ImageFont.truetype("Bungee-Regular.ttf", 36)
        draw.text((539, 35), str(accountCreatedAt), (157, 156, 157), font=font)
        draw.text((488, 80), str(joinedServerAt), (157, 156, 157), font=font)
        if isBoosting == "No":
            draw.text((383, 120), isBoosting, (255, 0, 0), font=font)
        else:
            draw.text((383, 128), isBoosting, (0, 255, 0), font=font)
        draw.text(
            (182, 176),
            f"{currentLevel} ({currentLevelName})",
            (157, 156, 157),
            font=font,
        )
        draw.text((108, 229), str(currentXP), (157, 156, 157), font=font)
        draw.text((305, 280), str(untilLevelUp), (157, 156, 157), font=font)
        if doNotify:
            draw.text((521, 332), "Yes", (0, 255, 0), font=font)
        else:
            draw.text((521, 332), "No", (255, 0, 0), font=font)
        avatar = Image.open(f"./Images/avatarCache/{user.id}.png")
        defaultImage.paste(avatar, (40, 45), avatar)
        defaultImage.save("./Images/infoImageReady.png")
        if currentLevel is None:
            await ctx.respond(
                "This user has not yet been registered to the databases, so some fields might be blank!"
            )
        await ctx.respond(file=discord.File("./Images/infoImageReady.png"))
        await conn.close()
        logger.info(f"{user.name} with ID: {user.id} has used the info slash command")

    @info.error
    async def info_error(self, ctx, error):
        await ctx.respond(f"`{error}`")


def setup(bot):
    bot.add_cog(info(bot))
