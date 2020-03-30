from __future__ import print_function
from redbot.core import Config
from redbot.core import commands
import datetime
import requests
import random
import discord
import typing
import asyncio
import time
import copy
import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#from discord.ext import commands


class Attendance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        Creds = ServiceAccountCredentials.from_json_keyfile_name("GCreds.json", scope)
        gc = gspread.authorize(Creds)

    @commands.command()
    async def LogEvent(ctx, mem1: discord.Member = "", mem2: discord.Member = "", mem3: discord.Member = "",
                mem4: discord.Member = "", mem5: discord.Member = ""):
        vch = ctx.guild.get_channel(360785714339643392)
        TempArr = [mem1, mem2, mem3, mem4, mem5]
        Guest_Arr = []
        Member_Array = []
        for temp in TempArr:
            if temp != "":
                Guest_Arr.append(f"{temp.name}#{temp.discriminator}")
        mem = vch.members
        for x in mem:
            y = f"{x.name}#{x.discriminator}"
            Member_Array.append(y)
        print(Member_Array)
        print(Guest_Arr)
        for Guest in Guest_Arr:
            if Guest in Member_Array:
                Member_Array.remove(Guest)

        print(Member_Array)
        if len(Member_Array) == 0:
            print("Only Guests/Empty Channel")
        else:
            wks = gc.open("GoA Guild Roster").sheet1
            for member in Member_Array:
                cell = wks.find(member)
                col = cell.col
                row = cell.row
                AC = wks.cell(row, 10)
                #print(wks.cell(row,4))
                ACV = int (AC.value)
                #print(ACV)
                ACV = ACV+1
                #print(ACV)
                wks.update_cell(AC.row, AC.col, ACV)
                today = date.today()
                d1 = today.strftime("%d/%m/%Y")
                #print(wks.cell(row, 11))
                wks.update_cell(AC.row, 11, d1)
