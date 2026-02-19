import discord
from discord.ext import commands

@commands.command(description="Unban a user from the server.")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):
    try:
        await ctx.guild.unban(user)
        embed = discord.Embed(title="Unban User", description=f"{user.name} has been unbanned from the server.", color=discord.Color.green())
        await ctx.send(embed=embed)
    except discord.NotFound:
        embed = discord.Embed(title="Unban User", description="User not found or not banned.", color=discord.Color.red())
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(title="Unban User", description="You don't have the required permissions to unban users.", color=discord.Color.red())
        await ctx.send(embed=embed)


async def setup(bot):
    bot.add_command(unban)