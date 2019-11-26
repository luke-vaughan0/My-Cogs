from __future__ import print_function
from redbot.core import commands
from redbot.core import Config
import discord

listener = getattr(commands.Cog, "listener", None)  # Trusty + Sinbad
if listener is None:

    def listener(name=None):
        return lambda x: x

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
    async def addchannel(self, ctx, upemote: discord.Emoji, downemote: discord.Emoji, pin: int, remove: int):
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
        """Removes the voting system in the current channel"""
        channels = await self.config.guild(ctx.guild).voting()
        channels.remove(ctx.channel.id)
        await self.config.guild(ctx.guild).voting.set(channels)
        await self.config.channel(ctx.channel).clear()

    @listener()
    async def on_message(self, message):
        channels = await self.config.guild(message.guild).voting()
        if message.channel.id in channels:
            await message.add_reaction(self.bot.get_emoji(await self.config.channel(message.channel).upemote()))
            await message.add_reaction(self.bot.get_emoji(await self.config.channel(message.channel).downemote()))

    @listener()
    async def on_reaction_add(self, reaction, user):
        channels = await self.config.guild(reaction.message.guild).voting()
        if reaction.message.channel.id in channels:
            up = await self.config.channel(reaction.message.channel).upemote()
            down = await self.config.channel(reaction.message.channel).downemote()
            pin = await self.config.channel(reaction.message.channel).pin()
            remove = await self.config.channel(reaction.message.channel).remove()
            if reaction.emoji.id == up or reaction.emoji.id == down:
                if user == reaction.message.author:
                    await reaction.remove(user)
                if reaction.emoji.id == up and pin != 0:
                    if reaction.count < pin:
                        print("pinned a great meme")
                        await reaction.message.pin()
                if reaction.emoji.id == down and remove != 0:
                    if reaction.count < remove:
                        print("deleted a bad meme")
                        await reaction.message.delete()



