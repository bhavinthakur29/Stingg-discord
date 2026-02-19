import discord
import asyncio
from discord.ext import commands

@commands.group(invoke_without_command=True)
async def listing(ctx):
    available_subcommands = [c.name for c in listing.commands]
    embed = discord.Embed(title='Available subcommands for `listing`', description="\n".join(available_subcommands), color=discord.Colour.blue())
    await ctx.send(embed=embed)


@listing.command(name='admins', description="List all administrators.")
async def list_admins(ctx):
    admins_list = [f"{member.name} ({member.mention})" for member in ctx.guild.members if not member.bot and member.guild_permissions.administrator]
    if admins_list:
        embed = discord.Embed(title='Admins', description='\n'.join(admins_list), color=discord.Colour.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description='No admins found', color=discord.Colour.red())
        await ctx.send(embed=embed)

@listing.command(name='mods', description="List all moderators.")
async def list_mods(ctx):
    mods_list = [f"{member.name} ({member.mention})" for member in ctx.guild.members if not member.bot and any(permission in member.guild_permissions for permission in [
        discord.Permissions.manage_guild,
        discord.Permissions.manage_channels,
        discord.Permissions.manage_roles,
        discord.Permissions.manage_messages
    ])]
    if mods_list:
        embed = discord.Embed(title='Mods', description='\n'.join(mods_list), color=discord.Colour.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description='No moderators found', color=discord.Colour.red())
        await ctx.send(embed=embed)

@listing.command(name='norole', description="List all members without any roles.")
async def list_norole(ctx):
    norole_list = [f"{member.display_name} ({member.mention})" for member in ctx.guild.members if not member.bot and len(member.roles) == 1]
    if norole_list:
        embed = discord.Embed(title='No Role', description='\n'.join(norole_list), color=discord.Colour.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description='No members found without roles.', color=discord.Colour.green())
        await ctx.send(embed=embed)

@listing.command(name='role', description="List members with a specific role.")
async def list_role(ctx, role_id: int):
    role = discord.utils.get(ctx.guild.roles, id=role_id)
    if role is None:
        await ctx.send("Role not found.")
        return

    role_list = [f"{member.display_name} ({member.mention})" for member in ctx.guild.members if role in member.roles]
    if role_list:
        embed = discord.Embed(title=f'Members with {role.name} role', description='\n'.join(role_list), color=role.color)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f"No members found with {role.name} role.", color=discord.Colour.red())
        await ctx.send(embed=embed)

@listing.command(name='roles', description="List all roles in the server.")
async def list_roles(ctx):
    allroles_list = [role.name for role in ctx.guild.roles]
    if allroles_list:
        embed = discord.Embed(title='All Roles', description='\n'.join(allroles_list), color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="No roles found in this server.", color=discord.Colour.red())
        await ctx.send(embed=embed)

@listing.command(name='channels', description="List all channels in the server.")
async def list_channels(ctx):
    channel_names = [ch.name for ch in ctx.guild.channels]
    if channel_names:
        embed = discord.Embed(title='All Channels', description='\n'.join(channel_names), color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="No channels found in this server.", color=discord.Colour.red())
        await ctx.send(embed=embed)

@listing.command(name='bots', description="List all bots in the server.")
async def list_bots(ctx):
    bots_list = [f"{member.display_name} ({member.mention})" for member in ctx.guild.members if member.bot]
    if bots_list:
        embed = discord.Embed(title='Bots', description='\n'.join(bots_list), color=discord.Colour.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description='No bots found', color=discord.Colour.red())
        await ctx.send(embed=embed)

@listing.command(name='bans', description="List all banned members in the server with their mentions.")
async def list_bans(ctx):
    banned_members = [entry.user async for entry in ctx.guild.bans()]
    embed = discord.Embed(title="Ban Count", description=f"There are {len(banned_members)} users banned in this server.")
    embed.add_field(name="Banned Members", value="\n".join([f"{banned_member.name} `ID: {banned_member.id}`" for banned_member in banned_members]))
    await ctx.send(embed=embed)

@listing.command(name='recent', description="List last 15 messages of the specified user.")
async def list_recent(ctx, user_id: int):
    try:
        user = await ctx.bot.fetch_user(user_id)
    except discord.NotFound:
        await ctx.send("User not found.")
        return

    user_messages = []
    async for message in ctx.channel.history(limit=100):  # Increase the limit if needed
        if message.author.id == user.id:
            user_messages.append(f"{message.content} - {message.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    if user_messages:
        user_messages.reverse()
        messages_str = "\n".join(user_messages[:15])  # Display only the last 15 messages
        display = getattr(user, "global_name", None) or user.name
        embed = discord.Embed(title=f"Last 15 Messages of {display}", description=messages_str, color=discord.Colour.blue())
        await ctx.send(embed=embed)
    else:
        display = getattr(user, "global_name", None) or user.name
        await ctx.send(f"No recent messages found for {display}.")

async def setup(bot):
    bot.add_command(listing)