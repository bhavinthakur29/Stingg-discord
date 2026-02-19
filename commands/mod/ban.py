import discord
from discord.ext import commands
from discord.ui import Button, View

def create_embed(title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    return embed

@commands.command(name='ban', aliases=['fuck'], description="Ban a user from the server.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    """Ban a user from the server and ask if they should be notified."""
    
    # Ban the user first
    await ctx.guild.ban(user, reason=reason)

    # Embed to confirm the ban and ask for notification choice
    embed = create_embed(
        "User Banned",
        f"{user.name} has been banned from the server for the following reason: {reason or 'No reason provided.'}",
        discord.Color.green()
    )

    # Create buttons for user interaction
    notify_button = Button(label="Notify User", style=discord.ButtonStyle.green, emoji="✅")
    dont_notify_button = Button(label="Don't Notify", style=discord.ButtonStyle.red, emoji="❌")

    # Define a view to hold the buttons
    view = View(timeout=60)
    
    # Define the button actions
    async def notify_user(interaction: discord.Interaction):
        if interaction.user != ctx.author:
            return await interaction.response.send_message("You cannot use this button.", ephemeral=True)
        await interaction.response.edit_message(content=f"Banned {user.name}. They will be notified.", embed=None, view=None)
        await send_notification(ctx, user, reason)
        view.stop()

    async def dont_notify_user(interaction: discord.Interaction):
        if interaction.user != ctx.author:
            return await interaction.response.send_message("You cannot use this button.", ephemeral=True)
        await interaction.response.edit_message(content=f"Banned {user.name}. They will not be notified.", embed=None, view=None)
        view.stop()

    # Add the buttons to the view
    notify_button.callback = notify_user
    dont_notify_button.callback = dont_notify_user
    view.add_item(notify_button)
    view.add_item(dont_notify_button)

    # Send the embed and view (buttons) to the channel
    await ctx.send(embed=embed, view=view)

async def send_notification(ctx, user, reason):
    """Send a notification DM to the user if possible."""
    try:
        await user.send(f"You have been banned from the server `{ctx.guild.name}` for the following reason: {reason or 'No reason provided.'}")
    except discord.Forbidden:
        embed = create_embed("Ban User", "I couldn't send a DM to the user. They have been banned, but I don't have permission to DM them.", discord.Color.orange())
        await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(ban)