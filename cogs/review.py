import discord
from discord.ext import commands
import config

class Review(commands.Cog):
    """Admin review commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="approve")
    @commands.has_permissions(administrator=True)
    async def approve(self, ctx, user: discord.Member):
        """Approves a bounty and notifies the user"""
        await ctx.send(f"Bounty approved for {user.mention}!")
        await user.send("Your bounty proof has been approved. Congratulations!")

    @commands.command(name="deny")
    @commands.has_permissions(administrator=True)
    async def deny(self, ctx, user: discord.Member):
        """Denies a bounty and notifies the user"""
        await ctx.send(f"Bounty proof denied for {user.mention}.")
        await user.send("Your bounty proof has been denied. Please try again.")

async def setup(bot):
    await bot.add_cog(Review(bot))

