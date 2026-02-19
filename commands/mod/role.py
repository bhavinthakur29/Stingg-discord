import discord
from discord.ext import commands

@commands.group(name='role', invoke_without_command=True, description="Manages roles for members in a server.")
@commands.has_permissions(manage_roles=True)
async def role(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="User Roles Management", description="Available subcommands:", color=discord.Color.blue())
        embed.add_field(name="Give", value="Gives one or more roles to the mentioned user.", inline=False)
        embed.add_field(name="Remove", value="Removes one or more roles from the mentioned user.", inline=False)
        await ctx.send(embed=embed)


@role.command(name="give", description='Gives one or more roles to the mentioned user.')
async def give_role(ctx, member: discord.Member, *roles: discord.Role):
    given_roles = []
    
    for role in roles:
        if role not in member.roles:
            await member.add_roles(role)
            given_roles.append(role.mention)

    if given_roles:
        roles_mention = ", ".join(given_roles)
        embed = discord.Embed(
            title="Roles Given",
            description=f"Gave {roles_mention} roles to {member.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Roles Already Exist",
            description=f"All specified roles already exist for {member.mention}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)


@role.command(name="remove", description='Removes one or more roles from the mentioned user.')
async def remove_role(ctx, member: discord.Member, *roles: discord.Role):
    removed_roles = []

    for role in roles:
        if role in member.roles:
            await member.remove_roles(role)
            removed_roles.append(role.mention)

    if removed_roles:
        roles_mention = ", ".join(removed_roles)
        embed = discord.Embed(
            title="Roles Removed",
            description=f"Removed {roles_mention} roles from {member.mention}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Roles Not Found",
            description=f"{member.mention} does not have any of the specified roles",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)


async def setup(bot):
    bot.add_command(role)