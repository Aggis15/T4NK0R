import discord
from discord.ext import commands
import json
import random as r
from dotenv import load_dotenv
import os
import asyncpg
import logging
from PIL import Image, ImageFont, ImageDraw
from resizeimage import resizeimage
import requests
load_dotenv()

# Logging
logging.basicConfig(filename='logs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initiate json
file = open("config.json")
data = json.load(file)

# Public Vars
prefix = data["prefix"]
dbHost = os.environ.get("dbHost")
dbUser = os.environ.get("dbUser")
dbPass = os.environ.get("dbPass")
dbName = os.environ.get("dbName")
dbPort = os.environ.get("dbPort")
tableName = os.environ.get("tableName")
startingXP = data["XP"]["startingXP"]
whitelistChannels = data["whitelistChannels"]
levelupChat = data["channelIDs"]["levelupChat"]


class MessageListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Create cooldown bucket
        self.cd_mapping = commands.CooldownMapping.from_cooldown(100, 120, commands.BucketType.member)
        self.startingXP = startingXP
        self.levelupChat = levelupChat

    def xp(self):
        return r.randint(1, 100)

    @commands.Cog.listener()
    async def on_message(self, message):
        conn = await asyncpg.create_pool(f'postgres://{dbUser}:{dbPass}@{dbHost}:{dbPort}/{dbName}')
        await self.bot.process_commands(message)
        if message.author.bot:
            return
        elif message.channel.id == whitelistChannels:
            return
        else:
            await self.bot.process_commands(message)
            bucket = self.cd_mapping.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if not retry_after:
                xp_val = self.xp()
                await conn.execute(f"INSERT INTO {tableName} (username, userid, currentxp, neededxp) VALUES ('{message.author.name}', {message.author.id}, {xp_val}, {startingXP})  ON CONFLICT (userid) DO UPDATE SET currentxp = {tableName}.currentxp + {xp_val}")
                xp = await conn.fetchval(f"SELECT currentxp FROM {tableName} WHERE userid = {message.author.id}")
                await conn.execute(f"UPDATE {tableName} SET neededxp = {tableName}.neededxp - {xp_val} WHERE userid = {message.author.id}")
                neededXP = await conn.fetchval(f"SELECT neededxp FROM {tableName} WHERE userid = {message.author.id}")
                if neededXP <= 0:
                    await conn.execute(f"UPDATE {tableName} SET currentlevel = {tableName}.currentlevel + 1 WHERE userid = {message.author.id}")
                    level = await conn.fetchval(f"SELECT currentlevel FROM {tableName} WHERE userid = {message.author.id}")
                    untilLevelUp = int(str(xp)[-2:])
                    untilLevelUp = startingXP * level - untilLevelUp
                    await conn.execute(f"UPDATE {tableName} SET neededxp = {untilLevelUp} WHERE userid = {message.author.id}")
                    notify = await conn.fetchval(f"SELECT doNotify FROM {tableName} WHERE userid = {message.author.id}")
                    if notify:
                        untilLevelUp = await conn.fetchval(f"SELECT neededxp FROM {tableName} WHERE userid = {message.author.id}")
                        # Edit the default image to add the text then send it
                        defaultImage = Image.open("./Images/levelImage.png")
                        getAvatar = requests.get(message.author.avatar.url)
                        with open(f"./Images/avatarCache/{message.author.id}.png", "wb") as outfile:
                            outfile.write(getAvatar.content)
                        avatarImage = Image.open(f"./Images/avatarCache/{message.author.id}.png")
                        # Crop the avatar to make it a circle
                        width, height = avatarImage.size
                        x = (width - height)
                        img_cropped = avatarImage.crop((x, 0, x+height, height))
                        mask = Image.new("L", img_cropped.size)
                        mask_draw = ImageDraw.Draw(mask)
                        width, height = img_cropped.size
                        mask_draw.ellipse((0, 0, width, height), fill=255)
                        img_cropped.putalpha(mask)
                        img_cropped.save(f"./Images/avatarCache/{message.author.id}.png")
                        # Resize the avatar to fit the image
                        resizeAvatar = Image.open(f"./Images/avatarCache/{message.author.id}.png")
                        resizeAvatar = resizeimage.resize_width(resizeAvatar, 100)
                        resizeAvatar.save(f"./Images/avatarCache/{message.author.id}.png", resizeAvatar.format)
                        # Add the text
                        draw = ImageDraw.Draw(defaultImage)
                        levelFont = ImageFont.truetype("Bungee-Regular.ttf", 20)
                        xpFont = ImageFont.truetype("Bungee-Regular.ttf", 18)
                        untilLevelUpFont = ImageFont.truetype("Bungee-Regular.ttf", 16)
                        draw.text((234, 94), f"{level}", (255, 255, 255), font=levelFont)
                        draw.text((185, 55), str(xp), (255, 255, 255), font=xpFont)
                        draw.text((271, 31), str(untilLevelUp), (255, 255, 255), font=untilLevelUpFont)
                        # Add the image, then save
                        resizedAvatar = Image.open(f"./Images/avatarCache/{message.author.id}.png")
                        defaultImage.paste(resizedAvatar, (27, 25), resizedAvatar)
                        defaultImage.save("./Images/levelImageReady.png")
                        levelupChannel = self.bot.get_channel(self.levelupChat)
                        await levelupChannel.send(f"{message.author.mention} You have reached the next level!", file=discord.File("./Images/levelImageReady.png"))
                logger.info(f"{message.author.name} with ID: {message.author.id} has logged {xp_val} XP")
        await conn.close()


def setup(bot):
    bot.add_cog(MessageListener(bot))
