import discord
from discord.commands import slash_command, Option
from discord.ext import commands, pages
import logging
import json


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


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = [
            discord.Embed(
                title="Welcome to the interactive help center for T4NK0R!",
                description="This guide is made "
                "for users who are "
                "interested in "
                "knowing how T4NK0R "
                "works! You can "
                "navigate through "
                "the guide using "
                "the buttons below! "
                "If you have any "
                "questions, "
                "feel free to ask "
                "any staff member "
                "or Aggis15!",
                color=0x00FF00,
            ),
            discord.Embed(
                title="Leveling System",
                description="Levels work just like you'd expect really.\n\nEvery 2 "
                "minutes, you can gather from 1 to 200 XP. By chatting "
                "more, you can reach new levels!\n\n**Commands "
                "associated with levels**\n\n/info - Users can use "
                "this in order to check what their level is along with "
                "how much XP they need in order to reach the next "
                "level!\n\n/leaderboard - Check what the leaderboard "
                "is currently looking like!\n\n/notifications - Change "
                "your preference regarding notifications when you "
                "reach the next level!\n\n/overridelevel - This can "
                "only be used by people who are **level 500** or "
                "bigger. This command allows for people to override "
                "their current level name and use a custom one!",
                color=0x00FF00,
            ),
            discord.Embed(
                title="Music",
                description="T4NK0R supports music functions!\n\n**Commands associated with "
                "music**\n\n/play - Start playing music! You can provide name "
                "songs or Youtube URLs. You must be in a **Voice Channel** to "
                "use this command!\n\n/pause - Pause the player.\n\n/resume - "
                "Resume the player.\n\n/stop - Stop the currently playing song. "
                "If there is a queue, the next song plays.\n\n/queue - Check the "
                "queue.\n\n/disconnect - Stop the player and disconnect from the "
                "Voice Channel.",
                color=0x00FF00,
            ),
            discord.Embed(
                title="General Commands",
                description="This category is about general commands that didn't "
                "fit in the other categories.\n\n**Commands associated "
                "with general**\n\n/botinfo - See general information "
                "about the bot info like the ping "
                "etc.\n\n/historyquote - Recall on a quote said by "
                "Star.\n\n/serverinfo - See information regarding the "
                "server\n\n/reportbug - Use this command if you want "
                "to report a bug you have seen. When reporting bugs, "
                "you must be descriptive about it. You may be "
                "contacted by the bot developer for additional "
                "information.\n\n/newfeature - Use this command if "
                "you want to suggest a new feature to be added to the "
                "bot! You may be contacted by the bot developer for "
                "additional information.",
            ),
            discord.Embed(
                title="Admin Commands",
                description="This category is about commands that only server "
                "admins can use.\n\n**Command associated with Admin "
                "Commands**\n\n/changestatus - Use this command when "
                "you want to change the bot status "
                "manually.\n\n/readlogs - Get a copy of the bot logs. "
                "Useful for troubleshooting.\n\n/shutdownbot - "
                "Dangerous command. Shuts the bot down if needed. Will "
                "need to be turned on manually thereafter.",
                color=0x00FF00,
            ),
            discord.Embed(
                title="Admin Commands - Twitch",
                description="This category is about twitch commands "
                "available. Only used by admins\n\n**Command "
                "associated with Admin Commands - "
                "Twitch**\n\n/getuserid - Get the ID of a "
                "Twitch user. Used later.\n\n/addstream - Add "
                "a stream to the database so the bot "
                "automatically notifies the members of the "
                "TSE. Use the ID you get from "
                "getuserid\n\n/getstreams - Get the number of "
                "streams added to be notified "
                "automatically.\n\n/removestream - Remove a "
                "certain stream from the database so it does "
                "not get published anymore.",
                color=0x00FF00,
            ),
            discord.Embed(
                title="Credits",
                description="Aggis - Bot Developer\nStarDelivery - Image "
                "Designer\nRest of the Staff Team - Providing insight and "
                "helping me design the bot\n\n[Trello Board]("
                "https://trello.com/b/HxDSanm5/t4nk0r)",
            ),
        ]
        for page in self.pages:
            page.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/772886530259812352/934169834235772929/T4NK0R.png"
            )

    def get_pages(self):
        return self.pages

    @slash_command(guild_ids=[guildID], description="Help command")
    async def help(self, ctx: discord.ApplicationContext):
        """Demonstrates using the paginator with the default options."""
        paginator = pages.Paginator(pages=self.get_pages())
        await paginator.respond(ctx.interaction, ephemeral=False)


def setup(bot):
    bot.add_cog(Help(bot))
