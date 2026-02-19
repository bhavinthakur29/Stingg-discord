import discord
from discord.ext import commands

@commands.group(invoke_without_command=True, description="Manage server channels.")
async def channel(ctx):
    available_subcommands = [command.name for command in channel.commands]
    embed = discord.Embed(title='Available subcommands for `channel`', description="\n".join(available_subcommands), color=discord.Colour.blue())
    await ctx.send(embed=embed)


def _resolve_channel(ctx, argument: str):
    """Resolve channel by mention, ID, or name. Returns None if not found."""
    if not argument or not argument.strip():
        return None
    argument = argument.strip()
    # Try mention <#id> or raw ID
    if argument.startswith("<#") and argument.endswith(">"):
        try:
            cid = int(argument[2:-1])
            return ctx.guild.get_channel(cid)
        except (ValueError, TypeError):
            pass
    try:
        cid = int(argument)
        return ctx.guild.get_channel(cid)
    except (ValueError, TypeError):
        pass
    # Try by name (case-insensitive)
    lower_arg = argument.lower()
    for ch in ctx.guild.text_channels:
        if ch.name.lower() == lower_arg:
            return ch
    for ch in ctx.guild.channels:
        if ch.name.lower() == lower_arg:
            return ch
    return None


@channel.command(description="Delete a channel and create a clone. Use with no args for current channel, or pass a channel name/mention.")
@commands.has_permissions(manage_channels=True)
@commands.bot_has_permissions(manage_channels=True)
async def nuke(ctx, target: str = None):
    # Decide which channel to nuke
    if target is None or not target.strip():
        channel_to_nuke = ctx.channel
    else:
        channel_to_nuke = _resolve_channel(ctx, target)
        if channel_to_nuke is None:
            await ctx.send(f"Channel `{target}` not found. Use a channel name, mention, or ID.", delete_after=10)
            return
        if not isinstance(channel_to_nuke, discord.TextChannel):
            await ctx.send("Only text channels can be nuked.", delete_after=10)
            return

    # Confirmation for destructive action
    target_name = channel_to_nuke.mention if channel_to_nuke != ctx.channel else "this channel"
    confirm_embed = discord.Embed(
        title="⚠️ Confirm nuke",
        description=f"Are you sure you want to nuke {target_name}? This will delete it and create a blank clone.\nReact with ✅ to confirm or ❌ to cancel.",
        color=discord.Colour.orange()
    )
    confirm_msg = await ctx.send(embed=confirm_embed)
    await confirm_msg.add_reaction("✅")
    await confirm_msg.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == confirm_msg.id and str(reaction.emoji) in ("✅", "❌")

    try:
        reaction, _ = await ctx.bot.wait_for("reaction_add", timeout=30.0, check=check)
    except Exception:
        await confirm_msg.edit(embed=discord.Embed(description="Nuke cancelled (timeout).", color=discord.Colour.red()))
        try:
            await confirm_msg.clear_reactions()
        except discord.Forbidden:
            pass
        return
    if str(reaction.emoji) != "✅":
        await confirm_msg.edit(embed=discord.Embed(description="Nuke cancelled.", color=discord.Colour.red()))
        try:
            await confirm_msg.clear_reactions()
        except discord.Forbidden:
            pass
        return
    try:
        await confirm_msg.delete()
    except discord.Forbidden:
        pass

    new_channel = None
    try:
        new_channel = await channel_to_nuke.clone(reason="Nuked!")
        await channel_to_nuke.delete(reason="Nuked!")
        await new_channel.send(f"{new_channel.mention} has been nuked! 💥💣")
    except discord.Forbidden:
        msg = "I don't have permission to manage this channel."
        try:
            await ctx.send(msg, delete_after=10)
        except discord.HTTPException:
            if new_channel:
                await new_channel.send(msg, delete_after=10)
    except discord.HTTPException as e:
        msg = f"Something went wrong: {e}"
        try:
            await ctx.send(msg, delete_after=10)
        except discord.HTTPException:
            if new_channel:
                await new_channel.send(msg, delete_after=10)
    except Exception as e:
        msg = f"Failed to nuke channel: {e}"
        try:
            await ctx.send(msg, delete_after=10)
        except discord.HTTPException:
            if new_channel:
                await new_channel.send(msg, delete_after=10)

@channel.command(description="Rename a specified channel.")
@commands.has_permissions(manage_channels=True)
async def rename(ctx, channel: discord.abc.GuildChannel, *, new_name):
    await channel.edit(name=new_name, reason="Channel rename")
    await ctx.channel.send(embed=discord.Embed(description=f'Channel renamed successfully to {channel.mention}.', color=discord.Color.blue()))

@channel.command(name='clone', description="Clone a specified channel.")
@commands.has_permissions(manage_channels=True)
async def clone(ctx, channel: discord.abc.GuildChannel):
    new_channel = await channel.clone(reason="Channel cloned")
    await ctx.send(f"{channel.mention} has been cloned to {new_channel.mention}.")


async def setup(bot):
    bot.add_command(channel)