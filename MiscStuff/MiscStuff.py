from __future__ import print_function
from redbot.core import commands
from redbot.core import Config
import os
import datetime
import requests
import random

listener = getattr(commands.Cog, "listener", None)  # Trusty + Sinbad
if listener is None:

    def listener(name=None):
        return lambda x: x


class MiscStuff(commands.Cog):
    """Just misc commands I wanted to add"""

    def __init__(self, bot):
        self.bot = bot

        if os.path.exists('CustomAlerts.txt'):
            with open("CustomAlerts.txt", "r") as f:
                alertList = [line.split(",") for line in f]
                for item in alertList:
                    item[-1] = item[-1].rstrip("\n")
        else:
            with open("CustomAlerts.txt", "w"):
                alertList = []
        
        self.config = Config.get_conf(self, identifier=6457)
        self.config.register_global(
            alerts=alertList
        )
        

    @commands.command()
    async def joindate(self, ctx):
        """Prints the date you joined this server"""

        joinDate = ctx.author.joined_at.date()

        await ctx.send(str(joinDate))

    @commands.command()
    async def horoscope(self, ctx):
        """Shows your 100% accurate horoscope for today"""

        url = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign="
        url += str((ctx.author.id % 12)+1)

        response = requests.get(url)

        bonus = ['One of the leaders got you a surprise. They will definitely remember to send you it. Definitely.',
                    'In Cards Against Humanity, you will play a card that you think is funny, but nobody will laugh when it is read out. ',
                    'You glow with your own special light. You should really lay off the radium. ',
                    'You inspire strong feelings in everyone you meet. And strong smells too. ',
                    'Club Penguin will return, but for every time you tell someone, it is pushed back another year. ',
                    'You need to drink more water.',
                    'It doesn’t take a rocket scientist to figure out what’s wrong with you. It takes about three. ',
                    'Avoid the Sausage.',
                    'Romance is blossoming between two guildies. You are neither of them. ',
                    'You’re not the type of person who lets social conventions dictate how you live your life. I know, I’ve seen your #community-general chat history.',
                    'You’ll finally find a person who loves you for who you are, but unfortunately, they’re a bit of a cunt. ',
                    'It’s a great time to find romance in the guild if you’re the sort who thinks that’s even close to a good idea. ',
                    'Posture check!',
                    'This week, the guild will notice that thing you’ve been trying to hide. ',
                    'Now is the best time to post a questionable meme. Definitely. Do it. ',
                    'Your pessimism is usually misplaced, but it’ll be perfectly appropriate in #community-general next Thursday. ',
                    'We know about that weird Discord server you joined. We promise not to tell.',
                    'All your hard work will finally pay off, just not for you.',
                    'It’s really fun to destroy things. We won’t judge.',
                    'If you type out your password, it will appear as stars. Look: ************. You try it!']

        horoscope = "Here is your horoscope for today, " + ctx.author.name + "\n"

        try:
            if random.randint(0, 50) == 0:
                horoscope += bonus[random.randint(0, len(bonus)-1)]
            else:
                horoscope += response.text[response.text.find('</strong> - ') + 12:response.text.find("</p>")]
            await ctx.send(horoscope)

        except:
            print(horoscope)
            horoscope = "Hmm, having some problems with the crystal balls, try again later"
            await ctx.send(horoscope)



    @commands.command()
    async def oldest(self, ctx, role=None):
        """Lists the oldest users with an optional role"""
        print(role)
        roleID = 0
        for item in ctx.guild.roles:
            if item.name.lower() == role.lower():
                roleID = item

        if roleID != 0 and role is not None:
            joinDates = []
            for user in ctx.guild.members:
                if role is None:
                    if user.top_role.name != "Community Member":
                        joinDates.append([user.joined_at, str(user)])
                else:
                    if roleID in user.roles:
                        joinDates.append([user.joined_at, str(user)])

            joinDates.sort()
            if len(joinDates) > 10:
                message = "The 10 oldest users with roles are:\n"
                for i in range(0, 10):
                    message += joinDates[i][1] + ", " + str(joinDates[i][0].date()) + "\n"
            else:
                message = "The oldest users with roles are:\n"
                for i in range(0, len(joinDates)):
                    message += joinDates[i][1] + ", " + str(joinDates[i][0].date()) + "\n"
        else:
            message = "Couldn't find that role"

        await ctx.send(message)


    @commands.command()
    async def weekdays(self, ctx):
        """Shows the days of the week people joined on the most"""

        days = [0, 0, 0, 0, 0, 0, 0]
        for member in ctx.guild.members:
            joinDay = member.joined_at.weekday()

            days[joinDay] = days[joinDay]+1

        message = "People that joined the server joined on these days:\n" \
                  "Monday: " + str(days[0]) + "\n" + "Tuesday: " + str(days[1]) + "\n" + \
                  "Wednesday: " + str(days[2]) + "\n" + "Thursday: " + str(days[3]) + "\n" + \
                  "Friday: " + str(days[4]) + "\n" + "Saturday: " + str(days[5]) + "\n" + \
                  "Sunday: " + str(days[6]) + "\n"

        await ctx.send(message)


    @commands.command()
    async def alert(self, ctx, *message):
        """This does stuff!"""

        if os.path.exists('CustomAlerts.txt'):
            with open("CustomAlerts.txt", "r") as f:
                alertList = [line.split(",") for line in f]
                for item in alertList:
                    item[-1] = item[-1].rstrip("\n")
        else:
            with open("CustomAlerts.txt", "w"):
                alertList = []

        userRow = -1

        for i, item in enumerate(alertList):
            if str(ctx.author.id) == item[0]:
                userRow = i
                break
        if userRow == -1:
            alertList.append([str(ctx.author.id)])  
            userRow = len(alertList)-1

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
                
        with open("CustomAlerts.txt", "w") as f:
            fileWrite = ""
            for i in alertList:
                for j in i:
                    fileWrite = fileWrite+j+","
                fileWrite = fileWrite[:-1]+"\n"
            f.write(fileWrite)

        await self.config.alerts.set(alertList)

        await ctx.send(sendMessage)


    @listener()
    async def on_message(self, message):
        # delete set messages
        if message.author.id == 582583001838518285 and message.content == "That command is disabled.":
            await message.delete()

        # send messages on alerts
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
                        linkURL = "https://discordapp.com/channels/" + \
                                  str(message.guild.id) + "/" + \
                                  str(message.channel.id) + "/" + \
                                  str(message.id)
                        alertMessage = str(message.author.name) + " mentioned " + j + " in " + \
                                       str(message.channel.name) + ":\n" + \
                                       message.content + "\nLink to message: " + linkURL
                        await userDM.send(alertMessage)
                        print("["+str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) +
                              "] Sent alert to", userToDM)
                    except AttributeError:
                        pass
                    break
