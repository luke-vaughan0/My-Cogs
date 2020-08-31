from __future__ import print_function
from redbot.core import commands
import moviepy.editor as mp
import os
import discord


class Catjam(commands.Cog):
    """Time limited command to restart the bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def catbpm(self, ctx, bpm: int):
        """Scales the catjam gif to a given bpm"""
        if bpm < 40:
            await ctx.send("That's a bit too slow!")
            return
        if bpm > 1000:
            await ctx.send("That's a bit too fast!")
            return
        await ctx.send(os.getcwd())
        async with ctx.typing():
            with mp.VideoFileClip("catjam.gif") as clip:
                edited = clip.fx(mp.vfx.speedx, bpm / 123.417721519)
                edited.write_gif("cat.gif")
                with open("cat.gif", "rb") as cat:
                    await ctx.send(file=discord.File(cat))
