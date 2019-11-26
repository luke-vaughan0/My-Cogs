from __future__ import print_function
from redbot.core import commands
from redbot.core import Config
import discord


class vote(commands.Cog):
    """Adds a voting system to a channel"""

    def __init__(self, bot):
        self.bot = bot
        default_guild = {
            "voting": []
        }
        default_channel = {
            "upemote": "",
            "downemote": "",
            "remove": 0,
            "pin": 0

        }

        self.config = Config.get_conf(self, identifier=6457)
        self.config.register_guild(**default_guild)
        self.config.register_channel(**default_channel)

    @commands.command()
    async def addchannel(self, ctx, upemote: discord.Emoji, downemote: discord.Emoji, remove: int, pin: int):
        """Activates the voting system in the current channel"""
        channels = await self.config.guild(ctx.guild).voting()
        try:
            channels.append(ctx.channel.id)
        except AttributeError:
            channels = [ctx.channel.id]
        await self.config.guild(ctx.guild).voting.set(channels)
        await self.config.channel(ctx.channel).upemote.set(upemote.id)
        await self.config.channel(ctx.channel).downemote.set(downemote.id)
        await self.config.channel(ctx.channel).remove.set(remove)
        await self.config.channel(ctx.channel).pin.set(pin)

    @commands.command()
    async def removechannel(self, ctx):
        """Activates the voting system in the current channel"""
        channels = await self.config.guild(ctx.guild).voting()
        channels.remove(ctx.channel.id)
        await self.config.guild(ctx.guild).voting.set(channels)
        await self.config.channel(ctx.channel).clear()


