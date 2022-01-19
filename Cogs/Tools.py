from os import name
import discord
from discord.embeds import Embed
from discord.ext import commands

async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except discord.Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except discord.Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)

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
        await send_embed(ctx, embed)

    @commands.command(name="poll",
                    usage="question option1(optional) option2(optional)",
                    brief="creates a poll",
                    description="Creates a poll with 2 options")
    async def poll(self, ctx, question, option1=None, option2=None):
        if option1==None and option2==None:
            embed = Embed(title=f"```New poll: \n{question}```", description="**✅ = Yes**\n**❎ = No**")
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
            await message.add_reaction('❎')
        elif option1==None:
            embed = Embed(title=f"```New poll: \n{question}```",description=f"**1️⃣ = {option1}**\n**2️⃣ = No**")
            message = await ctx.send(embed=embed)
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')
        elif option2==None:
            embed = Embed(title=f"```New poll: \n{question}```",description=f"**1️⃣ = Yes**\n**2️⃣ = {option2}**")
            message = await ctx.send(embed=embed)
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')
        else:
            embed = Embed(title=f"```New poll: \n{question}```",description=f"**1️⃣ = {option1}**\n**2️⃣ = {option2}**")
            message = await ctx.send(embed=embed)
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')

def setup(bot: commands.Bot):
    bot.add_cog(Tools(bot))