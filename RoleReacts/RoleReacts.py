from __future__ import print_function
from redbot.core import Config
from redbot.core import commands
import discord


listener = getattr(commands.Cog, "listener", None)  # Trusty + Sinbad
if listener is None:

    def listener(name=None):
        return lambda x: x


class RoleReacts(commands.Cog):
    """Adds roles to people who react to a message"""



    def __init__(self, bot):
        self.bot = bot

        self.config = Config.get_conf(self, identifier=6457)
        self.config.register_guild(
            message=[0, 0],
            reacts={}
        )

    async def updateMessage(self, guild):
        botMessage = await self.config.guild(guild).message()
        message = await guild.get_channel(botMessage[1]).fetch_message(botMessage[0])

        reactList = await self.config.guild(guild).reacts()
        newMessage = "React to this message to get the indicated role\n"

        for react in reactList:
            await message.add_reaction(self.bot.get_emoji(int(react)))
            newMessage += str(self.bot.get_emoji(int(react))) + " - " + guild.get_role(reactList[react]).mention + "\n"
        newMessage += "After that, you can type @role to ping everyone who plays it"
        await message.edit(content=newMessage)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def forceupdate(self, ctx):
        await self.updateMessage(ctx.guild)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addreact(self, ctx, react: discord.Emoji, role: discord.Role):
        """Adds a role react to the list"""
        await ctx.message.add_reaction(react)
        reactList = await self.config.guild(ctx.guild).reacts()
        reactList[react.id] = role.id
        await self.config.guild(ctx.guild).reacts.set(reactList)
        await self.updateMessage(ctx.guild)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removereact(self, ctx, react: discord.Emoji):
        """Adds a role react to the list"""
        await ctx.message.add_reaction(react)
        reactList = await self.config.guild(ctx.guild).reacts()
        reactList.pop(str(react.id))
        await self.config.guild(ctx.guild).reacts.set(reactList)
        await self.updateMessage(ctx.guild)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createmessage(self, ctx):
        """stuff"""
        botMessage = await ctx.send("Message created. This message will be edited when role reacts are added")
        await self.config.guild(ctx.guild).message.set([botMessage.id, botMessage.channel.id])


    @listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        botMessage = await self.config.guild(guild).message()
        if payload.message_id == botMessage[0]:
            reactList = await self.config.guild(guild).reacts()
            role = guild.get_role(reactList[str(payload.emoji.id)])
            await payload.member.add_roles(role)


    @listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        botMessage = await self.config.guild(guild).message()
        if payload.message_id == botMessage[0]:
            reactList = await self.config.guild(guild).reacts()
            role = guild.get_role(reactList[str(payload.emoji.id)])
            await guild.get_member(payload.user_id).remove_roles(role)
