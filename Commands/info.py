import logging
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from PIL import Image, ImageFont, ImageDraw
from resizeimage import resizeimage
import requests
import json
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


# Logging
logging.basicConfig(filename='logs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initiate json
file = open("config.json")
data = json.load(file)

# Public Vars
guildID = data["guildID"][0]
startingXP = data["XP"]["startingXP"]
dbHost = os.environ.get("dbHost")
dbUser = os.environ.get("dbUser")
dbPass = os.environ.get("dbPass")
dbName = os.environ.get("dbName")
dbPort = os.environ.get("dbPort")
tableName = os.environ.get("tableName")
conn = psycopg2.connect(host=dbHost, database=dbName, user=dbUser, password=dbPass, port=dbPort)
cur = conn.cursor()


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.startingXP = startingXP

    @slash_command(guild_ids=[guildID], description="A command to check yours or someone else's profile information!")
    async def info(self, ctx, user: Option(discord.Member, required=False, description="Choose the member you want to look at, or leave blank if you want to see info about yourself!")):
        user = user if user is not None else ctx.author
        accountCreatedAt = f"{user.created_at.strftime('%d/%m/%y')}"
        joinedServerAt = f"{user.joined_at.strftime('%d/%m/%y')}"
        isBoosting = "Yes" if user.premium_since is True else "No"
        cur.execute(f"SELECT currentlevel FROM {tableName} where userid = {user.id}")
        currentLevel = cur.fetchall()
        currentLevel = currentLevel[0][0] if currentLevel else 0
        cur.execute(f"SELECT currentxp FROM {tableName} where userid = {user.id}")
        currentXP = cur.fetchall()
        currentXP = currentXP[0][0] if currentXP else 0
        untilLevelUp = currentXP - self.startingXP
        cur.execute(f"SELECT doNotify FROM {tableName} where userid = {user.id}")
        doNotify = cur.fetchall()
        doNotify = "Yes" if doNotify[0][0] is True else "No"
        defaultImage = Image.open("./Images/infoImage.png")
        # If the user's avatar is not in the cache, download it
        if not os.path.isfile(f"./Images/avatarCache/{user.id}"):
            getAvatar = requests.get(user.avatar.url)
            with open(f"./Images/avatarCache/{user.id}.png", "wb") as outfile:
                outfile.write(getAvatar.content)
            avatarImage = Image.open(f"./Images/avatarCache/{user.id}.png")
            # Crop the avatar to make it a circle
            width, height = avatarImage.size
            x = (width - height)
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
            resizeAvatar.save(f"./Images/avatarCache/{user.id}.png", resizeAvatar.format)
        draw = ImageDraw.Draw(defaultImage)
        font = ImageFont.truetype("Bungee-Regular.ttf", 36)
        draw.text((539, 35), str(accountCreatedAt), (157, 156, 157), font=font)
        draw.text((488, 80), str(joinedServerAt), (157, 156, 157), font=font)
        if isBoosting == "No":
            draw.text((383, 120), isBoosting, (255, 0, 0), font=font)
        else:
            draw.text((383, 128), isBoosting, (0, 255, 0), font=font)
        draw.text((182, 176), str(currentLevel), (157, 156, 157), font=font)
        draw.text((108, 229), str(currentXP), (157, 156, 157), font=font)
        draw.text((305, 280), str(untilLevelUp), (157, 156, 157), font=font)
        if doNotify == "No":
            draw.text((521, 332), doNotify, (255, 0, 0), font=font)
        else:
            draw.text((521, 332), doNotify, (0, 255, 0), font=font)
        avatar = Image.open(f"./Images/avatarCache/{user.id}.png")
        defaultImage.paste(avatar, (42, 45), avatar)
        defaultImage.save("./Images/infoImageReady.png")
        await ctx.respond(file=discord.File("./Images/infoImageReady.png"))

        logger.info(f"{user.name} with ID: {user.id} has used the info slash command")

def setup(bot):
    bot.add_cog(info(bot))

