from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    """Slash commands"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="slash", description="first slash command of this bot")
    def _slash(self, ctx: SlashContext):
        ctx.send("Slash")

def setup(bot:commands.Bot):
    bot.add_cog(Slash(bot))