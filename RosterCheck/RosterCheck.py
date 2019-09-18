from __future__ import print_function
from redbot.core import Config
from redbot.core import commands
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import asyncio

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1rhzwbQwW3nflIbcCWskDL0OAxj96pxhHXUAfcB3QWVs'


listener = getattr(commands.Cog, "listener", None)  # Trusty + Sinbad
if listener is None:

    def listener(name=None):
        return lambda x: x


class RosterCheck(commands.Cog):
    """Manages the GoA roster"""

    def __init__(self, bot):
        self.bot = bot

        tcreds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                tcreds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not tcreds or not tcreds.valid:
            if tcreds and tcreds.expired and tcreds.refresh_token:
                tcreds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'C:/Users/Luke Vaughan/Desktop/RosterCheck/credentials.json', SCOPES)
                tcreds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(tcreds, token)


        if os.path.exists('RoleExempt.txt'):
            with open("RoleExempt.txt", "r") as f:
                roleFile = f.read().splitlines()
        else:
            with open("RoleExempt.txt", "w"):
                pass
            roleFile = []   
                
                
        self.config = Config.get_conf(self, identifier=6457)
        self.config.register_global(
            creds=tcreds
        )
        self.config.register_global(
            roleExempt=roleFile
        )

    @commands.command()
    @commands.has_role("Officer")
    async def update(self, ctx):
        """This does stuff!"""
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H30"
        await ctx.send("I can do stuff!")

        ranks = {"7": "Wanderer", "5": "Adventurer", "4": "Honoraria", "3": "Journeyman",
                 "2": "Leadership", "1": "Guildmaster"}

        creds = await self.config.creds()

        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            message = ""
            for row in values:
                if row[3] != "":
                    member = ctx.guild.get_member_named(row[3])
                    message = message+ranks[row[1]]+" "
                    message = message+str(member)+" "
                    if str(member) != "None":
                        message = message+member.mention+" "
                        message = message + str(member.id)+"\n"
                    else:
                        message = message+"\n"
                        
            await ctx.send(message)


    @commands.command()
    @commands.has_role("Officer")
    async def rolecheck(self, ctx):
        """This does stuff!"""
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"
        await ctx.send("I can do stuff!")

        ranks = {"7": "Wanderer", "5": "Adventurer", "4": "Honoraria", "3": "Journeyman",
                 "2": "Leadership", "1": "Guildmaster"}

        creds = await self.config.creds()

        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            message = ""
            for row in values:
                if row[3] != "":
                    member = ctx.guild.get_member_named(row[3])
                    
                    if str(member) != "None":
                        if ranks[row[1]] != str(member.top_role) and row[1] in ["9", "7", "5"]:
                            message = message + ranks[row[1]] + " " + member.mention + " " + str(member.top_role) + "\n"

            if message == "":
                message = "No role inconsistencies found"
            await ctx.send(message[:1990])


    @commands.command()
    @commands.has_role("Officer")
    async def updatefromname(self, ctx):
        """This does stuff!"""
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"

        creds = await self.config.creds()

        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            message = ""
            membersToUpdate = []
            
            for i, row in enumerate(values, 3):
                if row[3] != "" and row[4] == "":
                    pos = row[3].find(" #")
                    if pos != -1:
                        row[3] = row[3][:pos] + row[3][(pos+1):]
                    member = ctx.guild.get_member_named(row[3])
                    
                    if str(member) != "None":
                        message = message + str(member) + " " + str(member.id) + " row: " + str(i)+"\n"
                        membersToUpdate.append([str(member.id)])
                    else:
                        membersToUpdate.append([])
                else:
                    membersToUpdate.append([])

            range_name = "'Guild Roster'!E3"

            values = membersToUpdate

            body = {
                'values': values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name,
                valueInputOption="RAW", body=body).execute()
            await ctx.send('{0} cells updated.'.format(result.get('updatedCells')))


    @commands.command()
    @commands.has_role("Officer")
    async def updatefromid(self, ctx):
        """This does stuff!"""
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"

        creds = await self.config.creds()
        await ctx.send("I can do stuff!")

        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            message = ""
            membersToUpdate = []
            
            for i, row in enumerate(values, 3):
                if row[4] != "":
                    member = ctx.guild.get_member(int(row[4]))
                    if str(member) != "None" and str(member) != row[3]:
                        message = message + row[3] + " --> " + str(member) + "\n"
                        membersToUpdate.append([str(member)])
                    else:
                        membersToUpdate.append([])
                else:
                    membersToUpdate.append([])
            if message == "":
                message = "No users to update"
            await ctx.send(message)


            range_name = "'Guild Roster'!D3"

            values = membersToUpdate

            body = {
                'values': values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name,
                valueInputOption="RAW", body=body).execute()
            await ctx.send('{0} cells updated.'.format(result.get('updatedCells')))


    @commands.command()
    async def lookup(self, ctx, *message):
        """This does stuff!"""
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"
        # Your code will go here
        creds = await self.config.creds()
        temp = ""
        for item in message:
            temp = temp + " " + item
        temp = temp[1:]

        nameToCheck = ctx.guild.get_member_named(str(temp))
        print("Name to check is '"+str(nameToCheck)+"'")
        if str(nameToCheck) != "None":

            service = build('sheets', 'v4', credentials=creds)
            
            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            else:
                message = ""
                for row in values:
                    if row[3] == str(nameToCheck):
                        message = "Ingame name is @"+str(row[2])

                if message == "":
                    message = "Ingame name not found"
                await ctx.send(message)
        else:
            await ctx.send("Discord user not found")

    @commands.command()
    async def lookupdiscord(self, ctx, *message):
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"
        """This does stuff!"""
        # Your code will go here
        creds = await self.config.creds()
        temp = ""
        for item in message:
            temp = temp + " " + item
        temp = temp[1:]

        nameToCheck = temp
        print("Name to check is '"+str(nameToCheck)+"'")
        if str(nameToCheck) != "":

            service = build('sheets', 'v4', credentials=creds)
            
            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            else:
                message = ""
                for row in values:
                    if row[2] == str(nameToCheck):
                        message = "Discord name is "+str(row[3])

                if message == "":
                    message = "Discord name not found"
                await ctx.send(message)
        else:
            await ctx.send("Enter a name to lookup")

    @commands.command()
    @commands.has_role("Officer")
    async def leftdiscord(self, ctx):
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"
        """This does stuff!"""
        # Your code will go here
        creds = await self.config.creds()
        await ctx.send("I can do stuff!")

        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        esoMembers = []
        membersWithoutRole = []
        rosterWithoutDiscord = []

        if not values:
            print('No data found.')
        else:
            for member in ctx.guild.members:
                for roleToCheck in member.roles:
                    if str(roleToCheck) == "ESO":
                        esoMembers.append(str(member))
        esoMembers.sort()
        roleWithoutRoster = list(esoMembers)
        for row in values:
            if row[3] != "":
                try:
                    roleWithoutRoster.remove(row[3])
                except ValueError:
                    membersWithoutRole.append(row[3])
        message = "Users with the eso role not on the roster: **" + str(len(roleWithoutRoster)) + "**\n"
        apprenticeCount = 0
        newCount = 0

        for member in list(membersWithoutRole):
            if str(ctx.guild.get_member_named(member)) == "None":
                rosterWithoutDiscord.append(str(member))
                membersWithoutRole.remove(str(member))

        for member in roleWithoutRoster:
            memberRole = str(ctx.guild.get_member_named(member).top_role)
            if memberRole == "Apprentice":
                apprenticeCount += 1
            elif memberRole == "New Recruit":
                newCount += 1
            message = message + "**" + memberRole + "** " + member + "\n"
            if len(message) > 1900:
                await ctx.send(message)
                message = ""
        
        await ctx.send(message[:2000])

        await ctx.send("**" + str(newCount) + "** New Recruits and **" + str(apprenticeCount) + "** Apprentices")

        message = "Users without the eso role on the roster: **" + str(len(membersWithoutRole)) + "**\n"

        for member in membersWithoutRole:
            message = message + member + "\n"
            if len(message) > 1900:
                await ctx.send(message)
                message = ""

        await ctx.send(message)


        message = "Users on the roster that have left Discord: **" + str(len(rosterWithoutDiscord)) + "**\n"

        for member in rosterWithoutDiscord:
            message = message + member + "\n"
        
        await ctx.send(message[:2000])

    @commands.command()
    @commands.has_role("Officer")
    async def estimatenames(self, ctx):
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"
        """This does stuff!"""
        # Your code will go here
        creds = await self.config.creds()
        await ctx.send("I can do stuff!")

        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        namesToUpdate = []
        actualNames = []

        if not values:
            print('No data found.')
        else:
            for row in values:
                if row[3] == "":
                    member = ctx.guild.get_member_named(row[2])
                    if str(member) != "None" and member.name.lower() == (row[2]).lower():
                        namesToUpdate.append([str(member)])
                        actualNames.append(str(member))
                    else:
                        namesToUpdate.append([])
                else:
                    namesToUpdate.append([])

        message = "Number of users estimated: " + str(len(actualNames)) + "\n"

        for member in actualNames:
            message = message + member + ", "
        
        await ctx.send(message[:2000])
        
        range_name = "'Guild Roster'!D3"   
        
        values = namesToUpdate
        
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name,
            valueInputOption="RAW", body=body).execute()
        await ctx.send('{0} cells updated.'.format(result.get('updatedCells')))
        print(namesToUpdate)


    @commands.command()
    @commands.has_role("Officer")
    async def recruitsnodiscord(self, ctx):
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"
        """This does stuff!"""
        # Your code will go here
        creds = await self.config.creds()
        await ctx.send("I can do stuff!")

        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        newRecruitsWithoutDiscord = []

        if not values:
            print('No data found.')
        else:
            for row in values:
                if row[1] == "9" and row[3] == "":
                    newRecruitsWithoutDiscord.append(row[2])

        message = "New recruits who have not joined discord: **" + str(len(newRecruitsWithoutDiscord)) + "**\n"

        for member in newRecruitsWithoutDiscord:
            message = message + member + "\n"
        
        await ctx.send(message[:2000])


    @commands.command()
    async def togglerole(self, ctx):
        """This does stuff!"""
        # Your code will go here
        esorole = ctx.guild.get_role(356874800502931457)
        
        if os.path.exists('RoleExempt.txt'):
            with open("RoleExempt.txt", "r") as f:
                roleExempt = f.read().splitlines()

        def addNewlines(things):
            for item in things:
                yield item
                yield '\n'
        
        with open("RoleExempt.txt", "w") as f:
            if str(ctx.author) in roleExempt:
                print("yes")
                roleExempt.remove(str(ctx.author))
                await ctx.author.add_roles(esorole, reason="User on roster")
                await ctx.send("Your role has been added")
            else:
                print("no")
                roleExempt.append(str(ctx.author))
                await ctx.author.remove_roles(esorole, reason="User not on roster")
                await ctx.send("Your role has been removed")
            f.writelines(addNewlines(roleExempt))
            print(ctx.author)
            print(roleExempt)

    @commands.command()
    @commands.has_role("Officer")
    async def esorole(self, ctx):
        """This does stuff!"""
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"
        # Your code will go here
        esorole = ctx.guild.get_role(356874800502931457)
        creds = await self.config.creds()
        rosterMembers = []

        with open("RoleExempt.txt", "r") as f:
            roleExempt = f.read().splitlines()

        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        added = []
        removed = []

        async with ctx.typing():
            for row in values:
                if row[3] != "" and str(ctx.guild.get_member_named(row[3])) != "None":
                    rosterMembers.append(row[3])

            for name in rosterMembers:
                member = ctx.guild.get_member_named(name)
                if esorole not in member.roles and str(member) not in roleExempt:
                    print("added to", member)
                    added.append(str(member))
                    await member.add_roles(esorole)
            print()

            for member in esorole.members:
                if str(member) not in rosterMembers:
                    print("removed from", str(member))
                    removed.append(str(member))
                    await member.remove_roles(esorole)

        message = "Roles added: " + str(len(added)) + "\n"
        for member in added:
            if len(message) > 1990:
                await ctx.send(message)
                message = ""
            message = message + member + "\n"
        await ctx.send(message)
        
        message = "Roles removed: " + str(len(removed)) + "\n"
        
        for member in removed:
            if len(message) > 1990:
                await ctx.send(message)
                message = ""
            message = message + member + "\n"

        await ctx.send(message[:1990])
        await ctx.send("Roles updated")

    @commands.command()
    @commands.has_role("Officer")
    async def addjoindates(self, ctx):
        """This does stuff!"""
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"
        # Your code will go here
        creds = await self.config.creds()
        await ctx.send("I can do stuff!")

        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        datesToUpdate = []
        actualNames = []

        def createDate(date):
            return str(date.day) + "/" + str(date.month) + "/" + str(date.year)

        if not values:
            print('No data found.')
        else:
            for row in values:
                if row[5] == "":
                    member = ctx.guild.get_member_named(row[3])
                    if str(member) != "None":
                        datesToUpdate.append([createDate(member.joined_at)])
                        actualNames.append(str(member) + " - " + createDate(member.joined_at))
                    else:
                        datesToUpdate.append([])
                else:
                    datesToUpdate.append([])

        message = "Number of dates added: " + str(len(actualNames)) + "\n"

        for member in actualNames:
            message = message + str(member) + ", "
        
        await ctx.send(message[:2000])
        
        range_name = "'Guild Roster'!F3"   
        
        values = datesToUpdate
        
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name,
            valueInputOption="RAW", body=body).execute()
        await ctx.send('{0} cells updated.'.format(result.get('updatedCells')))


    @listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            roleChange = list(set(after.roles) - set(before.roles))
            if roleChange:
                if roleChange[0].name == "ESO":
                    print("ESO role added to", after)
                    print("Will check in an hour for roster")
                    await asyncio.sleep(3600)

                    SAMPLE_RANGE_NAME = "'Guild Roster'!A3:H"
                    creds = await self.config.creds()

                    service = build('sheets', 'v4', credentials=creds)

                    # Call the Sheets API
                    sheet = service.spreadsheets()
                    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                range=SAMPLE_RANGE_NAME).execute()
                    values = result.get('values', [])

                    if not values:
                        print('No data found.')
                    else:
                        found = False
                        for row in values:
                            pos = row[3].find(" #")
                            if pos != -1:
                                row[3] = row[3][:pos] + row[3][(pos + 1):]
                            if row[3] == str(after):
                                print("User found")
                                found = True
                        if not found:
                            print("Unknown user", str(after), "given eso role")
                            messageToSend = "A user " + str(after) + " was given the eso role but not added to the roster.\n"
                            welcomeChannel = self.bot.get_guild(285175143104380928).get_channel(425707351874469908)
                            botChannel = self.bot.get_guild(285175143104380928).get_channel(517788758008004608)
                            staffChannel = self.bot.get_guild(285175143104380928).get_channel(439102408354693132)
                            userMessages = []
                            async for message in welcomeChannel.history(limit=200):
                                if message.author == after:
                                    userMessages.append(message)
                            if len(userMessages) == 0:
                                print("No messages found")
                                messageToSend += "They have not sent any recent messages so no account name could be found.\n"
                            else:
                                found = False
                                for message in userMessages:
                                    if message.content.lower().find("eso") != -1:
                                        print("Contains ESO:", message.content)
                                        messageToSend += "A message containing ESO was found here:\n"
                                        messageToSend += "https://discordapp.com/channels/" + \
                                            str(message.guild.id) + "/" + \
                                            str(message.channel.id) + "/" + \
                                            str(message.id)
                                        found = True
                                if not found:
                                    message = userMessages[-1]
                                    print("First Message:", message.content)
                                    messageToSend += "Their first message is here:\n"
                                    messageToSend += "https://discordapp.com/channels/" + \
                                                     str(message.guild.id) + "/" + \
                                                     str(message.channel.id) + "/" + \
                                                     str(message.id)
                            await botChannel.send(messageToSend)
