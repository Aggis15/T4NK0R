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
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


class musicPlay(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        wavelink.NodePool.get_node(identifier=node.identifier)

    @slash_command(guild_ids=[guildID], description="Play a song!")
    async def play(self, ctx, value: Option(str, required=True,
                                           description="Search for the song!")):
        #channel = ctx.message.author.voice.channel
        track = await wavelink.YouTubeTrack.search(query=value, return_first=True)
        """Play a song with the given search query.
        If not connected, connect to our voice channel.
        """
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and not vc.is_playing():
            await vc.queue.put_wait(track)
            await vc.play(track)
            await ctx.send(f'Added `{track.title}` to the queue...', delete_after=10)

        else:
            await vc.queue.put_wait(track)
            await ctx.send(f'Added `{track.title}` to the queue...', delete_after=10)

    @slash_command(guild_ids=[guildID], description="queue!")
    async def queue(self, ctx):
        vc: wavelink.Player = ctx.voice_client

        if not vc:
            return await ctx.send('No queue as we are not connected', delete_after=5)

        await ctx.send(vc.queue)

def setup(bot):
    bot.add_cog(musicPlay(bot))