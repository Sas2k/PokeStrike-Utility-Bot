import discord
from discord.ext import commands
import json
from dotenv import load_dotenv
import os
from discord_slash import SlashCommand

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
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
# Load cogs
initial_extensions = ["Cogs.Tools","Cogs.Pokemon_TCG","Cogs.Github","Cogs.Fun", "Cogs.Quiz", "Cogs.help", "Cogs.Slash"]

print(initial_extensions)

bot.remove_command('help')

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f"Failed to load extension {extension}")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))
    print(discord.__version__)
    for guild in bot.guilds:
        print(guild)
    print(f'{bot.user} is connected to the following guild:')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

bot.run(token)