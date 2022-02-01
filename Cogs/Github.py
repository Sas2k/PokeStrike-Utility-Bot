import discord
from discord.ext import commands
import github
import dotenv
import os

if os.path.isfile('.env'):
    dotenv.load_dotenv('Cogs/.env')
else:
    pass

gh_token = os.environ['GH_token']
g = github.Github(gh_token)

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

class Github(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name = "bug",
                    usage="Title Description",
                    help = "Reports a Bug to the Github Repository")
    async def bug(self, ctx:commands.Context, Title, Body):
        repo = g.get_repo("Sas2k/PokeStrike-Utility-Bot")
        repo.create_issue(title=f"[Bug][Discord: {ctx.author.display_name}]{Title}", body=Body, assignee="Sas2k", labels=['Bug'])
        embed = discord.Embed(title="Thanks for creating a report 📄", description="You can see your issue here https://github.com/Sas2k/PokeStrike-Utility-Bot/issues")
        await send_embed(ctx, embed)
    
    @commands.command(name="feature",
                    usage="Title Description",
                    help="suggest a feature for this bot using this command")
    async def feature(self, ctx:commands.context, Title, Body):
        repo = g.get_repo("Sas2k/PokeStrike-Utility-Bot")
        repo.create_issue(title=f"[Feature][Discord: {ctx.author.display_name}]{Title}", body=Body, assignee="Sas2k", labels=['enhancement'])
        embed = discord.Embed(title = "Thanks for your suggestion 🤖", description="You can see your suggestion here https://github.com/Sas2k/PokeStrike-Utility-Bot/issues?q=label%3Aenhancement")
        await send_embed(ctx, embed)

def setup(bot:commands.Bot):
    bot.add_cog(Github(bot))