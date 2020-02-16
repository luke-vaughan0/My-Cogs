from __future__ import print_function
from redbot.core import commands
from redbot.core import Config
import datetime
import requests
import random
import discord
import typing
import asyncio
import time
import copy

listener = getattr(commands.Cog, "listener", None)  # Trusty + Sinbad
if listener is None:

    def listener(name=None):
        return lambda x: x


class MiscStuff(commands.Cog):
    """Just misc commands I wanted to add"""

    def __init__(self, bot):
        self.bot = bot

        default_global = {
            "alerts": [],
            "filters": []
        }

        default_guild = {
            "quotes": []
        }
        
        self.config = Config.get_conf(self, identifier=6457)
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)
        

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
    @commands.has_role("Officer")
    async def pingrole(self, ctx, role: discord.Role, duration: int = 120):
        """Turns on role pings for this role for the entered time"""
        if duration > 300:
            duration = 300
        if role.mentionable:
            await ctx.send("This role is already mentionable")
        else:
            await role.edit(mentionable=True)
            await ctx.send(role.name + " is now mentionable for " + str(duration) + " seconds")
            await asyncio.sleep(duration)
            await role.edit(mentionable=False)
            await ctx.send(role.name + " is no longer mentionable")




    @commands.command()
    async def alert(self, ctx, *message):
        """Allows you to get notifications when particular words or phrases are mentioned"""

        alertList = await self.config.alerts()

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
                if len(alertList[userRow]) == 1:
                    alertList.pop(userRow)
                sendMessage = message + " removed"
            else:
                alertList[userRow].append(message)
                sendMessage = message + " added"

        await self.config.alerts.set(alertList)

        await ctx.send(sendMessage)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def filter(self, ctx, message, role: discord.Role):
        """Filters reactions on a message to a particular role"""

        filterList = await self.config.filters()

        messageRow = -1

        for i, item in enumerate(filterList):
            if message == item[0]:
                messageRow = i
                break

        if messageRow == -1:
            filterList.append([message])
            messageRow = len(filterList) - 1

        if str(role.id) in filterList[messageRow][1:]:
            filterList[messageRow].remove(str(role.id))
            if len(filterList[messageRow]) == 1:
                filterList.pop(messageRow)
            sendMessage = role.name + " removed"
        else:
            filterList[messageRow].append(str(role.id))
            sendMessage = role.name + " added"

        await self.config.filters.set(filterList)

        await ctx.send(sendMessage)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def filternow(self, ctx, messageid: int, role: discord.Role, channel: discord.TextChannel = None):
        """One time removal of all incorrect reactions"""
        reactsRemoved = 0
        if not channel:
            channel = ctx.channel
        async for message in channel.history(limit=200):
            if message.id == messageid:
                for reaction in message.reactions:
                    async for user in reaction.users():
                        if role not in user.roles:
                            print("removed a reaction from", user.name)
                            reactsRemoved += 1
                            await reaction.remove(user)
