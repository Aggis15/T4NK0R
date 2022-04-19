import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import wavelink
from wavelink.ext import spotify
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Initiate json
file = open("config.json")
data = json.load(file)

# Public variables
guildID = data["guildID"][0]


class musicQueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[guildID], description="queue!")
    async def queue(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if not vc:
            return await ctx.respond("No queue as we are not connected")
        else:
            if vc.queue.is_empty and vc.is_playing():
                await ctx.respond(f"Currently playing `{vc.source}`. Nothing queued.")
            else:
                embed = discord.Embed(
                    title="Queue",
                    description="**# • Track Name • Track Duration**",
                    color=0x00FF00,
                )
                counter = 0
                for track in vc.queue:
                    counter = counter + 1
                    embed.add_field(
                        name="\u200b",
                        value=f"**#{counter} • [{track.title}]({track.uri}) • {track.duration}**",
                        inline=False,
                    )
                await ctx.respond(f"Currently playing: {vc.source}", embed=embed)


def setup(bot):
    bot.add_cog(musicQueue(bot))
