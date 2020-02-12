from __future__ import print_function
from redbot.core import commands
from redbot.core import Config


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
    async def trial(self, ctx, ddNum: int, healNum: int, tankNum: int):
        """Creates a trial"""
        trialChannel = ctx.guild.get_channel(517788758008004608)
        trialInfo = [0, ddNum, healNum, tankNum, [], [], []]
        trialMessage = ["Created a trial:\n",
                        "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): \n",
                        "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): \n",
                        "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): \n"]
        signupMessage = await ctx.send(trialMessage[0] + trialMessage[1] + trialMessage[2] + trialMessage[3])
        trialInfo[0] = signupMessage.id
        trialInfo.append(trialMessage)
        await self.config.trialInfo.set(trialInfo)

        # post message, store id
        # add reacts
        # start listener

    @commands.command()
    @commands.has_role("Officer")
    async def addsignup(self, user, role):
        """Adds a user to the trial"""
        trialChannel = self.bot.get_guild(285175143104380928).get_channel(517788758008004608)
        # checks if user is signed up
        # if they aren't, check validity
        # if valid, add to signup message
        # if not, send message with error

    @listener()
    async def on_reaction_add(self, reaction, user):
        """stuff"""
        # check if on trial message
        # if is, run addsignup
        # remove reaction

    @listener()
    async def on_message(self, message):
        """stuff"""
        if message.channel.id == 517788758008004608 and message.author.id != 582583001838518285:
            dd = ["+dd", "+dps", "+damage"]
            heal = ["+heal", "+healer"]
            tank = ["+tank"]
            reserve = ["+res", "+reserve"]

            for code in dd:
                if code in message.content.replace(" ", ""):
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
                                    await message.channel.send(message.author.mention + " You have been signed up as a dd")
                                    trialInfo[4].append(message.author.id)
                                    newRow = "DD (" + str(len(trialInfo[4])) + "/" + str(trialInfo[1]) + "): "
                                    for user in trialInfo[4]:
                                        newRow += self.bot.get_user(user).mention + ", "
                                    newRow = newRow[:-2] + "\n"
                                    trialInfo[7][1] = newRow
                                    await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][1] + trialInfo[7][2] + trialInfo[7][3])
                            if not found:
                                await message.channel.send(message.author.mention + " Sorry, there was an error")

                            await self.config.trialInfo.set(trialInfo)
                    break

            for code in heal:
                if code in message.content.replace(" ", ""):
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
                                    await message.channel.send(message.author.mention + " You have been signed up as a healer")
                                    trialInfo[5].append(message.author.id)
                                    newRow = "Heal (" + str(len(trialInfo[5])) + "/" + str(trialInfo[2]) + "): "
                                    for user in trialInfo[5]:
                                        newRow += self.bot.get_user(user).mention + ", "
                                    newRow = newRow[:-2] + "\n"
                                    trialInfo[7][2] = newRow
                                    await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][1] + trialInfo[7][2] + trialInfo[7][3])
                            if not found:
                                await message.channel.send(message.author.mention + " Sorry, there was an error")

                            await self.config.trialInfo.set(trialInfo)
                    break

            for code in tank:
                if code in message.content.replace(" ", ""):
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
                                    await message.channel.send(message.author.mention + " You have been signed up as a tank")
                                    trialInfo[6].append(message.author.id)
                                    newRow = "Tank (" + str(len(trialInfo[6])) + "/" + str(trialInfo[3]) + "): "
                                    for user in trialInfo[6]:
                                        newRow += self.bot.get_user(user).mention + ", "
                                    newRow = newRow[:-2] + "\n"
                                    trialInfo[7][3] = newRow
                                    await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][1] + trialInfo[7][2] + trialInfo[7][3])
                            if not found:
                                await message.channel.send(message.author.mention + " Sorry, there was an error")

                            await self.config.trialInfo.set(trialInfo)
                    break

            dd = ["-dd", "-dps", "-damage"]
            heal = ["-heal", "-healer"]
            tank = ["-tank"]
            reserve = ["-res", "-reserve"]

            for code in dd:
                if code in message.content.replace(" ", ""):
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
                                await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][1] + trialInfo[7][2] + trialInfo[7][3])
                        if not found:
                            await message.channel.send(message.author.mention + " Sorry, there was an error")
                        await self.config.trialInfo.set(trialInfo)
                    else:
                        await message.channel.send(message.author.mention + " You weren't signed up!")

                    break

            for code in heal:
                if code in message.content.replace(" ", ""):
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
                                await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][1] + trialInfo[7][2] + trialInfo[7][3])
                        if not found:
                            await message.channel.send(message.author.mention + " Sorry, there was an error")
                        await self.config.trialInfo.set(trialInfo)
                    else:
                        await message.channel.send(message.author.mention + " You weren't signed up!")

                    break

            for code in tank:
                if code in message.content.replace(" ", ""):
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
                                await channelMessage.edit(content=trialInfo[7][0] + trialInfo[7][1] + trialInfo[7][2] + trialInfo[7][3])
                        if not found:
                            await message.channel.send(message.author.mention + " Sorry, there was an error")
                        await self.config.trialInfo.set(trialInfo)
                    else:
                        await message.channel.send(message.author.mention + " You weren't signed up!")

                    break


        # check if valid +code
        # if is, run addsignup
        # react with thumbs up
