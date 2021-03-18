from __future__ import print_function
from redbot.core import commands
from redbot.core import Config
import asyncio
import discord


listener = getattr(commands.Cog, "listener", None)  # Trusty + Sinbad
if listener is None:

    def listener(name=None):
        return lambda x: x


class TrialSignup(commands.Cog):
    """Commands to create and sign up to trials"""
    def __init__(self, bot):
        self.bot = bot

        default_channel = {
            "trialInfo": []
        }

        default_global = {
            "trialChannels": []
        }

        self.config = Config.get_conf(self, identifier=6457)
        self.config.register_channel(**default_channel)
        self.config.register_global(**default_global)


    @commands.command()
    @commands.has_role("Officer")
    async def trial(self, ctx, tankNum: int, healNum: int, ddNum: int, description: str = "Created a trial:"):
        """Creates a trial"""
        trialInfo = await self.config.channel(ctx.channel).trialInfo()
        if not trialInfo:
            trialInfo = [0]
        if trialInfo[0] != 0:
            await ctx.send("You must end the current trial before creating a new one!")
        else:
            trialInfo = [0, ddNum, healNum, tankNum, [], [], []]
            trialMessage = [description+"\n",
                            "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): \n",
                            "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): \n",
                            "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): \n"]
            signupMessage = await ctx.send(trialMessage[0] + trialMessage[3] + trialMessage[2] + trialMessage[1])
            trialInfo[0] = signupMessage.id
            trialInfo.append(trialMessage)

            channels = await self.config.trialChannels()
            channels.append(ctx.channel.id)
            await self.config.trialChannels.set(channels)

            await self.config.channel(ctx.channel).trialInfo.set(trialInfo)


    @commands.command()
    @commands.has_role("Officer")
    async def endtrial(self, ctx, channel: discord.TextChannel = None):
        """Ends current trial"""
        if not channel:
            channel = ctx.channel
        trialInfo = [0, 1, 1, 1, [], [], []]
        channels = await self.config.trialChannels()
        channels.remove(channel.id)
        await ctx.send("Trial in <#" + str(channel.id) + "> ended")
        await self.config.channel(channel).trialInfo.set(trialInfo)
        await self.config.trialChannels.set(channels)

    @commands.command()
    @commands.has_role("Officer")
    async def work(self, ctx):
        """Fixes it if it's stuck"""
        await self.config.inUse.set(False)
        await ctx.send("ok")



    @commands.command()
    @commands.has_role("Officer")
    async def addsignup(self, ctx, user: discord.Member, role, trialChannel: discord.TextChannel = None):
        """Adds a user to the trial"""
        if not trialChannel:
            trialChannel = ctx.channel
        dd = ["dd", "dps", "damage"]
        heal = ["heal", "healer"]
        tank = ["tank"]
        trialInfo = await self.config.channel(trialChannel).trialInfo()

        try:
            channelMessage = await trialChannel.fetch_message(trialInfo[0])
        except discord.NotFound:
            await ctx.send("No trial currently running")
            return

        if role in dd:
            if user.id in trialInfo[4] or user.id in trialInfo[5] or user.id in trialInfo[6]:
                await ctx.send(user.name + " is already signed up!")
            else:
                if len(trialInfo[4]) >= trialInfo[1]:
                    await ctx.send("All DD spots are taken!")
                else:
                    await ctx.send(user.name + " has been signed up as a dd")
                    trialInfo[4].append(user.id)
                    newRow = "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): "
                    for users in trialInfo[4]:
                        newRow += self.bot.get_user(users).mention + ", "
                    newRow = newRow[:-2] + "\n"
                    trialInfo[7][1] = newRow
                    await channelMessage.edit(
                        content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])

                    await self.config.channel(trialChannel).trialInfo.set(trialInfo)


        if role in heal:
            if user.id in trialInfo[4] or user.id in trialInfo[5] or user.id in trialInfo[6]:
                await ctx.send(user.name + " is already signed up!")
            else:
                if len(trialInfo[5]) >= trialInfo[2]:
                    await ctx.send("All healer spots are taken!")
                else:
                    await ctx.send(user.name + " has been signed up as a healer")
                    trialInfo[5].append(user.id)
                    newRow = "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): "
                    for users in trialInfo[5]:
                        newRow += self.bot.get_user(users).mention + ", "
                    newRow = newRow[:-2] + "\n"
                    trialInfo[7][2] = newRow
                    await channelMessage.edit(
                        content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])

                    await self.config.channel(trialChannel).trialInfo.set(trialInfo)


        if role in tank:
            if user.id in trialInfo[4] or user.id in trialInfo[5] or user.id in trialInfo[6]:
                await ctx.send(user.name + " is already signed up!")
            else:
                if len(trialInfo[6]) >= trialInfo[3]:
                    await ctx.send("All tank spots are taken!")
                else:
                    await ctx.send(user.name + " has been signed up as a tank")
                    trialInfo[6].append(user.id)
                    newRow = "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): "
                    for users in trialInfo[6]:
                        newRow += self.bot.get_user(users).mention + ", "
                    newRow = newRow[:-2] + "\n"
                    trialInfo[7][3] = newRow
                    await channelMessage.edit(
                        content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])

                    await self.config.channel(trialChannel).trialInfo.set(trialInfo)

    @commands.command()
    @commands.has_role("Officer")
    async def restoretrial(self, ctx, trialChannel: discord.TextChannel = None):
        """For when zeb deletes it again"""
        if not trialChannel:
            trialChannel = ctx.channel
        trialInfo = await self.config.channel(trialChannel).trialInfo()
        newMessage = await trialChannel.send("Restoring")
        await newMessage.edit(
            content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
        trialInfo[0] = newMessage.id
        await self.config.channel(trialChannel).trialInfo.set(trialInfo)

    @commands.command()
    @commands.has_role("Officer")
    async def verifytrial(self, ctx, trialChannel: discord.TextChannel = None):
        """Fixes missing people and stuff"""
        if not trialChannel:
            trialChannel = ctx.channel
        trialInfo = await self.config.channel(trialChannel).trialInfo()
        for signup in trialInfo[4]:
            if self.bot.get_user(signup) is None:
                #trialInfo[4].remove(signup)
                #newRow = "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): "
                #for users in trialInfo[4]:
                #    newRow += self.bot.get_user(users).mention + ", "
                #newRow = newRow[:-2] + "\n"
                #trialInfo[7][1] = newRow
                await ctx.send("<@"+str(signup)+"> is no longer in the server, they have been unsigned")
        await ctx.send("Verification complete")
        await self.config.channel(trialChannel).trialInfo.set(trialInfo)

    @commands.command()
    @commands.has_role("Officer")
    async def removesignup(self, ctx, user: discord.Member, role, trialChannel: discord.TextChannel = None):
        """Removes a user from the trial"""
        if not trialChannel:
            trialChannel = ctx.channel
        dd = ["dd", "dps", "damage"]
        heal = ["heal", "healer"]
        tank = ["tank"]
        trialInfo = await self.config.channel(trialChannel).trialInfo()

        try:
            channelMessage = await trialChannel.fetch_message(trialInfo[0])
        except discord.NotFound:
            await ctx.send("No trial currently running")
            return

        if role in dd:
            if user.id in trialInfo[4]:
                await ctx.send(user.name + " has been unsigned")
                trialInfo[4].remove(user.id)
                newRow = "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): "
                for users in trialInfo[4]:
                    newRow += self.bot.get_user(users).mention + ", "
                newRow = newRow[:-2] + "\n"
                trialInfo[7][1] = newRow
                await channelMessage.edit(
                    content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])

                await self.config.channel(trialChannel).trialInfo.set(trialInfo)
            else:
                await ctx.send(user.name + " wasn't signed up!")



        if role in heal:
            if user.id in trialInfo[5]:
                await ctx.send(user.name + " has been unsigned")
                trialInfo[5].remove(user.id)
                newRow = "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): "
                for users in trialInfo[5]:
                    newRow += self.bot.get_user(users).mention + ", "
                newRow = newRow[:-2] + "\n"
                trialInfo[7][2] = newRow
                await channelMessage.edit(
                    content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                await self.config.channel(trialChannel).trialInfo.set(trialInfo)
            else:
                await ctx.send(user.name + " wasn't signed up!")



        if role in tank:
            if user.id in trialInfo[6]:
                await ctx.send(user.name + " has been unsigned")
                trialInfo[6].remove(user.id)
                newRow = "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): "
                for users in trialInfo[6]:
                    newRow += self.bot.get_user(users).mention + ", "
                newRow = newRow[:-2] + "\n"
                trialInfo[7][3] = newRow
                await channelMessage.edit(
                    content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                await self.config.channel(trialChannel).trialInfo.set(trialInfo)
            else:
                await ctx.send(user.name + " wasn't signed up!")



    @listener()
    async def on_reaction_add(self, reaction, user):
        """stuff"""
        # check if on trial message
        # if is, run addsignup
        # remove reaction


    @listener()
    async def on_message(self, message):
        """stuff"""
        channels = await self.config.trialChannels()
        if len(message.content) == 0:
            return
        if message.channel.id in channels and message.author.id != 582583001838518285 and message.content[0] in ["+", "-"] and message.content.find("reserve") == -1:
            dd = ["+dd", "+dps", "+damage"]
            heal = ["+heal", "+healer"]
            tank = ["+tank"]
            reserve = ["+res", "+reserve"]

            trialInfo = await self.config.channel(message.channel).trialInfo()

            try:
                channelMessage = await message.channel.fetch_message(trialInfo[0])
            except discord.NotFound:
                await message.channel.send("No trial currently running")
                return

            try:
                for code in dd:
                    if code in message.content.replace(" ", "").lower():
                        while await self.config.inUse():
                            await asyncio.sleep(1)
                        await self.config.inUse.set(True)
                        trialInfo = await self.config.channel(message.channel).trialInfo()
                        if message.author.id in trialInfo[4] or message.author.id in trialInfo[5] or message.author.id in trialInfo[6]:
                            await message.channel.send(message.author.mention + " you're already signed up!")
                        else:
                            if len(trialInfo[4]) >= trialInfo[1]:
                                await message.channel.send(message.author.mention + " all DD spots are taken!")
                            else:
                                response = await message.channel.send(message.author.mention + " You have been signed up as a dd")
                                await message.add_reaction("👍")
                                trialInfo[4].append(message.author.id)
                                newRow = "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): "
                                for user in trialInfo[4]:
                                    newRow += self.bot.get_user(user).mention + ", "
                                newRow = newRow[:-2] + "\n"
                                trialInfo[7][1] = newRow
                                await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                                await self.config.channel(message.channel).trialInfo.set(trialInfo)
                                await asyncio.sleep(5)
                                await response.delete()

                        break

                for code in heal:
                    if code in message.content.replace(" ", "").lower():
                        while await self.config.inUse():
                            await asyncio.sleep(1)
                        await self.config.inUse.set(True)
                        trialInfo = await self.config.channel(message.channel).trialInfo()
                        if message.author.id in trialInfo[4] or message.author.id in trialInfo[5] or message.author.id in trialInfo[6]:
                            await message.channel.send(message.author.mention + " you're already signed up!")
                        else:
                            if len(trialInfo[5]) >= trialInfo[2]:
                                await message.channel.send(message.author.mention + " all healer spots are taken!")
                            else:
                                response = await message.channel.send(message.author.mention + " You have been signed up as a healer")
                                await message.add_reaction("👍")
                                trialInfo[5].append(message.author.id)
                                newRow = "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): "
                                for user in trialInfo[5]:
                                    newRow += self.bot.get_user(user).mention + ", "
                                newRow = newRow[:-2] + "\n"
                                trialInfo[7][2] = newRow
                                await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                                await self.config.channel(message.channel).trialInfo.set(trialInfo)
                                await asyncio.sleep(5)
                                await response.delete()

                        break

                for code in tank:
                    if code in message.content.replace(" ", "").lower():
                        while await self.config.inUse():
                            await asyncio.sleep(1)
                        await self.config.inUse.set(True)
                        trialInfo = await self.config.channel(message.channel).trialInfo()
                        if message.author.id in trialInfo[4] or message.author.id in trialInfo[5] or message.author.id in trialInfo[6]:
                            await message.channel.send(message.author.mention + " you're already signed up!")
                        else:
                            if len(trialInfo[6]) >= trialInfo[3]:
                                await message.channel.send(message.author.mention + " all tank spots are taken!")
                            else:
                                response = await message.channel.send(message.author.mention + " You have been signed up as a tank")
                                await message.add_reaction("👍")
                                trialInfo[6].append(message.author.id)
                                newRow = "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): "
                                for user in trialInfo[6]:
                                    newRow += self.bot.get_user(user).mention + ", "
                                newRow = newRow[:-2] + "\n"
                                trialInfo[7][3] = newRow
                                await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                                await self.config.channel(message.channel).trialInfo.set(trialInfo)
                                await asyncio.sleep(5)
                                await response.delete()
                        break

                dd = ["-dd", "-dps", "-damage"]
                heal = ["-heal", "-healer"]
                tank = ["-tank"]
                reserve = ["-res", "-reserve"]

                for code in dd:
                    if code in message.content.replace(" ", "").lower():
                        while await self.config.inUse():
                            await asyncio.sleep(1)
                        await self.config.inUse.set(True)
                        trialInfo = await self.config.channel(message.channel).trialInfo()
                        if message.author.id in trialInfo[4]:
                            await message.channel.send(message.author.mention + " You have been unsigned")
                            trialInfo[4].remove(message.author.id)
                            newRow = "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): "
                            for user in trialInfo[4]:
                                newRow += self.bot.get_user(user).mention + ", "
                            newRow = newRow[:-2] + "\n"
                            trialInfo[7][1] = newRow
                            await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                            await self.config.channel(message.channel).trialInfo.set(trialInfo)
                        else:
                            await message.channel.send(message.author.mention + " You weren't signed up!")

                        break

                for code in heal:
                    if code in message.content.replace(" ", "").lower():
                        while await self.config.inUse():
                            await asyncio.sleep(1)
                        await self.config.inUse.set(True)
                        trialInfo = await self.config.channel(message.channel).trialInfo()
                        if message.author.id in trialInfo[5]:
                            await message.channel.send(message.author.mention + " You have been unsigned")
                            trialInfo[5].remove(message.author.id)
                            newRow = "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): "
                            for user in trialInfo[5]:
                                newRow += self.bot.get_user(user).mention + ", "
                            newRow = newRow[:-2] + "\n"
                            trialInfo[7][2] = newRow
                            await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                            await self.config.channel(message.channel).trialInfo.set(trialInfo)
                        else:
                            await message.channel.send(message.author.mention + " You weren't signed up!")

                        break

                for code in tank:
                    if code in message.content.replace(" ", "").lower():
                        while await self.config.inUse():
                            await asyncio.sleep(1)
                        await self.config.inUse.set(True)
                        trialInfo = await self.config.channel(message.channel).trialInfo()
                        if message.author.id in trialInfo[6]:
                            await message.channel.send(message.author.mention + " You have been unsigned")
                            trialInfo[6].remove(message.author.id)
                            newRow = "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): "
                            for user in trialInfo[6]:
                                newRow += self.bot.get_user(user).mention + ", "
                            newRow = newRow[:-2] + "\n"
                            trialInfo[7][3] = newRow
                            await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                            await self.config.channel(message.channel).trialInfo.set(trialInfo)
                        else:
                            await message.channel.send(message.author.mention + " You weren't signed up!")

                        break
            except:
                await message.channel.send("Something went wrong")
            finally:
                await self.config.inUse.set(False)

