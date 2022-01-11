import discord
from discord.ext import commands
from random import randint, choice

class Fun(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "coin",
                    usage="@the_person_who_chose_heads(optional) @the_person_who_chose_tails(optional)",
                    brief="Flips a coin",
                    description = "flips a coin, the first person is heads, the second person is tails")
    async def coin(self, ctx:commands.Context, heads = None, tails = None):
        coin = randint(1,2)
        if heads == None:
            if coin == 1:
                await ctx.send("the :coin: was flippped and lands on 🤕")
            else:
                await ctx.send("the :coin: was flipped and lands on 🦖")
        else:
            if coin == 1:
                await ctx.send(f"the :coin: was flippped and lands on 🤕 and {heads} wins")
            else:
                await ctx.send(f"the :coin: was flipped and lands on 🦖 and {tails} wins")
    
    @commands.command(name = "roll",
                    usage="sides(optional)",
                    brief="rolls a dice",
                    description="rolls a 6 sided dice if the amount sides aren't put")
    async def roll(self, ctx:commands.Context, sides: int = None):
        if sides == None:
            dice = randint(1, 6)
            await ctx.send(f"🎲 is rolled and it lands on {dice}")
        else:
            dice = randint(1, sides)
            await ctx.send(f"A 🎲({sides}) is rolled and lands on {dice}")


def setup(bot:commands.Bot):
    bot.add_cog(Fun(bot))