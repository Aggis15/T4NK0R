from discord.ext import commands
from discord.commands import slash_command
import wavelink
import json

# Initiate json
file = open("config.json")
data = json.load(file)

# Public variables
guildID = data["guildID"][0]


class musicStop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        wavelink.NodePool.get_node(identifier=node.identifier)

    @slash_command(guild_ids=[guildID], description="Stop the music! If there is anything in the queue, plays the next song!")
    async def stop(self, ctx):
        if not ctx.voice_client:
            await ctx.respond("I'm not playing anything right now!")
        else:
            vc: wavelink.Player = ctx.voice_client
            await vc.stop()
            await ctx.respond("Music stopped!")


def setup(bot):
    bot.add_cog(musicStop(bot))