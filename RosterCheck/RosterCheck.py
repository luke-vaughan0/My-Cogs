from __future__ import print_function
from redbot.core import Config
from redbot.core import commands
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import discord
import asyncio
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


listener = getattr(commands.Cog, "listener", None)  # Trusty + Sinbad
if listener is None:

    def listener(name=None):
        return lambda x: x


def shorthash(string):
    value = 0
    for letter in string:
        value += ord(letter)
    return value


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
        else:
            os.chdir("/home/ubuntu")
            with open('token.pickle', 'rb') as token:
                tcreds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not tcreds or not tcreds.valid:
            if tcreds and tcreds.expired and tcreds.refresh_token:
                tcreds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'C:/Users/Luke Vaughan/Desktop/My Cogs/RosterCheck/credentials.json', SCOPES)
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
            creds=tcreds,
            sheetid="",
            trialsheetid=""
        )
        self.config.register_global(
            roleExempt=roleFile
        )
        # self.config.register_channel(**default_channel)

    @commands.command()
    @commands.has_role("Officer")
    async def setrosterid(self, ctx, sheetid):
        old = await self.config.sheetid()
        await self.config.sheetid.set(sheetid)
        await ctx.send("Old ID: " + old + "\nNew ID: " + sheetid)


    @commands.command()
    @commands.has_role("Officer")
    async def settrialsheetid(self, ctx, sheetid):
        old = await self.config.trialsheetid()
        await self.config.trialsheetid.set(sheetid)
        await ctx.send("Old ID: " + old + "\nNew ID: " + sheetid)


    @commands.command()
    @commands.has_role("Officer")
    async def listrole(self, ctx, role: discord.Role):
        message = "Members with " + role.name + ":"
        for member in role.members:
            if len(message) > 1970:
                await ctx.send(message)
                message = ""
            message = message + "\n" + str(member)
        await ctx.send(message)


    @commands.command()
    @commands.has_role("Officer")
    async def setvgoat(self, ctx):
        """Sets people to the correct vgoat roles"""
        SAMPLE_SPREADSHEET_ID = await self.config.trialsheetid()
        SAMPLE_RANGE_NAME = "'Vet Trial Roster'!B17:AC"

        trainee = ctx.guild.get_role(675480762925187084)
        expert = ctx.guild.get_role(675480949827567635)
        master = ctx.guild.get_role(675481067012227072)

        creds = await self.config.creds()
        vgoatMembers = []

        service = build('sheets', 'v4', credentials=creds)
        async with ctx.typing():

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])
            added = []
            removed = []

            for i in range(0, len(values), 7):
                row = values[i]
                if row == []:
                    break
                name = row[0].strip("@").split(" ", 1)[0]
                if str(ctx.guild.get_member_named(name)) != "None":
                    #if values[i+1][0] != "":
                    #print(values[i+2])
                    vgoatMembers.append([ctx.guild.get_member_named(name).name, values[i+2][1]])

            print(vgoatMembers)


            for item in vgoatMembers:
                member = ctx.guild.get_member_named(item[0])
                if trainee not in member.roles:
                    print("added to", member)
                    added.append(str(member))
                    #await member.add_roles(trainee)
            print()

            #for member in esorole.members:
            #    if str(member) not in rosterMembers:
            #        print("removed from", str(member))
            #        removed.append(str(member))
            #        await member.remove_roles(esorole)

        message = "Trainee Roles added: " + str(len(added)) + "\n"
        for member in added:
            if len(message) > 1990:
                await ctx.send(message)
                message = ""
            message = message + member + "\n"
        await ctx.send(message)

        message = "Trainee Roles removed: " + str(len(removed)) + "\n"

        for member in removed:
            if len(message) > 1990:
                await ctx.send(message)
                message = ""
            message = message + member + "\n"

        await ctx.send(message[:1990])

        for item in vgoatMembers:
            member = ctx.guild.get_member_named(item[0])
            if expert not in member.roles and item[1] in ["vGoat Expert", "vGoat Master"]:
                print("added to", member)
                added.append(str(member))
                #await member.add_roles(trainee)
        print()

        #for member in esorole.members:
        #    if str(member) not in rosterMembers:
        #        print("removed from", str(member))
        #        removed.append(str(member))
        #        await member.remove_roles(esorole)

        message = "Expert Roles added: " + str(len(added)) + "\n"
        for member in added:
            if len(message) > 1990:
                await ctx.send(message)
                message = ""
            message = message + member + "\n"
        await ctx.send(message)

        message = "Expert Roles removed: " + str(len(removed)) + "\n"

        for member in removed:
            if len(message) > 1990:
                await ctx.send(message)
                message = ""
            message = message + member + "\n"

        await ctx.send(message[:1990])

        for item in vgoatMembers:
            member = ctx.guild.get_member_named(item[0])
            if master not in member.roles and item[1] == "vGoat Master":
                print("added to", member)
                added.append(str(member))
                #await member.add_roles(trainee)
        print()

        #for member in esorole.members:
        #    if str(member) not in rosterMembers:
        #        print("removed from", str(member))
        #        removed.append(str(member))
        #        await member.remove_roles(esorole)

        message = "Master Roles added: " + str(len(added)) + "\n"
        for member in added:
            if len(message) > 1990:
                await ctx.send(message)
                message = ""
            message = message + member + "\n"
        await ctx.send(message)

        message = "Master Roles removed: " + str(len(removed)) + "\n"

        for member in removed:
            if len(message) > 1990:
                await ctx.send(message)
                message = ""
            message = message + member + "\n"

        await ctx.send(message[:1990])

        await ctx.send("Roles updated")


    @commands.command()
    @commands.has_role("Officer")
    async def wrongroles(self, ctx):
        """Lists incorrect roles"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"

        roles = {"9": "Scout", "8": "Wanderer", "7": "Adventurer", "5": "Honoraria", "4": "Officer", "3": "Senior Officer", "2": "Community Leadership"}


        creds = await self.config.creds()

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        message = ""
        if not values:
            print('No data found.')
        else:
            for row in values:
                if row[4] == "" or row[1] in ["5", "1"]:
                    continue
                member = ctx.guild.get_member(int(row[4]))
                role = roles[row[1]]
                if member:
                    if member.top_role.name != role:
                        message += str(member) + " is " + member.top_role.name + ", but " + role + " on roster\n"
        if message == "":
            message = "No wrong roles"
        await ctx.send(message)


    @commands.command()
    @commands.has_role("Officer")
    async def correctroles(self, ctx):
        """Corrects incorrect roles"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"

        adventurer = ctx.guild.get_role(434100306893209610)  # 6
        wanderer = ctx.guild.get_role(290170879302696961)  # 7

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
            promoted = ""
            ingame = ""
            async with ctx.typing():
                for row in values:
                    if row[3] != "":
                        member = ctx.guild.get_member_named(row[3])
                        if str(member) != "None":
                            if wanderer in member.roles and row[1] != "7":
                                if row[1] == "6":
                                    await member.remove_roles(wanderer)
                                    await member.add_roles(adventurer)
                                    promoted += "\nPromoted " + member.name + " to Adventurer"
                            elif adventurer in member.roles and row[1] != "6":
                                ingame += "\n" + row[2] + " should be Adventurer"
                if promoted == "":
                    promoted = "No discord promotions"
                if ingame == "":
                    ingame = "No ingame promotions"
            await ctx.send(promoted)
            await ctx.send(ingame)


    @commands.command()
    @commands.has_role("Officer")
    async def roleless(self, ctx):
        """Prints how many users have no roles on the server!"""
        count = 0
        for user in ctx.guild.members:
            if len(user.roles) == 1:
                count += 1
        await ctx.send("There are " + str(count) + " members with no roles")


    @commands.command()
    @commands.has_role("Officer")
    async def addroleless(self, ctx):
        """Adds Roleless role to people with no roles"""
        rolelessRole = ctx.guild.get_role(671005795999023144)
        count = 0
        async with ctx.typing():
            for user in ctx.guild.members:
                if len(user.roles) == 1:
                    count += 1
                    await user.add_roles(rolelessRole)
        await ctx.send("Added Roleless role to " + str(count) + " members")


    @commands.command()
    @commands.has_role("Officer")
    async def kickroleless(self, ctx):
        """Kicks everyone with a roleless role"""
        rolelessRole = ctx.guild.get_role(671005795999023144)
        count = 0
        async with ctx.typing():
            for member in rolelessRole.members:
                await member.kick(reason="Roleless")
                count += 1
        await ctx.send("Kicked " + str(count) + " members")


    @commands.command()
    @commands.has_role("Officer")
    async def updatefromname(self, ctx):
        """Adds user IDs to users without one"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"

        creds = await self.config.creds()

        service = build('sheets', 'v4', credentials=creds)
        async with ctx.typing():
        
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
        """Updates discord username from their id"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"

        creds = await self.config.creds()

        service = build('sheets', 'v4', credentials=creds)

        async with ctx.typing():
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
    @commands.has_role("Officer")
    async def trialroles(self, ctx):
        """Lists stats for trial roles"""
        esorole = ctx.guild.get_role(356874800502931457)
        traineeRole = ctx.guild.get_role(675480762925187084)
        expertRole = ctx.guild.get_role(675480949827567635)
        masterRole = ctx.guild.get_role(675481067012227072)
        members = esorole.members
        trainee = []
        expert = []
        master = []
        for member in members:
            if traineeRole in member.roles or expertRole in member.roles or masterRole in member.roles:
                trainee.append(member)
            if expertRole in member.roles or masterRole in member.roles:
                expert.append(member)
            if masterRole in member.roles:
                master.append(member)

        message = "ESO members: " + str(len(members))
        message += "\nMembers with at least trainee: " + str(len(trainee)) + " - " + str(
            round((len(trainee) / len(members)) * 100)) + "%"
        message += "\nMembers with at least expert: " + str(len(expert)) + " - " + str(
            round((len(expert) / len(members)) * 100)) + "%"
        message += "\nMembers with master: " + str(len(master)) + " - " + str(
            round((len(master) / len(members)) * 100)) + "%"


        await ctx.send(message)


    @commands.command()
    async def lookup(self, ctx, user: discord.Member):
        """Finds an ingame name from a discord name"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
        creds = await self.config.creds()

        async with ctx.typing():
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            for row in values:
                if row[3] == str(user):
                    embed = discord.Embed(description=user.mention)
                    embed.add_field(name="Ingame name", value=row[2])
                    embed.add_field(name="Join date", value=user.joined_at.date())
                    await ctx.send(content="Ingame name is " + row[2], embed=embed)
                    return


            await ctx.send("No roster entry found for that discord name")


    @commands.command()
    @commands.has_role("Officer")
    async def generatecode(self, ctx, user: discord.Member, dps, siroria, valid):
        """Finds an ingame name from a discord name"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
        creds = await self.config.creds()

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        else:
            name = ""
            for row in values:
                if row[3] == str(user):
                    name = str(row[2])

            if name == "":
                await ctx.send("No roster entry found for that discord name")
                return
        namehash = shorthash(name)
        code = int(dps+siroria+valid)*namehash
        await ctx.send(code)


    @commands.command()
    @commands.has_role("Officer")
    async def checkcode(self, ctx, ingamename, code: int):
        """Finds an ingame name from a discord name"""
        namehash = shorthash(ingamename)
        info = code/namehash
        if info.is_integer():
            info = str(info)[:-2]
            await ctx.send("DPS: " + info[:-2].replace("-","") + "\tSiroria/Relequen: " + info[-2:-1] + "\tValid: " + info[-1])
        else:
            await ctx.send("This code is invalid")




    @commands.command()
    async def lookupdiscord(self, ctx, *message):
        """Finds a discord name from an ingame name"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
        creds = await self.config.creds()
        temp = ""
        for item in message:
            temp = temp + " " + item
        nameToCheck = temp[1:]

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
                    if row[2].lower() == str(nameToCheck).lower():
                        if row[3] != "":
                            member = ctx.guild.get_member_named(row[3])
                            if not member:
                                await ctx.send("This user has left discord, their name was " + row[3])
                                return
                            embed = discord.Embed(description=member.mention)
                            embed.add_field(name="Ingame name", value=row[2])
                            embed.add_field(name="Join date", value=member.joined_at.date())
                            await ctx.send(content="Discord name is "+str(member), embed=embed)
                            return
                        else:
                            await ctx.send("No discord name registered for that ingame name")

                message = "No roster entry found for that ingame name"
                await ctx.send(message)
        else:
            await ctx.send("Enter a name to lookup")


    @commands.command()
    @commands.has_role("Officer")
    async def notondiscord(self, ctx):
        """Lists users not on discord"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
        # Your code will go here
        creds = await self.config.creds()
        await ctx.send("I can do stuff!")

        service = build('sheets', 'v4', credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        neverJoined = []
        leftDiscord = []

        if not values:
            print('No data found.')
        else:
            for row in values:
                if row[2] == "":
                    break
                elif row[3] == "":
                    neverJoined.append(row[2])
                elif str(ctx.guild.get_member_named(row[3])) == "None":
                    leftDiscord.append(row[2])

        message = "Users that have left Discord: **" + str(len(leftDiscord)) + "**\n"

        if len(leftDiscord) != 0:
            for member in leftDiscord:
                message = message + member + "\n"
        
        await ctx.send(message[:2000])

        message = "Users that have never joined Discord: **" + str(len(neverJoined)) + "**\n"

        if len(neverJoined) != 0:
            for member in neverJoined:
                if len(message) > 1970:
                    await ctx.send(message)
                    message = ""
                message = message + member + "\n"

        await ctx.send(message[:2000])


    @commands.command()
    @commands.has_role("Officer")
    async def estimatenames(self, ctx):
        """Adds names of users who have the same ESO and discord names"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
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
                    if str(member) == "None":
                        for discordMember in ctx.guild.members:
                            if discordMember.name.lower() == row[2].lower():
                                member = discordMember
                                break
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
    async def addtoroster(self, ctx, ingameName, discordName: discord.Member, rank="9"):
        """Adds a user to the roster"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
        creds = await self.config.creds()
        ranks = {"scout": "9", "wanderer": "8", "adventurer": "7", "honoraria": "4", "officer": "3",
                 "leadership": "2", "guildmaster": "1"}

        service = build('sheets', 'v4', credentials=creds)

        async with ctx.typing():

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            ingameOnRoster = []
            discordOnRoster = []
            roster = []
            userform = [[time.strftime("%d/%m/%y %X")]]

            discordMember = discordName

            if not values:
                print('No data found.')
            else:
                for count, row in enumerate(values, 3):
                    if row[2] == "":
                        break
                for row in values:
                    roster.append([row[2], row[3]])
                    ingameOnRoster.append(row[2])
                    discordOnRoster.append(row[3])

            error = False
            special = False
            if not rank.isdigit() or rank not in ["9", "8", "7", "4", "3", "2", "1"]:
                try:
                    rank = ranks[rank.lower()]
                except KeyError:
                    await ctx.send("This rank could not be recognised")
                    error = True
            userform[0].append(rank)

            if ingameName.find("#") != -1:
                await ctx.send("This ingame name is not valid")
                error = True
            for pos, row in enumerate(roster, 3):
                if str(ingameName).lower() == row[0].lower():
                    try:
                        if row[1] == "":
                            await ctx.send("This ingame name is on the roster, would you like to add a discord name only?\nType Y to accept")

                            def check(m):
                                return (m.content == 'Y' or m.content == "y") and m.channel == ctx.channel

                            try:
                                reply = await self.bot.wait_for('message', timeout=10.0, check=check)
                            except asyncio.TimeoutError:
                                await ctx.send("No response given")
                                error = True
                            else:
                                if str(discordMember) != "None":
                                    if str(discordMember) in discordOnRoster:
                                        await ctx.send("This discord name is a duplicate")
                                        error = True
                                    else:
                                        special = True
                                        range_name = "'Guild Roster'!D" + str(pos) + ":G" + str(pos)

                                        values = [[str(discordMember), str(discordMember.id), discordMember.joined_at.strftime("%d/%m/%y"), time.strftime("%d/%m/%y")]]

                                        body = {
                                            'values': values
                                        }
                                        result = service.spreadsheets().values().update(
                                            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name,
                                            valueInputOption="RAW", body=body).execute()
                                        await ctx.send("User added")
                                else:
                                    await ctx.send("This Discord user could not be found")
                                    error = True


                        else:
                            await ctx.send("This ingame name is a duplicate")
                            error = True

                    except ValueError:
                        await ctx.send("This ingame name is a duplicate")
                        error = True
                        pass
            userform[0].append(ingameName)

            if str(discordMember) != "None":
                if str(discordMember) in discordOnRoster:
                    await ctx.send("This discord name is a duplicate")
                    error = True
                userform[0].append(str(discordMember))
                userform[0].append(str(discordMember.id))
                userform[0].append(discordMember.joined_at.strftime("%d/%m/%y"))
                userform[0].append(time.strftime("%d/%m/%y"))
            else:
                await ctx.send("This Discord user could not be found")
                error = True

        if not special:
            if not error:
                range_name = "'Guild Roster'!A" + str(count) + ":G" + str(count)

                values = userform

                body = {
                    'values': values
                }
                #service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name)
                result = service.spreadsheets().values().append(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name,
                    valueInputOption="RAW", body=body).execute()
                if result.get('updatedCells') == 0:
                    await ctx.send("No data was entered, please check the sheet (or ping luke or sodan)")
                else:
                    await ctx.send("User added")
            else:
                await ctx.send("The user was not added")
        pass


    @commands.command()
    @commands.has_role("Officer")
    async def bulkaddtoroster(self, ctx, *message):
        """Adds multiple users to the roster"""
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
        creds = await self.config.creds()
        ranks = {"wanderer": "7", "adventurer": "6", "honoraria": "4", "officer": "3",
                 "leadership": "2", "guildmaster": "1"}

        service = build('sheets', 'v4', credentials=creds)
        updatelist = []
        error = False

        if len(message) % 2 == 0:
            for i in range(0, len(message)-1, 2):
                if message[i+1].isdigit():
                    discordMember = ctx.guild.get_member(int(message[i+1]))
                else:
                    discordMember = ctx.guild.get_member_named(message[i+1])
                if not discordMember:
                    await ctx.send("\"" + message[i+1] + "\" is not a valid discord name")
                    error = True
                    break
                else:
                    updatelist.append([message[i], discordMember])
            if not error:
                message = "Users to add:\n"
                for member in updatelist:
                    message += member[0] + " - " + str(member[1]) + "\n"
                message += "If these are all correct, type Y"
                await ctx.send(message)

                def check(m):
                    return m.channel == ctx.channel
                try:
                    reply = await self.bot.wait_for('message', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("Response not given")
                else:
                    if reply.content.upper() == "Y":
                        for member in updatelist:
                            await ctx.send("Running for " + member[0])
                            await ctx.invoke(self.bot.get_command("addtoroster"), member[0], member[1])
                    elif reply.content.upper() == "N":
                        await ctx.send("ok I won't")
                await ctx.send("Done")

        else:
            await ctx.send("Input is invalid, make sure you put \"\" around names with spaces")


    @commands.command()
    async def togglerole(self, ctx):
        """Toggles ESO role on and off for notifications"""
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
    async def replacerole(self, ctx, oldrole: discord.Role, newrole: discord.Role, *members):
        """Toggles ESO role on and off for notifications"""
        async with ctx.typing():
            for imember in members:
                member = ctx.guild.get_member_named(imember)
                if member:
                    if oldrole in member.roles:
                        await member.remove_roles(oldrole)
                    if newrole not in member.roles:
                        await member.add_roles(newrole)
                else:
                    await ctx.send("Member not found: " + str(imember))
        await ctx.send("Updated " + str(len(members)) + " members")



    @commands.command()
    @commands.has_role("Officer")
    async def overduepromotion(self, ctx):
        """Lists users that need promotions."""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
        creds = await self.config.creds()
        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        promotions = []

        for row in values:
            if row[6] != "":
                if row[1] == "7" and int(row[7]) >= 90:
                    promotions.append(row[2])

        message = "Promotions needed: **" + str(len(promotions)) + "**\n"

        for member in promotions:
            if len(message) > 1990:
                await ctx.send(message)
                message = ""
            message = message + member + "\n"
        await ctx.send(message)

    @commands.command()
    @commands.has_role("Officer")
    async def checkroster(self, ctx):
        """Lists users who haven't been added to the roster"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"

        esorole = ctx.guild.get_role(356874800502931457)
        creds = await self.config.creds()
        rosterMembers = []

        with open("RoleExempt.txt", "r") as f:
            roleExempt = f.read().splitlines()

        service = build('sheets', 'v4', credentials=creds)
        async with ctx.typing():

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])
            removed = []

            for row in values:
                if row[3] != "" and str(ctx.guild.get_member_named(row[3])) != "None":
                    rosterMembers.append(row[3])

            welcomeChannel = ctx.guild.get_channel(425707351874469908)
            welcomeHistory = await welcomeChannel.history(limit=500).flatten()

            for member in esorole.members:
                if str(member) not in rosterMembers and str(member) not in roleExempt:
                    userMessages = []
                    for message in welcomeHistory:
                        if message.author == member:
                            userMessages.append(message)
                    if len(userMessages) == 0:
                        print("No messages found")
                        messageToSend = "No messages found"
                    else:
                        found = False
                        for message in userMessages:
                            if message.content.lower().find("eso") != -1:
                                print("Contains ESO:", message.content)
                                messageToSend = "https://discordapp.com/channels/" + \
                                                 str(message.guild.id) + "/" + \
                                                 str(message.channel.id) + "/" + \
                                                 str(message.id)
                                found = True
                                break
                        if not found:
                            message = userMessages[-1]
                            messageToSend = "https://discordapp.com/channels/" + \
                                             str(message.guild.id) + "/" + \
                                             str(message.channel.id) + "/" + \
                                             str(message.id)
                    removed.append([str(member), messageToSend])


        message = "Users to be added to the roster: " + str(len(removed)) + "\n"

        for member in removed:
            if len(message) > 1900:
                await ctx.send(message)
                message = ""
            message = message + member[0] + " - " + member[1] + "\n"

        await ctx.send(message[:1990])


    @commands.command()
    @commands.has_role("Officer")
    async def esorole(self, ctx):
        """Adds and removes the ESO role to match the roster"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
        # Your code will go here
        esorole = ctx.guild.get_role(356874800502931457)
        creds = await self.config.creds()
        rosterMembers = []

        with open("RoleExempt.txt", "r") as f:
            roleExempt = f.read().splitlines()

        service = build('sheets', 'v4', credentials=creds)
        async with ctx.typing():
        
            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])
            added = []
            removed = []


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
                if str(member) not in rosterMembers and str(member) not in roleExempt:
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
        """Adds join dates to users without one on the roster"""
        SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
        SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
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
                    SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
                    print("ESO role added to", after)
                    print("Will check in an hour for roster")
                    await asyncio.sleep(3600)

                    SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
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
                                        break
                                if not found:
                                    message = userMessages[-1]
                                    print("First Message:", message.content)
                                    messageToSend += "Their first message is here:\n"
                                    messageToSend += "https://discordapp.com/channels/" + \
                                                     str(message.guild.id) + "/" + \
                                                     str(message.channel.id) + "/" + \
                                                     str(message.id)
                            await botChannel.send(messageToSend)

    @listener()
    async def on_member_join(self, member):
        await member.guild.get_channel(425707351874469908).send("Welcome " + member.mention + " to the Guild of Adventure **[EU]** Discord!\n\n"
                                                                                                "Please take a look at the <#500990128035069962> channel and then let us know __below this message:__\n"
                                                                                                ":small_orange_diamond: the **game** you are joining (our guild spans multiple games)\n"
                                                                                                ":small_orange_diamond: your **account name** in that game\n"
                                                                                                "After this, an officer will open the **rest of our channels** and invite you\n")

    @listener()
    async def on_member_remove(self, member):
        leavers = self.bot.get_guild(285175143104380928).get_channel(517788855882088466)
        esoRole = self.bot.get_guild(285175143104380928).get_role(356874800502931457)
        gw2Role = self.bot.get_guild(285175143104380928).get_role(356874876125970432)
        comRole = self.bot.get_guild(285175143104380928).get_role(304714006411739156)
        embed = discord.Embed(title=str(member) + " has just left")
        try:
            embed.set_thumbnail(url=str(member.avatar_url))
        except:
            pass
        embed.add_field(name="Discord", value=member.mention)
        embed.add_field(name="Join date", value=member.joined_at.date())
        # embed.add_field(name="Member for", value=member.joined_at.date())
        message = str(member) + " (" + str(member.id) + ") has just left\n"
        if len(member.roles) == 1:
            embed.add_field(name="Roles", value="No Roles")
        elif esoRole in member.roles:
            SAMPLE_SPREADSHEET_ID = await self.config.sheetid()
            roleEmbed = "ESO " + member.top_role.name
            message = message + "They were an ESO " + member.top_role.name

            SAMPLE_RANGE_NAME = "'Guild Roster'!A3:I"
            creds = await self.config.creds()

            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            ign = ""
            for row in values:
                pos = row[3].find(" #")
                if pos != -1:
                    row[3] = row[3][:pos] + row[3][(pos + 1):]
                if row[3] == str(member):
                    print("User found")
                    ign = row[2]
                    break
            if ign != "":
                embed.add_field(name="Ingame Name", value=ign)
            else:
                embed.add_field(name="Ingame Name", value="Unknown")
            if gw2Role in member.roles:
                embed.insert_field_at(index=2, name="Roles", value=roleEmbed + "\nGW2 " + member.top_role.name)
            else:
                embed.insert_field_at(index=2, name="Roles", value="ESO " + member.top_role.name)

        elif gw2Role in member.roles:
            embed.insert_field_at(index=2, name="Roles", value="GW2 " + member.top_role.name)
        elif len(member.roles) == 3 and comRole in member.roles:
            embed.insert_field_at(index=2, name="Roles", value="Community Member")
        else:
            embed.insert_field_at(index=2, name="Roles", value=member.top_role.name)
        await leavers.send(embed=embed)
