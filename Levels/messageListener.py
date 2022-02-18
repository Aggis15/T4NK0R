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
logging.basicConfig(filename='./logs/discordlogs.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initiate json
file = open("config.json")
data = json.load(file)

# Public Vars
prefix = data["prefix"]
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
TABLE_NAME = os.environ.get("TABLE_NAME")
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
        await self.bot.process_commands(message)
        conn = await asyncpg.connect(f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

        if message.author.bot:
            return
        elif message.channel.id in whitelistChannels:
            return
        else:
            await self.bot.process_commands(message)
            bucket = self.cd_mapping.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if not retry_after:
                xp_val = self.xp()
                await conn.execute(f"INSERT INTO {TABLE_NAME} (username, userid, currentxp, neededxp) VALUES ('{message.author.name}', {message.author.id}, {xp_val}, {startingXP})  ON CONFLICT (userid) DO UPDATE SET currentxp = {TABLE_NAME}.currentxp + {xp_val}")
                xp = await conn.fetchval(f"SELECT currentxp FROM {TABLE_NAME} WHERE userid = {message.author.id}")
                await conn.execute(f"UPDATE {TABLE_NAME} SET neededxp = {TABLE_NAME}.neededxp - {xp_val} WHERE userid = {message.author.id}")
                neededXP = await conn.fetchval(f"SELECT neededxp FROM {TABLE_NAME} WHERE userid = {message.author.id}")
                if neededXP <= 0:
                    await conn.execute(f"UPDATE {TABLE_NAME} SET currentlevel = {TABLE_NAME}.currentlevel + 1 WHERE userid = {message.author.id}")
                    level = await conn.fetchval(f"SELECT currentlevel FROM {TABLE_NAME} WHERE userid = {message.author.id}")
                    untilLevelUp = int(str(xp)[-2:])
                    untilLevelUp = startingXP * level - untilLevelUp
                    await conn.execute(f"UPDATE {TABLE_NAME} SET neededxp = {untilLevelUp} WHERE userid = {message.author.id}")
                    notify = await conn.fetchval(f"SELECT doNotify FROM {TABLE_NAME} WHERE userid = {message.author.id}")
                    if notify:
                        untilLevelUp = await conn.fetchval(f"SELECT neededxp FROM {TABLE_NAME} WHERE userid = {message.author.id}")
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
