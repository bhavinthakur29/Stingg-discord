import discord
from discord.ext import commands
import asyncio

TIME_UNITS = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400
}

@commands.command(description="Mute a user for a specified duration.")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, user: discord.Member, duration: str = None):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted", reason="Creating Muted role for muting users.")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False)

    if mute_role in user.roles:
        await ctx.send("User is already muted.")
        return

    if duration is None:
        await user.add_roles(mute_role, reason=f"Muted indefinitely by {ctx.author.name}.")
        await ctx.send(f"{user.mention} has been muted indefinitely.")
    else:
        duration = duration.lower()
        time_unit = duration[-1]
        if time_unit not in TIME_UNITS:
            await ctx.send("Invalid duration format. Please use a valid time unit (s/m/h/d).")
            return

        time_value = int(duration[:-1])
        time_in_seconds = time_value * TIME_UNITS[time_unit]

        await user.add_roles(mute_role, reason=f"Muted for {duration} by {ctx.author.name}.")
        await ctx.send(f"{user.mention} has been muted for {duration}.")

        await asyncio.sleep(time_in_seconds)
        if mute_role in user.roles:
            await user.remove_roles(mute_role, reason=f"Unmuted automatically after {duration}.")


async def setup(bot):
    bot.add_command(mute)