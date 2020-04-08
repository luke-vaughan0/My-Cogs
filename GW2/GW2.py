from __future__ import print_function
from redbot.core import commands
from random import seed
from random import randint

Easy = ["Ascalonian Catacombs - Path 0 - Story",
                "Ascalonian Catacombs - Path 1 - Hodgins",
                "Ascalonian Catacombs - Path 3 - Tzark",
                "Caudecus Manor - Path 0 - Story",
                "Caudecus Manor - Path 1 - Asura",
                "Twilight Arbor - Path 0 - Story",
                "Twilight Arbor - Path 1 - Leurent",
                "Twilight Arbor - Path 2 - Vevina",
                "Sorrow's Embrace - Path 0 - Story",
                "Sorrow's Embrace - Path 1 - Fergg",
                "Sorrow's Embrace - Path 3 - Koptev",
                "Honor of the Waves - Path 1 - Butcher",
                "Crucibal of Eternity - Path 0 - Story",
                "Crucibal of Eternity - Path 1 - Submarine",
                "Crucibal of Eternity - Path 3 - Front Door ",
                "Citadel of Flame - Path 0 - Story",
                "Citadel of Flame - Path 1 - Ferrah",
                "Citadel of Flame - Path 2 - Magg"]
Mid = [
            "Ascalonian Catacombs - Path 2 - Detha",
            "Caudecus Manor - Path 2 - Seraph",
            "Caudecus Manor - Path 3 - Butler",
            "Sorrow's Embrace - Path 2 - Rasolov",
            "Honor of the Waves - Path 0 - Story",
            "Honor of the Waves - Path 2 - Plunderer",
            "Honor of the Waves - Path 3 - Zealot",
            "Crucibal of Eternity - Path 2 - Teleporter",
            "Citadel of Flame - Path 3 - Rhiannon"
        ]
Hard = [
            "Twilight Arbor - Path 3 - Aetherpath",
            "Ruined City of Arah - Path 0 - Story ",
            "Ruined City of Arah - Path 1 - Jotun ",
            "Ruined City of Arah - Path 2 - Mursaat",
            "Ruined City of Arah - Path 3 - Forgotten",
            "Ruined City of Arah - Path 4 - Seer"
        ]


def PrintPaths(ctx, SelectList, amount):
    PrintList = []
    seed()
    if amount > 6:
        amount = 6
    if amount < 1:
        amount = 1
    for x in range(amount):
        PrintList.append(SelectList.pop(randint(0, len(SelectList)-1)))

    message = ""
    for x in PrintList:
        message += "\t" + x + "\n"
    return message


def EPaths(ctx, amount):
    SelectList = Easy
    return PrintPaths(ctx, SelectList, amount)


def MPaths(ctx, amount):
    SelectList = Easy + Mid
    return PrintPaths(ctx, SelectList, amount)


def HPaths(ctx, amount):
    SelectList = Easy + Mid + Hard
    return PrintPaths(ctx, SelectList, amount)


class GW2(commands.Cog):
    """GW2 Commands"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def PrintDungeons(self, ctx, amount: int = 3):
        message = "This Weeks Easy Paths Are: \n" + EPaths(ctx, amount) + "\n" +\
                  "This Weeks Medium Paths Are: \n" + MPaths(ctx, amount) + "\n" +\
                  "This Weeks Hard Paths Are: \n" + HPaths(ctx, amount)
        await ctx.send(message)
