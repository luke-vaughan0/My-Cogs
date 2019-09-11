from __future__ import print_function
from redbot.core import commands
from redbot.core import Config
import os
import datetime

listener = getattr(commands.Cog, "listener", None)  # Trusty + Sinbad
if listener is None:

    def listener(name=None):
        return lambda x: x

class MiscStuff(commands.Cog):
    """Just misc commands I wanted to add"""

    def __init__(self, bot):
        self.bot = bot

        if os.path.exists('CustomAlerts.txt'):
            with open("CustomAlerts.txt","r") as f:
                alertList = [line.split(",") for line in f]
                for item in alertList:
                    item[-1] = item[-1].rstrip("\n")
        else:
            with open("CustomAlerts.txt","w") as f:
                alertList = []
        
        self.config = Config.get_conf(self, identifier=6457)
        self.config.register_global(
            alerts = alertList
        )
        


    @commands.command()
    async def joindate(self, ctx):
        """This does stuff!"""

        joinDate = ctx.author.joined_at.date()

        await ctx.send(str(joinDate))


    @commands.command()
    async def weekdays(self, ctx):
        """This does stuff!"""

        esorole = ctx.guild.get_role(356874800502931457)
        days = [0, 0, 0, 0, 0, 0, 0]
        for member in ctx.guild.members:
            joinDay = member.joined_at.weekday()

            days[joinDay] = days[joinDay]+1

        message = "Monday: " + str(days[0]) + "\n" + "Tuesday: " + str(days[1]) + "\n" + "Wednesday: " + str(days[2]) + "\n" + "Thursday: " + str(days[3]) + "\n" + "Friday: " + str(days[4]) + "\n" + "Saturday: " + str(days[5]) + "\n" + "Sunday: " + str(days[6]) + "\n"
        await ctx.send(message)

    @commands.command()
    async def alert(self, ctx, *message):
        """This does stuff!"""

        if os.path.exists('CustomAlerts.txt'):
            with open("CustomAlerts.txt","r") as f:
                alertList = [line.split(",") for line in f]
                for item in alertList:
                    item[-1] = item[-1].rstrip("\n")
        else:
            with open("CustomAlerts.txt","w") as f:
                alertList = []

        def addNewlines(things):
            for item in things:
                yield item
                yield '\n'

        userRow = -1

        for i, item in enumerate(alertList):
            if str(ctx.author.id) == item[0]:
                userRow = i
                break
        if userRow == -1:
            alertList.append([str(ctx.author.id)])  
            userRow = len(alertList)-1

        sendMessage = "test"

        if message == ():
            sendMessage = "Your Alerts:\n"
            for item in alertList[userRow][1:]:
                sendMessage = sendMessage+item+", "
            sendMessage = sendMessage[:-2]
        else:
            temp = tuple(message)
            message = ""
            for item in temp:
                message = message + item + " "
            message = message[:-1]
            if message in alertList[userRow][1:]:
                alertList[userRow].remove(message)
                sendMessage = message + " removed"
            else:
                alertList[userRow].append(message)
                sendMessage = message + " added"
                
        with open("CustomAlerts.txt","w") as f:
            fileWrite = ""
            for i in alertList:
                for j in i:
                    fileWrite = fileWrite+j+","
                fileWrite = fileWrite[:-1]+"\n"
            f.write(fileWrite)

        await self.config.alerts.set(alertList)
        

        await ctx.send(sendMessage)

##    @commands.command()
##    async def leaderboard(self, ctx):
##        """This does stuff!"""
##
##        esorole = ctx.guild.get_role(356874800502931457)
##
##
##        async with ctx.typing():
##            messages = await ctx.channel.history(limit=100000).flatten()
##        count = 0
##        for message in messages:
##            if message.author.id == ctx.author.id:
##                count += 1
##
##
##        await ctx.send(count)


    @listener()
    async def on_message(self, message):
        if message.author.id == 582583001838518285 and message.content == "That command is disabled.":
            await message.delete()
        alertList = await self.config.alerts()
        for i in alertList:
            for j in i[1:]:
                if message.author.id == int(i[0]):
                    break
                if message.content.lower().find(j.lower()) != -1:
                    userToDM = self.bot.get_user(int(i[0]))
                    await userToDM.create_dm()
                    userDM = userToDM.dm_channel
                    try:
                        linkURL = "https://discordapp.com/channels/" + str(message.guild.id) + "/" + str(message.channel.id) + "/" + str(message.id)
                        alertMessage = str(message.author.name) + " mentioned "+ j + " in " + str(message.channel.name) + ":\n" + message.content + "\nLink to message: " + linkURL
                        await userDM.send(alertMessage)
                        print("["+str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)+"] Sent alert to",userToDM)
                    except AttributeError:
                        pass
                    break
                