#
        await ctx.send("Removed " + str(reactsRemoved) + " reactions")



    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearupto(self, ctx, clearPoint: discord.Message):
        """Deletes all messages up to a specified point"""
        print("Working")
        messages = await ctx.channel.history(limit=101).flatten()
        messagesToDelete = []
        found = False
        for message in messages:
            if message.id == clearPoint.id:
                found = True
                print("gottem")
                break
            else:
                messagesToDelete.append(message)
        print("still working")
        if found:
            warning = await ctx.send("Are you sure you want to delete " + str(
                len(messagesToDelete)) + " messages up to message beginning `" + clearPoint.content[:10] + "`?\nType Y to accept")

            def check(m):
                return m.content == 'Y' and m.channel == ctx.channel
            try:
                reply = await self.bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                errorMessage = await ctx.send("You didn't respond fast enough")
                await asyncio.sleep(3)
                await warning.delete()
                await ctx.message.delete()
                await errorMessage.delete()
            else:
                await reply.delete()
                await warning.delete()
                await ctx.channel.delete_messages(messagesToDelete)

        else:
            await ctx.send("Couldn't find a message to clear up to")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearuser(self, ctx, member: discord.Member, limit: int):
        """Deletes all messages from a user"""
        messages = await ctx.channel.history(limit=limit).flatten()
        messagesToDelete = []
        for message in messages:
            if message.author == member:
                messagesToDelete.append(message)
        await ctx.channel.delete_messages(messagesToDelete)



    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearbetween(self, ctx, start: discord.Message, end: discord.Message):
        """Deletes all messages between two messages"""
        print("Working")
        messages = await ctx.channel.history(limit=101).flatten()
        messagesToDelete = []
        if start.created_at < end.created_at:
            temp = start
            start = copy.copy(end)
            end = copy.copy(temp)
        foundStart = False
        foundEnd = False
        for message in messages:
            if not foundStart:
                if message.id == start.id:
                    foundStart = True
                    print("gottem")
            else:
                if message.id == end.id:
                    foundEnd = True
                    print("gottem")
                    break
                else:
                    messagesToDelete.append(message)
        print("still working")
        if foundEnd:
            warning = await ctx.send("Are you sure you want to delete " + str(
                len(messagesToDelete)) + " messages between `" + start.content[:10] + "` and " + end.content[:10] + "`?\nType Y to accept")

            def check(m):
                return m.content == 'Y' and m.channel == ctx.channel

            try:
                reply = await self.bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                errorMessage = await ctx.send("You didn't respond fast enough")
                await asyncio.sleep(3)
                await warning.delete()
                await ctx.message.delete()
                await errorMessage.delete()
            else:
                await reply.delete()
                await warning.delete()
                await ctx.message.delete()
                await ctx.channel.delete_messages(messagesToDelete)

        else:
            await ctx.send("Couldn't find one of the messages to clear between")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def slowclearbetween(self, ctx, start: discord.Message, end: discord.Message):
        """Deletes all messages between two messages, slowly"""
        print("Working")
        messages = await ctx.channel.history(limit=101).flatten()
        messagesToDelete = []
        if start.created_at < end.created_at:
            temp = start
            start = copy.copy(end)
            end = copy.copy(temp)
        foundStart = False
        foundEnd = False
        for message in messages:
            if not foundStart:
                if message.id == start.id:
                    foundStart = True
                    print("gottem")
            else:
                if message.id == end.id:
                    foundEnd = True
                    print("gottem")
                    break
                else:
                    messagesToDelete.append(message)
        print("still working")
        if foundEnd:
            warning = await ctx.send("Are you sure you want to delete " + str(
                len(messagesToDelete)) + " messages between `" + start.content[:10] + "` and " + end.content[
                                                                                                 :10] + "`?\nType Y to accept")

            def check(m):
                return m.content == 'Y' and m.channel == ctx.channel

            try:
                reply = await self.bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                errorMessage = await ctx.send("You didn't respond fast enough")
                await asyncio.sleep(3)
                await warning.delete()
                await ctx.message.delete()
                await errorMessage.delete()
            else:
                await reply.delete()
                await warning.delete()
                await ctx.message.delete()
                if len(messagesToDelete) > 30:
                    errorMessage = await ctx.send("Sorry, that's too many messages to slow delete")
                    await asyncio.sleep(3)
                    await errorMessage.delete()
                else:
                    for message in messagesToDelete:
                        await message.delete()


        else:
            await ctx.send("Couldn't find one of the messages to clear between")


    @commands.command()
    async def emoteid(self, ctx, emote: discord.Emoji):
        """Returns an emote ID"""
        await ctx.send(emote.id)


    @commands.command()
    async def addquote(self, ctx, user: typing.Union[discord.Member, str], *message):
        quoteList = await self.config.guild(ctx.guild).quotes()
        temp = tuple(message)
        message = ""
        for item in temp:
            message = message + item + " "
        message = message[:-1]
        error = False

        if message[:1] == '"' and message[-1:] == '"':
            message = message[1:-1]

        if type(user) == str:
            warning = await ctx.send("This user is not on the server. Do you wish to continue?\nType Y to continue")


            def check(m):
                return m.content == 'Y' and m.channel == ctx.channel

            try:
                reply = await self.bot.wait_for('message', timeout=10.0, check=check)
                await reply.delete()

            except asyncio.TimeoutError:
                await ctx.send("No response given, quote was not added")
                error = True
            await warning.delete()

        if not error:
            if type(user) != str:
                quoteList.append([int(user.id), message, time.strftime("%d/%m/%y")])
            else:
                quoteList.append([str(user), message, time.strftime("%d/%m/%y")])
            await self.config.guild(ctx.guild).quotes.set(quoteList)

            await ctx.send("Quote added")

    @commands.command()
    async def quotelist(self, ctx, check: typing.Union[discord.Member, str] = ""):
        quoteList = await self.config.guild(ctx.guild).quotes()
        message = ""
        search = [""]
        if check != "":
            if type(check) == discord.Member:
                search = ["User", check.id]
            elif type(check) == str and not check.isdigit():
                search = ["User", check]
            elif len(check) == 4 or len(check) == 2:
                search = ["Year", check[-2:]]

        long = False
        for i, quote in enumerate(quoteList):
            if search[0] == "User":
                if search[1] != quote[0]:
                    continue
            elif search[0] == "Year":
                if search[1] != quote[2][-2:]:
                    continue

            message = message + str(i+1) + ') "' + quote[1] + '" - '

            if type(quote[0]) == int:
                try:
                    message = message + ctx.guild.get_member(quote[0]).nick
                except TypeError:
                    message = message + self.bot.get_user(quote[0]).name
            else:
                message = message + quote[0]

            message = message + ", 20" + quote[2][-2:] + "\n"

            if len(message) > 1800:
                long = True
                await ctx.send(message)
                message = ""
        if message == "" and not long:
            message = "No quotes found"
            if search[0] != "":
                message = message + " for " + search[0] + " " + search[1]
        await ctx.send(message)

    @commands.command()
    @commands.is_owner()
    async def delquote(self, ctx, quoteToDel: int):
        quoteList = await self.config.guild(ctx.guild).quotes()

        warning = await ctx.send("You are about to delete quote \"" + quoteList[quoteToDel][1] + "\", do you wish to continue?")

        def check(m):
            return m.content == 'Y' and m.channel == ctx.channel

        try:
            reply = await self.bot.wait_for('message', timeout=10.0, check=check)
            await reply.delete()
            quoteList.pop(quoteToDel)
            await self.config.guild(ctx.guild).quotes.set(quoteList)

        except asyncio.TimeoutError:
            end = await ctx.send("No response given, quote was not deleted")
            await asyncio.sleep(3)
            await end.delete()
            await ctx.delete()
        await warning.delete()

    @commands.command()
    async def minesweepers(self, ctx, size: int = 10, mines: int = 8):
        """Generates a minesweepers board"""

        board = [["" for x in range(size)] for y in range(size)]
        emotes = {"M": ":bomb:", "": ":bomb:",
                  0: ":zero:", 1: ":one:", 2: ":two:",
                  3: ":three:", 4: ":four:", 5: ":five:",
                  6: ":six:", 7: ":seven:", 8: ":eight:", 9: ":nine:"}
        message = ""

        if mines > size*size:
            await ctx.send("There's not enough room for that many mines")
        elif size >= 14:
            await ctx.send("There's not enough room for that big of a board")
        else:
            for i in range(0, mines):
                posx = random.randint(0, size - 1)
                posy = random.randint(0, size - 1)
                while board[posx][posy] == "M":
                    posx = random.randint(0, size - 1)
                    posy = random.randint(0, size - 1)
                board[posx][posy] = "M"

            checkBoard = [["" for x in range(size+2)] for y in range(size+2)]
            for x in range(0, size):
                for y in range(0, size):
                    checkBoard[x+1][y+1] = board[x][y]

            for x in range(1, size+1):
                for y in range(1, size+1):
                    if checkBoard[x][y] != "M":
                        count = 0
                        if checkBoard[x-1][y-1] == "M":
                            count += 1
                        if checkBoard[x][y-1] == "M":
                            count += 1
                        if checkBoard[x+1][y-1] == "M":
                            count += 1
                        if checkBoard[x-1][y] == "M":
                            count += 1
                        if checkBoard[x+1][y] == "M":
                            count += 1
                        if checkBoard[x-1][y+1] == "M":
                            count += 1
                        if checkBoard[x][y+1] == "M":
                            count += 1
                        if checkBoard[x+1][y+1] == "M":
                            count += 1
                        board[x-1][y-1] = count


            for i in board:
                for j in i:
                    message = message + "||" + emotes[j] + "||"
                message = message + "\n"
            await ctx.send(message)




    @listener()
    async def on_message(self, message):
        # send messages on alerts
        alertList = await self.config.alerts()
        for i in alertList:
            for j in i[1:]:
                if message.author.id == int(i[0]):
                    break
                foundAt = message.content.lower().find(j.lower())

                def endCheck(found):
                    try:
                        result = message.content[found + len(j)] in [" ", "'", "s"]
                    except IndexError:
                        result = found == len(message.content)-len(j)
                    return result

                if foundAt != -1 and (message.content[foundAt-1] in [" "] or foundAt == 0) and endCheck(foundAt):
                    try:
                        userToDM = message.guild.get_member(int(i[0]))
                        if message.channel.permissions_for(userToDM).read_messages:
                            await userToDM.create_dm()
                            userDM = userToDM.dm_channel
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
                        break
                    except AttributeError:
                        pass

    @listener()
    async def on_reaction_add(self, reaction, user):
        # send messages on alerts
        filterList = await self.config.filters()
        if len(filterList) != 0:
            for i in filterList:
                if int(i[0]) == int(reaction.message.id):
                    role = reaction.message.guild.get_role(int(i[1]))
                    if role in user.roles:
                        break
                    else:
                        print("removed a reaction from", user.name)
                        await reaction.remove(user)

