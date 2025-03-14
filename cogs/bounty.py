import discord
from discord.ext import commands
import config

class BountyButton(discord.ui.View):
    """View for the Done button"""

    def __init__(self, bot, bounty_message):
        super().__init__()
        self.bot = bot
        self.bounty_message = bounty_message

    @discord.ui.button(label="Done", style=discord.ButtonStyle.green)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.user.send("You've marked the bounty as done! Please reply with proof.")

        def check(message):
            return message.author == interaction.user and isinstance(message.channel, discord.DMChannel)

        try:
            proof_message = await self.bot.wait_for("message", check=check, timeout=300)  # 5-minute timeout
            admin_channel = self.bot.get_channel(config.ADMIN_CHANNEL_ID)
            
            embed = discord.Embed(title="Bounty Proof Submission", color=discord.Color.orange())
            embed.add_field(name="User", value=interaction.user.mention, inline=False)
            embed.add_field(name="Proof", value=proof_message.content, inline=False)
            embed.set_footer(text="Admins can approve or deny this bounty.")

            view = BountyApprovalView(self.bounty_message)
            await admin_channel.send(embed=embed, view=view)
            await interaction.user.send("Your proof has been sent for admin review.")

        except:
            await interaction.user.send("You took too long to submit proof. Please try again.")

class BountyApprovalView(discord.ui.View):
    """Admin Approval View"""

    def __init__(self, bounty_message):
        super().__init__()
        self.bounty_message = bounty_message

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.bounty_message.delete()
        await interaction.channel.send(f"Bounty approved! {self.bounty_message.content} has been removed.")

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.channel.send("Bounty proof was denied.")

class Bounty(commands.Cog):
    """Bounty creation commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bounty")
    async def bounty(self, ctx, target: str, reward: int):
        """Creates a bounty"""
        embed = discord.Embed(title="New Bounty Posted!", color=discord.Color.red())
        embed.add_field(name="**Target**", value=target, inline=False)
        embed.add_field(name="**Reward**", value=f"${reward:,}", inline=False)
        embed.add_field(name="**Instructions**", value="Click 'Done' once completed.", inline=False)
        embed.set_footer(text=f"Posted by {ctx.author.display_name}")

        message = await ctx.send(embed=embed, view=BountyButton(self.bot, None))
        bounty_button = BountyButton(self.bot, message)
        await message.edit(view=bounty_button)

async def setup(bot):
    await bot.add_cog(Bounty(bot))

