import discord
from discord.ext import commands
from pokemontcgsdk import Card
from Main import *
class Pokemon(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name="ptcg",
                     usage=f"xy1-1",
                     brief="pokemon tcg card finder",
                     description="Finds the card that matches the id \nex** xy1-1")
    async def ptcg(self, ctx: commands.Context, id):
        card = Card.find(id)
        embed = discord.Embed(colour=0x03fcad, title=f"{card.name} [HP:{card.hp}] [(ptcg api)code: {card.id}] {card.nationalPokedexNumbers}", description=f"type: {card.types}\nweakness: {card.weaknesses}")
        embed.set_image(url=card.images.large)
        embed.add_field(name="Evolves From:", value=f"{card.evolvesFrom}", inline=False)
        embed.add_field(name="Moves [for now only 1 is displayed]", value=f"{card.attacks[0].name} | {card.attacks[0].text} | {card.attacks[0].cost} | {card.attacks[0].damage}", inline=False)
        embed.add_field(name="Other Info", value=f"set: {card.set.id}\nrarity: {card.rarity}\nCard Market: {card.cardmarket.url}", inline=False)
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Pokemon(bot))