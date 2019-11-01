from __future__ import print_function
from redbot.core import commands


class reset(commands.Cog):
    """Time limited command to restart the bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.default)
    async def reset(self, ctx):
        """Restarts the bot"""
        await ctx.invoke(self.bot.get_command("restart"))
