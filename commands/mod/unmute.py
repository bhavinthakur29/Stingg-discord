import discord
from discord.ext import commands

@commands.command(description="Unmute a previously muted user.")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, user: discord.Member):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    if not mute_role or mute_role not in user.roles:
        await ctx.send("User is not muted.")
        return

    await user.remove_roles(mute_role, reason=f"Unmuted by {ctx.author.name}.")
    await ctx.send(f"{user.mention} has been unmuted.")


async def setup(bot):
    bot.add_command(unmute)