from __future__ import print_function
from redbot.core import commands
from redbot.core import Config
import discord
import typing


class PokeTRs(commands.Cog):
    """Commands to find the TRs you want"""

    def __init__(self, bot):
        self.bot = bot


        default_user = {
            "seed": -1
        }

        self.config = Config.get_conf(self, identifier=6457)
        self.config.register_user(**default_user)

    @commands.command()
    async def setseed(self, ctx, seed: int):
        """Restarts the bot"""
        if seed >=0 and seed < 50:
            await self.config.user(ctx.author).seed.set(seed)
            await ctx.send("Seed successfully set")
        else:
            await ctx.send("Seed must be between 0 and 49!")

    @commands.command()
    async def login(self, ctx):
        """Restarts the bot"""
        seed = await self.config.user(ctx.author).seed()
        if seed == -1:
            await ctx.send("You need to set your seed with !setseed [seed] first! It is the TR number of the first TR sold by the trader at Meeting Spot")
        elif seed == 49:
            seed = 0
            await ctx.send("Seed successfully increased")
            await self.config.user(ctx.author).seed.set(seed)
        else:
            seed += 1
            await ctx.send("Seed successfully increased")
            await self.config.user(ctx.author).seed.set(seed)



    @commands.command()
    async def wt(self, ctx, seed: int = None):
        """Lists the watt traders' stock for today"""
        if not seed:
            seed = await self.config.user(ctx.author).seed()

        trname = {0: "Swords Dance", 1: "Body Slam", 2: "Flamethrower", 3: "Hydro Pump", 4: "Surf", 5: "Ice Beam",
                  6: "Blizzard", 7: "Low Kick", 8: "Thunderbolt", 9: "Thunder", 10: "Earthquake", 11: "Psychic",
                  12: "Agility", 13: "Focus Energy", 14: "Metronome", 15: "Fire Blast", 16: "Waterfall", 17: "Amnesia",
                  18: "Leech Life", 19: "Tri Attack", 20: "Substitue", 21: "Reversal", 22: "Sludge Bomb", 23: "Spikes",
                  24: "Outrage", 25: "Psyshock", 26: "Endure", 27: "Sleep Talk", 28: "Megahorn", 29: "Baton Pass",
                  30: "Encore", 31: "Iron Tail", 32: "Crunch", 33: "Shadow Ball", 34: "Future Sight", 35: "Uproar",
                  36: "Heat Wave", 37: "Taunt", 38: "Trick", 39: "Superpower", 40: "Skill Swap", 41: "Blaze Kick",
                  42: "Hyper Voice", 43: "Overheat", 44: "Cosmic Power", 45: "Muddy Water", 46: "Iron Defense",
                  47: "Dragon Claw", 48: "Bulk Up", 49: "Calm Mind", 50: "Leaf Blade", 51: "Dragon Dance",
                  52: "Gyro Ball", 53: "Close Combat", 54: "Toxic Spikes", 55: "Flare Blitz", 56: "Aura Sphere",
                  57: "Poison Jab", 58: "Dark Pulse", 59: "Seed Bomb", 60: "X-Scissor", 61: "Bug Buzz",
                  62: "Dragon Pulse", 63: "Power Gem", 64: "Focus Blast", 65: "Energy Ball", 66: "Brave Bird",
                  67: "Earth Power", 68: "Nasty Plot", 69: "Zen Headbutt", 70: "Flash Cannon", 71: "Leaf Storm",
                  72: "Power Whip", 73: "Gunk Shot", 74: "Iron Head", 75: "Stone Edge", 76: "Stealth Rock",
                  77: "Grass Knot", 78: "Sludge Wave", 79: "Heavy Slam", 80: "Electro Ball", 81: "Foul Play",
                  82: "Stored Power", 83: "Ally Switch", 84: "Scald", 85: "Work Up", 86: "Wild Charge", 87: "Drill Run",
                  88: "Heat Crash", 89: "Hurricane", 90: "Play Rough", 91: "Venom Drench", 92: "Dazzling Gleam",
                  93: "Darkest Lariat", 94: "High Horsepower", 95: "Throat Chop", 96: "Pollen Puff",
                  97: "Psychic Fangs", 98: "Liquidation", 99: "Body Press"}
        placename = {0: "Meetup Spot", 1: "East Lake Axewell", 2: "Dappled Grove", 3: "Giant's Seat", 4: "Bridge Field",
                     5: "Hammerlocke Hills", 6: "Giant's Cap"}

        trs = [[seed]]

        trs[0].append(trs[0][0] + 24)
        trs[0].append(trs[0][0] + 42)
        trs[0].append(trs[0][0] + 67)
        trs[0].append(trs[0][0] + 96)

        if trs[0][3] >= 100:
            trs[0][3] -= 100

        if trs[0][4] >= 100:
            trs[0][4] -= 100

        for i in range(1, 7):
            nextwt = trs[i - 1][0] + 7
            if nextwt >= 50:
                nextwt -= 49
            trs.append([nextwt])
            trs[i].append(trs[i][0] + 24)
            trs[i].append(trs[i][0] + 42)
            trs[i].append(trs[i][0] + 67)
            trs[i].append(trs[i][0] + 96)
            if trs[i][3] >= 100:
                trs[i][3] -= 100

            if trs[i][4] >= 100:
                trs[i][4] -= 100

        trEmbed = discord.Embed(description="Watt Traders' TR stock today for seed " + str(seed))
        for i in range(0, 7):
            trValue = ""
            for tr in trs[i]:
                trValue += "TR" + str(tr) + "\t" + trname[tr] + "\n"
            trEmbed.add_field(name=placename[i], value=trValue)
        await ctx.send(embed=trEmbed)

    @commands.command()
    async def findtr(self, ctx, tr: typing.Union[int, str], seed: int = None):
        """Finds when a TR is next available"""
        if not seed:
            seed = await self.config.user(ctx.author).seed()



        trname = {0: "Swords Dance", 1: "Body Slam", 2: "Flamethrower", 3: "Hydro Pump", 4: "Surf", 5: "Ice Beam",
                  6: "Blizzard", 7: "Low Kick", 8: "Thunderbolt", 9: "Thunder", 10: "Earthquake", 11: "Psychic",
                  12: "Agility", 13: "Focus Energy", 14: "Metronome", 15: "Fire Blast", 16: "Waterfall", 17: "Amnesia",
                  18: "Leech Life", 19: "Tri Attack", 20: "Substitue", 21: "Reversal", 22: "Sludge Bomb", 23: "Spikes",
                  24: "Outrage", 25: "Psyshock", 26: "Endure", 27: "Sleep Talk", 28: "Megahorn", 29: "Baton Pass",
                  30: "Encore", 31: "Iron Tail", 32: "Crunch", 33: "Shadow Ball", 34: "Future Sight", 35: "Uproar",
                  36: "Heat Wave", 37: "Taunt", 38: "Trick", 39: "Superpower", 40: "Skill Swap", 41: "Blaze Kick",
                  42: "Hyper Voice", 43: "Overheat", 44: "Cosmic Power", 45: "Muddy Water", 46: "Iron Defense",
                  47: "Dragon Claw", 48: "Bulk Up", 49: "Calm Mind", 50: "Leaf Blade", 51: "Dragon Dance",
                  52: "Gyro Ball", 53: "Close Combat", 54: "Toxic Spikes", 55: "Flare Blitz", 56: "Aura Sphere",
                  57: "Poison Jab", 58: "Dark Pulse", 59: "Seed Bomb", 60: "X-Scissor", 61: "Bug Buzz",
                  62: "Dragon Pulse", 63: "Power Gem", 64: "Focus Blast", 65: "Energy Ball", 66: "Brave Bird",
                  67: "Earth Power", 68: "Nasty Plot", 69: "Zen Headbutt", 70: "Flash Cannon", 71: "Leaf Storm",
                  72: "Power Whip", 73: "Gunk Shot", 74: "Iron Head", 75: "Stone Edge", 76: "Stealth Rock",
                  77: "Grass Knot", 78: "Sludge Wave", 79: "Heavy Slam", 80: "Electro Ball", 81: "Foul Play",
                  82: "Stored Power", 83: "Ally Switch", 84: "Scald", 85: "Work Up", 86: "Wild Charge", 87: "Drill Run",
                  88: "Heat Crash", 89: "Hurricane", 90: "Play Rough", 91: "Venom Drench", 92: "Dazzling Gleam",
                  93: "Darkest Lariat", 94: "High Horsepower", 95: "Throat Chop", 96: "Pollen Puff",
                  97: "Psychic Fangs", 98: "Liquidation", 99: "Body Press"}
        placename = {0: "Meetup Spot", 1: "East Lake Axewell", 2: "Dappled Grove", 3: "Giant's Seat", 4: "Bridge Field",
                     5: "Hammerlocke Hills", 6: "Giant's Cap"}

        if type(tr) == str:
            trrev = dict(zip(trname.values(), trname.keys()))
            tr = trrev[tr]

        def calculateTRs(day):
            trs = [[day]]

            trs[0].append(trs[0][0] + 24)
            trs[0].append(trs[0][0] + 42)
            trs[0].append(trs[0][0] + 67)
            trs[0].append(trs[0][0] + 96)

            if trs[0][3] >= 100:
                trs[0][3] -= 100

            if trs[0][4] >= 100:
                trs[0][4] -= 100

            for i in range(1, 7):
                nextwt = trs[i - 1][0] + 7
                if nextwt >= 50:
                    nextwt -= 49
                trs.append([nextwt])
                trs[i].append(trs[i][0] + 24)
                trs[i].append(trs[i][0] + 42)
                trs[i].append(trs[i][0] + 67)
                trs[i].append(trs[i][0] + 96)
                if trs[i][3] >= 100:
                    trs[i][3] -= 100

                if trs[i][4] >= 100:
                    trs[i][4] -= 100
            return trs

        def search(array, item):
            for i, row in enumerate(array):
                if item in row:
                    return i
            return -1

        for i in range(0, 7):
            searchResult = search(calculateTRs(seed + i), tr)
            if searchResult != -1:
                if i == 0:
                    await ctx.send(trname[tr] + " available today at " + placename[searchResult])
                elif i == 1:
                    await ctx.send(trname[tr] + " available tomorrow at " + placename[searchResult])
                else:
                    await ctx.send(trname[tr] + " available in " + str(i) + " days at " + placename[searchResult])
                found = True
                break
        if not found:
            await ctx.send("Error")
