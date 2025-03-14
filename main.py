import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="config.PREFIX", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.load_extension("cogs.bounty")
    await bot.load_extension("cogs.review")

bot.run(config.TOKEN)

