import discord
from discord.ext import commands
from pokemontcgsdk import Card, Set
from pokemontcgsdk import RestClient
from dotenv import load_dotenv
import os

if os.path.isfile('.env'):
    load_dotenv('Cogs/.env')
else:
    pass

RestClient.configure(os.environ['pokeapi'])

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

class Pokemon_TCG(commands.Cog):
    """Pokemon TCG related commands"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name="card_id",
                     usage="xy1-1",
                     help="Finds the card that matches the id \nex** xy1-1")
    async def card_id(self, ctx: commands.Context, id):
        card = Card.find(id)
        embed = discord.Embed(colour=0x03fcad, title=f"{card.name} [HP:{card.hp}] [ID: {card.id}] National Pokedex Number:{card.nationalPokedexNumbers}", description=f"type: {card.types}\nweakness: {card.weaknesses}")
        embed.set_image(url=card.images.large)
        embed.add_field(name="Evolves From:", value=f"{card.evolvesFrom}", inline=False)
        embed.add_field(name="Moves [for now only 1 is displayed]", value=f"{card.attacks[0].name} | {card.attacks[0].text} | {card.attacks[0].cost} | {card.attacks[0].damage}", inline=False)
        embed.add_field(name="Other Info", value=f"set: {card.set.name}\nrarity: {card.rarity}\nCard Market: {card.cardmarket.url}", inline=False)
        await send_embed(ctx, embed)
    @commands.command(name="set_id",
                    usage="xy",
                    help="Finds the set that matches the id \nex** xy")
    async def set_id(self, ctx: commands.Context, id):
        sets = Set.find(id)
        embed = discord.Embed(colour=0x03fcad, title=f"{sets.name} [Amount: {sets.total}]", description=f"Release Date: {sets.releaseDate}")
        embed.set_image(url=sets.images.logo)
        embed.set_author(name="The icon of the set", icon_url=sets.images.symbol)
        await send_embed(ctx, embed)

def setup(bot: commands.Bot):
    bot.add_cog(Pokemon_TCG(bot))