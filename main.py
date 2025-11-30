import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

BOT_TOKEN = "YOUR_BOT_TOKEN"     # <-- PUT YOUR TOKEN HERE
GIVE_ROLE_ID = 123456789000      # Visa Accepted role
REJECT_ROLE_ID = 123456789111    # Rejected role
HOLD_ROLE_ID = 123456789222      # Hold role
TICKET_STAFF_ROLE_ID = 123456789333  # Staff who see tickets
WELCOME_CHANNEL_ID = 123456789444    # Welcome channel ID

bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
#  WELCOME MESSAGE
# -----------------------------
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    embed = discord.Embed(
        title="👋 WELCOME TO THE SERVER 👋",
        description=f"🎉 **{member.mention}** welcome to **FOODIE HEAVEN / RP SERVER**! 🎉\n\n"
                    f"💡 Unlock your identity & choose your path.\n"
                    f"📗 Apply for your **Green Card** and read the rules!",
        color=0x00ff99
    )
    embed.set_thumbnail(url=member.avatar)
    await channel.send(embed=embed)

# -----------------------------
#  /givevisa COMMAND
# -----------------------------
@bot.tree.command(name="givevisa", description="Approve user and assign visa role")
async def givevisa(interaction: discord.Interaction, user: discord.Member):
    role = interaction.guild.get_role(GIVE_ROLE_ID)
    await user.add_roles(role)

    embed = discord.Embed(
        title="✅ VISA APPROVED",
        description=f"**Applicant:** {user.mention}\n"
                    f"**Reviewed by:** {interaction.user.mention}",
        color=0x00ff00
    )
    embed.set_footer(text="Your visa has been approved.")
    await interaction.response.send_message(embed=embed)

# -----------------------------
#  /reject COMMAND
# -----------------------------
@bot.tree.command(name="reject", description="Reject application")
async def reject(interaction: discord.Interaction, user: discord.Member):
    role = interaction.guild.get_role(REJECT_ROLE_ID)
    await user.add_roles(role)

    embed = discord.Embed(
        title="❌ APPLICATION REJECTED",
        description=f"**Applicant:** {user.mention}\n"
                    f"**Reviewed by:** {interaction.user.mention}",
        color=0xff0000
    )
    await interaction.response.send_message(embed=embed)

# -----------------------------
#  /holdon COMMAND
# -----------------------------
@bot.tree.command(name="holdon", description="Keep application on hold")
async def holdon(interaction: discord.Interaction, user: discord.Member):
    role = interaction.guild.get_role(HOLD_ROLE_ID)
    await user.add_roles(role)

    embed = discord.Embed(
        title="⏳ APPLICATION ON HOLD",
        description=f"**Applicant:** {user.mention}\n"
                    f"**Reason:** Under review\n"
                    f"**Reviewed by:** {interaction.user.mention}",
        color=0xffd000
    )
    await interaction.response.send_message(embed=embed)

# -----------------------------
#  /anno (Bold Announcement)
# -----------------------------
@bot.tree.command(name="anno", description="Send announcement message")
async def anno(interaction: discord.Interaction, message: str):
    embed = discord.Embed(
        title="📢 **ANNOUNCEMENT**",
        description=f"**{message}**",
        color=0x00aaff
    )
    await interaction.response.send_message(embed=embed)

# -----------------------------
#  TICKET SYSTEM
# -----------------------------
class TicketView(discord.ui.View):
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.get_role(TICKET_STAFF_ROLE_ID): discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites=overwrites,
            reason="New Ticket"
        )

        await channel.send(f"{interaction.user.mention} Ticket Created!", view=CloseTicketView())
        await interaction.response.send_message("Your ticket has been created!", ephemeral=True)


class CloseTicketView(discord.ui.View):
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()
        await interaction.response.send_message("Ticket closed!", ephemeral=True)


@bot.tree.command(name="ticketpanel", description="Create ticket panel")
async def ticketpanel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎫 Support Ticket",
        description="Click the button below to create a **support ticket**.",
        color=0x00ffcc
    )
    await interaction.response.send_message(embed=embed, view=TicketView())

# -----------------------------
#  SYNC COMMANDS ON START
# -----------------------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is online as {bot.user}")

bot.run(BOT_TOKEN)
