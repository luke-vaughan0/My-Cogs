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

        default_guild = {
            "trialInfo": []
        }

        self.config = Config.get_conf(self, identifier=6457)
        self.config.register_guild(**default_guild)


    @commands.command()
    @commands.has_role("Officer")
    async def trial(self, ctx, tankNum: int, healNum: int, ddNum: int, description: str = "Created a trial:"):
        """Creates a trial"""
        trialInfo = await self.config.trialInfo()
        if trialInfo[0] != 0:
            await ctx.send("You must end the current trial before creating a new one!")
        else:
            trialChannel = ctx.guild.get_channel(675461735968276506)
            trialInfo = [0, ddNum, healNum, tankNum, [], [], []]
            trialMessage = [description+"\n",
                            "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): \n",
                            "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): \n",
                            "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): \n"]
            signupMessage = await ctx.send(trialMessage[0] + trialMessage[3] + trialMessage[2] + trialMessage[1])
            trialInfo[0] = signupMessage.id
            trialInfo.append(trialMessage)
            await self.config.trialInfo.set(trialInfo)


    @commands.command()
    @commands.has_role("Officer")
    async def endtrial(self, ctx):
        """Ends current trial"""
        trialInfo = [0, 1, 1, 1, [], [], []]
        await ctx.send("Current trial ended")
        await self.config.trialInfo.set(trialInfo)


    @commands.command()
    @commands.has_role("Officer")
    async def addsignup(self, ctx, user: discord.Member, role):
        """Adds a user to the trial"""
        dd = ["dd", "dps", "damage"]
        heal = ["heal", "healer"]
        tank = ["tank"]
        trialChannel = self.bot.get_guild(285175143104380928).get_channel(675461735968276506)
        trialInfo = await self.config.trialInfo()
        if role in dd:
            if user.id in trialInfo[4] or user.id in trialInfo[5] or user.id in trialInfo[6]:
                await ctx.send(user.name + " is already signed up!")
            else:
                if len(trialInfo[4]) >= trialInfo[1]:
                    await ctx.send("All DD spots are taken!")
                else:
                    found = False
                    async for channelMessage in trialChannel.history():
                        if channelMessage.id == trialInfo[0]:
                            found = True
                            await ctx.send(user.name + " has been signed up as a dd")
                            trialInfo[4].append(user.id)
                            newRow = "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): "
                            for users in trialInfo[4]:
                                newRow += self.bot.get_user(users).mention + ", "
                            newRow = newRow[:-2] + "\n"
                            trialInfo[7][1] = newRow
                            await channelMessage.edit(
                                content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                    if not found:
                        await ctx.send("No trial currently running")

                    await self.config.trialInfo.set(trialInfo)


        if role in heal:
            if user.id in trialInfo[4] or user.id in trialInfo[5] or user.id in trialInfo[6]:
                await ctx.send(user.name + " is already signed up!")
            else:
                if len(trialInfo[5]) >= trialInfo[2]:
                    await ctx.send("All healer spots are taken!")
                else:
                    found = False
                    async for channelMessage in trialChannel.history():
                        if channelMessage.id == trialInfo[0]:
                            found = True
                            await ctx.send(user.name + " has been signed up as a healer")
                            trialInfo[5].append(user.id)
                            newRow = "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): "
                            for users in trialInfo[5]:
                                newRow += self.bot.get_user(users).mention + ", "
                            newRow = newRow[:-2] + "\n"
                            trialInfo[7][2] = newRow
                            await channelMessage.edit(
                                content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                    if not found:
                        await ctx.send("No trial currently running")

                    await self.config.trialInfo.set(trialInfo)


        if role in tank:
            if user.id in trialInfo[4] or user.id in trialInfo[5] or user.id in trialInfo[6]:
                await ctx.send(user.name + " is already signed up!")
            else:
                if len(trialInfo[6]) >= trialInfo[3]:
                    await ctx.send("All tank spots are taken!")
                else:
                    found = False
                    async for channelMessage in trialChannel.history():
                        if channelMessage.id == trialInfo[0]:
                            found = True
                            await ctx.send(user.name + " has been signed up as a tank")
                            trialInfo[6].append(user.id)
                            newRow = "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): "
                            for users in trialInfo[6]:
                                newRow += self.bot.get_user(users).mention + ", "
                            newRow = newRow[:-2] + "\n"
                            trialInfo[7][3] = newRow
                            await channelMessage.edit(
                                content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                    if not found:
                        await ctx.send("No trial currently running")

                    await self.config.trialInfo.set(trialInfo)

    @commands.command()
    @commands.has_role("Officer")
    async def removesignup(self, ctx, user: discord.Member, role):
        """Removes a user from the trial"""
        dd = ["dd", "dps", "damage"]
        heal = ["heal", "healer"]
        tank = ["tank"]
        trialChannel = self.bot.get_guild(285175143104380928).get_channel(675461735968276506)
        trialInfo = await self.config.trialInfo()

        if role in dd:
            if user.id in trialInfo[4]:
                found = False
                async for channelMessage in trialChannel.history():
                    if channelMessage.id == trialInfo[0]:
                        found = True
                        await ctx.send(user.name + " has been unsigned")
                        trialInfo[4].remove(user.id)
                        newRow = "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): "
                        for users in trialInfo[4]:
                            newRow += self.bot.get_user(users).mention + ", "
                        newRow = newRow[:-2] + "\n"
                        trialInfo[7][1] = newRow
                        await channelMessage.edit(
                            content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                if not found:
                    await ctx.send("No trial currently running")
                await self.config.trialInfo.set(trialInfo)
            else:
                await ctx.send(user.name + " wasn't signed up!")



        if role in heal:
            if user.id in trialInfo[5]:
                found = False
                async for channelMessage in trialChannel.history():
                    if channelMessage.id == trialInfo[0]:
                        found = True
                        await ctx.send(user.name + " has been unsigned")
                        trialInfo[5].remove(user.id)
                        newRow = "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): "
                        for users in trialInfo[5]:
                            newRow += self.bot.get_user(users).mention + ", "
                        newRow = newRow[:-2] + "\n"
                        trialInfo[7][2] = newRow
                        await channelMessage.edit(
                            content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                if not found:
                    await ctx.send("No trial currently running")
                await self.config.trialInfo.set(trialInfo)
            else:
                await ctx.send(user.name + " wasn't signed up!")



        if role in tank:
            if user.id in trialInfo[6]:
                found = False
                async for channelMessage in trialChannel.history():
                    if channelMessage.id == trialInfo[0]:
                        found = True
                        await ctx.send(user.name + " has been unsigned")
                        trialInfo[6].remove(user.id)
                        newRow = "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): "
                        for users in trialInfo[6]:
                            newRow += self.bot.get_user(users).mention + ", "
                        newRow = newRow[:-2] + "\n"
                        trialInfo[7][3] = newRow
                        await channelMessage.edit(
                            content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                if not found:
                    await ctx.send("No trial currently running")
                await self.config.trialInfo.set(trialInfo)
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
        if message.channel.id == 675461735968276506 and message.author.id != 582583001838518285 and message.content[0] in ["+", "-"]:
            dd = ["+dd", "+dps", "+damage"]
            heal = ["+heal", "+healer"]
            tank = ["+tank"]
            reserve = ["+res", "+reserve"]

            for code in dd:
                if code in message.content.replace(" ", "").lower():
                    trialInfo = await self.config.trialInfo()
                    if message.author.id in trialInfo[4] or message.author.id in trialInfo[5] or message.author.id in trialInfo[6]:
                        await message.channel.send(message.author.mention + " you're already signed up!")
                    else:
                        if len(trialInfo[4]) >= trialInfo[1]:
                            await message.channel.send(message.author.mention + " all DD spots are taken!")
                        else:
                            found = False
                            async for channelMessage in message.channel.history():
                                if channelMessage.id == trialInfo[0]:
                                    found = True
                                    response = await message.channel.send(message.author.mention + " You have been signed up as a dd")
                                    await message.add_reaction("👍")
                                    trialInfo[4].append(message.author.id)
                                    newRow = "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): "
                                    for user in trialInfo[4]:
                                        newRow += self.bot.get_user(user).mention + ", "
                                    newRow = newRow[:-2] + "\n"
                                    trialInfo[7][1] = newRow
                                    await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                                    await self.config.trialInfo.set(trialInfo)
                                    await asyncio.sleep(5)
                                    await response.delete()
                            if not found:
                                await message.channel.send(message.author.mention + " No trial currently running")


                    break

            for code in heal:
                if code in message.content.replace(" ", "").lower():
                    trialInfo = await self.config.trialInfo()
                    if message.author.id in trialInfo[4] or message.author.id in trialInfo[5] or message.author.id in trialInfo[6]:
                        await message.channel.send(message.author.mention + " you're already signed up!")
                    else:
                        if len(trialInfo[5]) >= trialInfo[2]:
                            await message.channel.send(message.author.mention + " all healer spots are taken!")
                        else:
                            found = False
                            async for channelMessage in message.channel.history():
                                if channelMessage.id == trialInfo[0]:
                                    found = True
                                    response = await message.channel.send(message.author.mention + " You have been signed up as a healer")
                                    await message.add_reaction("👍")
                                    trialInfo[5].append(message.author.id)
                                    newRow = "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): "
                                    for user in trialInfo[5]:
                                        newRow += self.bot.get_user(user).mention + ", "
                                    newRow = newRow[:-2] + "\n"
                                    trialInfo[7][2] = newRow
                                    await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                                    await self.config.trialInfo.set(trialInfo)
                                    await asyncio.sleep(5)
                                    await response.delete()
                            if not found:
                                await message.channel.send(message.author.mention + " No trial currently running")

                    break

            for code in tank:
                if code in message.content.replace(" ", "").lower():
                    trialInfo = await self.config.trialInfo()
                    if message.author.id in trialInfo[4] or message.author.id in trialInfo[5] or message.author.id in trialInfo[6]:
                        await message.channel.send(message.author.mention + " you're already signed up!")
                    else:
                        if len(trialInfo[6]) >= trialInfo[3]:
                            await message.channel.send(message.author.mention + " all tank spots are taken!")
                        else:
                            found = False
                            async for channelMessage in message.channel.history():
                                if channelMessage.id == trialInfo[0]:
                                    found = True
                                    response = await message.channel.send(message.author.mention + " You have been signed up as a tank")
                                    await message.add_reaction("👍")
                                    trialInfo[6].append(message.author.id)
                                    newRow = "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): "
                                    for user in trialInfo[6]:
                                        newRow += self.bot.get_user(user).mention + ", "
                                    newRow = newRow[:-2] + "\n"
                                    trialInfo[7][3] = newRow
                                    await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                                    await self.config.trialInfo.set(trialInfo)
                                    await asyncio.sleep(5)
                                    await response.delete()
                            if not found:
                                await message.channel.send(message.author.mention + " No trial currently running")
                    break

            dd = ["-dd", "-dps", "-damage"]
            heal = ["-heal", "-healer"]
            tank = ["-tank"]
            reserve = ["-res", "-reserve"]

            for code in dd:
                if code in message.content.replace(" ", "").lower():
                    trialInfo = await self.config.trialInfo()
                    if message.author.id in trialInfo[4]:
                        found = False
                        async for channelMessage in message.channel.history():
                            if channelMessage.id == trialInfo[0]:
                                found = True
                                await message.channel.send(message.author.mention + " You have been unsigned")
                                trialInfo[4].remove(message.author.id)
                                newRow = "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): "
                                for user in trialInfo[4]:
                                    newRow += self.bot.get_user(user).mention + ", "
                                newRow = newRow[:-2] + "\n"
                                trialInfo[7][1] = newRow
                                await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                        if not found:
                            await message.channel.send(message.author.mention + " No trial currently running")
                        await self.config.trialInfo.set(trialInfo)
                    else:
                        await message.channel.send(message.author.mention + " You weren't signed up!")

                    break

            for code in heal:
                if code in message.content.replace(" ", "").lower():
                    trialInfo = await self.config.trialInfo()
                    if message.author.id in trialInfo[5]:
                        found = False
                        async for channelMessage in message.channel.history():
                            if channelMessage.id == trialInfo[0]:
                                found = True
                                await message.channel.send(message.author.mention + " You have been unsigned")
                                trialInfo[5].remove(message.author.id)
                                newRow = "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): "
                                for user in trialInfo[5]:
                                    newRow += self.bot.get_user(user).mention + ", "
                                newRow = newRow[:-2] + "\n"
                                trialInfo[7][2] = newRow
                                await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                        if not found:
                            await message.channel.send(message.author.mention + " No trial currently running")
                        await self.config.trialInfo.set(trialInfo)
                    else:
                        await message.channel.send(message.author.mention + " You weren't signed up!")

                    break

            for code in tank:
                if code in message.content.replace(" ", "").lower():
                    trialInfo = await self.config.trialInfo()
                    if message.author.id in trialInfo[6]:
                        found = False
                        async for channelMessage in message.channel.history():
                            if channelMessage.id == trialInfo[0]:
                                found = True
                                await message.channel.send(message.author.mention + " You have been unsigned")
                                trialInfo[6].remove(message.author.id)
                                newRow = "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): "
                                for user in trialInfo[6]:
                                    newRow += self.bot.get_user(user).mention + ", "
                                newRow = newRow[:-2] + "\n"
                                trialInfo[7][3] = newRow
                                await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][3] + trialInfo[7][2] + trialInfo[7][1])
                        if not found:
                            await message.channel.send(message.author.mention + " No trial currently running")
                        await self.config.trialInfo.set(trialInfo)
                    else:
                        await message.channel.send(message.author.mention + " You weren't signed up!")

                    break
