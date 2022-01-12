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
initial_extensions = ["Cogs.Tools","Cogs.Pokemon","Cogs.Github","Cogs.Fun"]

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

@bot.event
async def on_message(message:discord.Message):
    if message.author == bot.user:
        pass
    if bot.user.mentioned_in and "preifx" in  message.content:
        await bot.send(message.channel, f'My Prefix is {bot.command_prefix}')

bot.run(token)