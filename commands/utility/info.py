import discord
from discord.ext import commands

@commands.group(invoke_without_command=True)
async def info(ctx):
    available_subcommands = [command.name for command in info.commands]
    embed = discord.Embed(title='Available subcommands for `info`', description="\n".join(available_subcommands), color=discord.Colour.blue())
    await ctx.send(embed=embed)

@info.command(name='role', description='Gives info about a role.')
async def info_role(ctx, *, role: discord.Role):
    embed = discord.Embed(title=f'Information for {role.name} role', color=role.color)
    embed.add_field(name='ID', value=role.id, inline=False)
    embed.add_field(name='Created At', value=role.created_at.strftime('%Y-%m-%d | %H:%M:%S'), inline=False)
    embed.add_field(name='Color', value=str(role.color), inline=False)
    embed.add_field(name='Members', value=len(role.members), inline=False)
    embed.add_field(name='Mentionable', value=role.mentionable, inline=False)
    embed.add_field(name='Position', value=role.position, inline=False)
    embed.add_field(name='Hoisted', value=role.hoist, inline=False)

    await ctx.send(embed=embed)

@info.command(name='user', description='Gives info about a user.')
async def info_user(ctx, *, user: discord.User = None):
    if not user:
        user = ctx.author

    if isinstance(user, int):
        try:
            user = await ctx.bot.fetch_user(user)
        except discord.NotFound:
            await ctx.send("User not found.")
            return

    if user:
        embed = discord.Embed(title=f'Information for {user.name}', color=discord.Color.blue())

        try:
            embed.set_thumbnail(url=user.avatar.url)
        except AttributeError:
            pass

        embed.add_field(name='ID', value=user.id, inline=False)
        embed.add_field(name='Created At', value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

        if isinstance(user, discord.Member):
            embed.add_field(name='Joined At', value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
            embed.add_field(name='Top Role', value=user.top_role.mention, inline=False)

            if user.guild_permissions.administrator:
                embed.add_field(name='Server Role', value='Administrator', inline=False)
            else:
                moderator_permissions = [
                    discord.Permissions.manage_guild,
                    discord.Permissions.manage_channels,
                    discord.Permissions.manage_roles,
                    discord.Permissions.manage_messages
                ]
                if any(permission in user.guild_permissions for permission in moderator_permissions):
                    embed.add_field(name='Server Role', value='Moderator', inline=False)
                else:
                    embed.add_field(name='Server Role', value='Member', inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Invalid user ID.")

def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

@info.command(name='server', description='Get information about the server')
@is_admin()
async def server(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Server Information", color=discord.Color.blue())
    embed.set_thumbnail(url=guild.icon)
    embed.set_author(name=f"{guild.name}'s Information", icon_url=ctx.bot.user.avatar.url)
    embed.set_footer(text=f'Requested by {ctx.message.author.name} • {ctx.message.created_at.strftime("%Y-%m-%d | %H:%M:%S")}', icon_url=ctx.author.display_avatar)

    bans_list = [entry.user async for entry in ctx.guild.bans()]
    embed.add_field(name="\n\n__About__", value=f'**Name:** {guild.name}\n**ID:** {guild.id}\n**Owner:crown::** {guild.owner.mention}\n**Created:** {guild.created_at.strftime("%Y-%m-%d | %H:%M:%S")}\n**Members:** {guild.member_count}\n**Banned:** {len(bans_list)}', inline=False)
    
    embed.add_field(name="\n\n__Description__", value=f'> {guild.description}', inline=False)
    
    verification = guild.verification_level
    mfa = guild.mfa_level
    auth = (":x:" if 'disabled' in mfa else ":white_check_mark:" if 'require_2fa' in mfa else "Unknown")
    noti = guild.default_notifications.value
    notifications = ("Only mentions" if noti == 1 else "All messages")
    embed.add_field(name="\n\n__Additional__", value=f'**Channels:** {len(guild.channels)}\n**Roles:** {len(guild.roles)}\n**Verification Level:** {str(verification).title()}\n**Upload Limit:** {"No Boosts Available" if "NitroBoost" not in guild.features else guild.max_upload_size}\n**Inactive Channel:** {guild.afk_channel.mention}\n**System Messages Channel:** {guild.system_channel.mention}\n**Explicit Media Content Filter:** {":white_check_mark:" if guild.explicit_content_filter else ":x:"}\n**Boost Status:** {f"Level: {guild.premium_tier} [:sparkles: {guild.premium_subscription_count} boosts]"}\n**2FA Requirement:** {auth}\n**Default Notifications:** {notifications}\n**Emojis:** {len(guild.emojis)}', inline=False)
    
    await ctx.send(embed=embed)


async def setup(bot):
    bot.add_command(info)