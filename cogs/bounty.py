import discord
from discord.ext import commands

class Bounty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bounty(self, ctx, target: str, reward: str, *, instructions: str):
        """Creates a bounty with a target, reward, and instructions."""
        # Validate reward input
        try:
            reward = int(reward)
            if reward <= 0:
                raise ValueError("Reward must be positive.")
        except ValueError:
            await ctx.send("Invalid reward amount. Please enter a number.")
            return

        # Create embed for bounty
        embed = discord.Embed(title="New Bounty Posted!", description="A new bounty has been placed!", color=discord.Color.red())
        embed.add_field(name="**Target**", value=target, inline=False)
        embed.add_field(name="**Reward**", value=f"${reward:,}", inline=False)
        embed.add_field(name="**Instructions**", value=instructions, inline=False)
        embed.set_footer(text=f"{ctx.message.created_at.strftime('%m/%d/%y, %I:%M %p')}")

        # Send bounty message with "Done" button
        view = BountyButtons(ctx.author)
        message = await ctx.send(embed=embed, view=view)
        view.message = message  # Save message reference for deletion later

# Bounty Buttons View
class BountyButtons(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author
        self.message = None

    @discord.ui.button(label="Done", style=discord.ButtonStyle.green)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handles the Done button click."""
        await interaction.response.defer()
        await interaction.user.send("You clicked 'Done'! Please provide proof.")
        # Log in admin channel (replace CHANNEL_ID with the actual channel ID)
        admin_channel = interaction.guild.get_channel(CHANNEL_ID)
        if admin_channel:
            await admin_channel.send(f"{interaction.user.mention} submitted a bounty proof.")

# Setup function to load cog
async def setup(bot):
    await bot.add_cog(Bounty(bot))
