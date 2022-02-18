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

    @slash_command(guild_ids=[guildID], description="Resume the song!")
    async def disconnect(self, ctx):
        if not ctx.voice_client:
            await ctx.respond("You need to be in a voice channel to use this command!")
        else:
            vc: wavelink.Player = ctx.voice_client
            await vc.disconnect()
            await ctx.respond("Disconnected from voice channel!")


def setup(bot):
    bot.add_cog(musicStop(bot))