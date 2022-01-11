import discord
from discord.ext import commands
from Main import *

class Tools(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="ping",
                     brief="the ping command",
                     description="returns the bot latency")
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms") # It's now self.bot.latency

    @commands.command(name="embed",
                     usage=f"Title Description color Field1Header(optional) Field1T(Optional) Field1Inline(Optional)",
                     brief="creates an embed",
                     description="creates an embed for the color must be in hexadecimal")
    async def embed(self, ctx: commands.Context, title, description, color, F1h = None, F1T = None, F1I = None):
        color = int(color, 16)
        embed = discord.Embed(title=title, description=description, colour=color)
        if F1h != None:
            embed.add_field(name=F1h, value=F1T, inline=F1I)
        else:
            pass
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Tools(bot))