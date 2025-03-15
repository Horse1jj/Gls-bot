import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True  # Enable message content access

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Load cogs
async def load_cogs():
    await bot.load_extension("cogs.bounty")

async def main():
    async with bot:
        await load_cogs()
        await bot.start("YOUR_BOT_TOKEN")

asyncio.run(main())


