import discord
from discord.ext import commands
import github
from Main import *
import dotenv
import os

if os.path.isfile('.env'):
    dotenv.load_dotenv('Cogs/.env')
else:
    pass

gh_token = os.environ['GH_token']
g = github.Github(gh_token)

class Github(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name = "Bug",
                    usage=f"{prefix}bug Title Description",
                    brief="Reports a Bug",
                    description = "Reports a Bug to the Github Repository")
    async def Bug(self, ctx:commands.Context, Title, Body):
        repo = g.get_repo("Sas2k/PokeStrike-Utility-Bot")
        repo.create_issue(title=Title, body=Body, assignee="Sas2k", labels=['Bug'])
        embed = discord.Embed(title="Thanks for creating a report 📄", description="You can see your issue here https://github.com/sas2k/PokeStrike-Utility-Bot/issues")
        await ctx.send(embed=embed)

def setup(bot:commands.Bot):
    bot.add_cog(Github(bot))