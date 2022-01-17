import discord
from discord.ext import commands
import json
from dotenv import load_dotenv
import os
from pretty_help import PrettyHelp, DefaultMenu

if os.path.isfile('.env'):
    load_dotenv('.env')
else:
    pass

token = os.environ['token']
# Get configuration.json
with open("configurations.json", "r") as config:
    data = json.load(config)
    prefix = data["prefix"]

bot = commands.Bot(prefix)
# Load cogs
initial_extensions = ["Cogs.Tools","Cogs.Pokemon_TCG","Cogs.Github","Cogs.Fun", "Cogs.Quiz"]

print(initial_extensions)


for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f"Failed to load extension {extension}")

menu = DefaultMenu(page_left="◀", page_right="▶", remove="❌")
bot.help_command = PrettyHelp(menu=menu, no_category="Commands")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))
    print(discord.__version__)
    for guild in bot.guilds:
        print(guild)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

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

bot.run(token)