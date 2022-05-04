import asyncio
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
    """Tools and utilities"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="ping",
                     help="returns the bot latency")
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms") # It's now self.bot.latency

    @commands.command(name="embed",
                     help="creates an embed, `Title Description color(in hex) Field1Header(optional) Field1T(Optional) Field1Inline(Optional)`")
    async def embed(self, ctx: commands.Context, title, description, color, F1h = None, F1T = None, F1I = None):
        color = int(color, 16)
        embed = discord.Embed(title=title, description=description, colour=color)
        if F1h != None:
            embed.add_field(name=F1h, value=F1T, inline=F1I)
        else:
            pass
        await send_embed(ctx, embed)

    @commands.command(name="poll",
                    help="Creates a poll with 2 options `question option1(optional) option2(optional)`")
    async def poll(self, ctx, question, option1=None, option2=None):
        if option1==None and option2==None:
            embed = Embed(title=f"{question}", description="**✅ = Yes**\n\n**❎ = No**", colour=0x96b9d9)
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
            await message.add_reaction('❎')
        elif option1==None:
            embed = Embed(title=f"{question}",description=f"**1️⃣ = {option1}**\n\n**2️⃣ = No**", colour=0x96b9d9)
            message = await ctx.send(embed=embed)
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')
        elif option2==None:
            embed = Embed(title=f"{question}",description=f"**1️⃣ = Yes**\n\n**2️⃣ = {option2}**", colour=0x96b9d9)
            message = await ctx.send(embed=embed)
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')
        else:
            embed = Embed(title=f"{question}",description=f"**1️⃣ = {option1}**\n\n**2️⃣ = {option2}**", colour=0x96b9d9)
            message = await ctx.send(embed=embed)
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')

    @commands.command(name="clear",
                    usage="limit(int)",
                    help="deletes the commanded amount only can be done with admin permissions")
    async def clean(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)

    @commands.command(name = "say",
                    help = "say 'hello world!'")
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def say(self, ctx:commands.Context, *, sentence):
        await ctx.send(sentence)
    @say.error
    async def command_name_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=0x96b9d9)
            await ctx.send(embed=em)

def setup(bot: commands.Bot):
    bot.add_cog(Tools(bot))
