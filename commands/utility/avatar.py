import discord
from discord.ext import commands
from discord.ui import Button, View

@commands.command(aliases=['av'], description='Displays the avatar or banner of a user/server.')
async def avatar(ctx, *, arg=None):
    """Displays the avatar or banner of a user/server."""

    # Function to create the embed with the image URL
    def create_embed(title, url):
        embed = discord.Embed(title=title, color=discord.Color.blue())
        embed.set_image(url=url)
        return embed

    # If no argument or "me", show the avatar of the command author
    arg_lower = (arg or "").strip().lower()
    if arg is None or arg_lower in ('', 'me', 'av', 'avatar'):
        user = ctx.author

    # If the argument is "server", show the server's avatar
    elif arg_lower == 'server':
        if ctx.guild:
            user = ctx.guild
        else:
            await ctx.send("This command can only be used in a server.")
            return
    
    else:
        # If the argument is a mention or user ID, handle it
        if '<@' in arg:
            # Handle user mention
            user_id = int(arg[2:-1])  # Extract user ID from the mention
        else:
            try:
                # Attempt to convert to user ID if it's an integer
                user_id = int(arg)
            except ValueError:
                await ctx.send("Invalid user mention or ID.")
                return
        
        try:
            user = await ctx.bot.fetch_user(user_id)
        except discord.NotFound:
            await ctx.send("User not found.")
            return

    # Create the buttons
    avatar_button = Button(label="Avatar", style=discord.ButtonStyle.green, emoji="🖼️")
    banner_button = Button(label="Banner", style=discord.ButtonStyle.blurple, emoji="🖼️")

    # Define a view to hold the buttons
    view = View(timeout=60)
    
    # Create the embed for avatar (use display_avatar so default avatars work)
    avatar_embed = None
    if isinstance(user, discord.Guild):
        if user.icon:
            avatar_embed = create_embed(f"{user.name} Server Icon", user.icon.url)
        else:
            await ctx.send("This server has no custom icon.")
            return
    else:
        # User or Member: always show avatar (custom or default)
        display_name = getattr(user, "display_name", user.name)
        avatar_embed = create_embed(f"{display_name} Avatar", user.display_avatar.url)

    # Create the embed for banner
    banner_embed = None
    if isinstance(user, discord.User) and user.banner:
        banner_embed = create_embed(f"{user.name} Banner", user.banner.url)
    elif isinstance(user, discord.Guild) and user.banner:
        banner_embed = create_embed(f"{user.name} Banner", user.banner.url)

    # Define the button actions
    async def on_avatar_button_click(interaction: discord.Interaction):
        if interaction.user != ctx.author:
            return await interaction.response.send_message("You cannot use this button.", ephemeral=True)
        await interaction.response.edit_message(embed=avatar_embed, view=view)

    async def on_banner_button_click(interaction: discord.Interaction):
        if interaction.user != ctx.author:
            return await interaction.response.send_message("You cannot use this button.", ephemeral=True)
        if banner_embed:
            await interaction.response.edit_message(embed=banner_embed, view=view)
        else:
            await interaction.response.send_message("This user/server does not have a banner.")

    # Add the buttons to the view
    avatar_button.callback = on_avatar_button_click
    banner_button.callback = on_banner_button_click
    view.add_item(avatar_button)
    view.add_item(banner_button)

    # Send the embed with the avatar and buttons
    await ctx.send(embed=avatar_embed, view=view)


async def setup(bot):
    bot.add_command(avatar)