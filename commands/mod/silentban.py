import discord
from discord.ext import commands

@commands.command(description="Ban a user from the server without sending any notification.")
@commands.has_permissions(ban_members=True)
async def silentban(ctx, user: discord.User):
    try:
        await ctx.guild.ban(user, delete_message_days=0)
        embed = discord.Embed(title="Silent Ban User", description=f"{user.name} has been silently banned from the server.", color=discord.Color.green())
        await ctx.send(embed=embed)
    except discord.NotFound:
        embed = discord.Embed(title="Silent Ban User", description="User not found.", color=discord.Color.red())
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(title="Silent Ban User", description="You don't have the required permissions to ban users.", color=discord.Color.red())
        await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(silentban)