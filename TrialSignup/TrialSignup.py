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
        signupMessage = await ctx.send("Created a trial")
        trialInfo = [signupMessage.id, ddNum, healNum, tankNum, [], [], []]
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
                            await message.channel.send(message.author.mention + " You have been signed up as a dd")
                            trialInfo[4].append(message.author.id)
                            # await trialInfo[0].edit("Created a trial and now there's signups")
                            await self.config.trialInfo.set(trialInfo)
                    break

            dd = ["-dd", "-dps", "-damage"]
            heal = ["-heal", "-healer"]
            tank = ["-tank"]
            reserve = ["-res", "-reserve"]

            for code in dd:
                if code in message.content.replace(" ", ""):
                    trialInfo = await self.config.trialInfo()
                    if message.author.id in trialInfo[4] or message.author.id in trialInfo[5] or message.author.id in \
                            trialInfo[6]:
                        await message.channel.send(message.author.mention + " You have been unsigned")
                        trialInfo[4].remove(message.author.id)
                        # await trialInfo[0].edit("Created a trial and now there's signups")
                        await self.config.trialInfo.set(trialInfo)
                    else:
                        await message.channel.send(message.author.mention + " You weren't signed up!")

                    break

        # check if valid +code
        # if is, run addsignup
        # react with thumbs up
