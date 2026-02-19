import discord
from discord.ext import commands

warn_count = {}
max_warns = 3

@commands.command(description="Warn a user. Mute the user if warns exceed the maximum allowed warns.")
@commands.has_permissions(manage_roles=True)
async def warn(ctx, user: discord.Member, *, reason=None):
    if user.bot:
        await ctx.send("You can't warn a bot.")
        return

    if user.id not in warn_count:
        warn_count[user.id] = 1
    else:
        warn_count[user.id] += 1

    if user.id in max_warns and warn_count[user.id] > max_warns[user.id]:
        await ctx.invoke(ctx.bot.get_command('mute'), user=user, time="1h")
        warn_count[user.id] = 0
    else:
        await ctx.send(f"{user.mention} has been warned. Warn count: {warn_count[user.id]}")


@commands.command(description="Set the maximum allowed warns for all users.")
@commands.has_permissions(manage_guild=True)
async def setmaxwarns(ctx, limit: int):
    global max_warns
    if limit < 1:
        await ctx.send("The maximum allowed warns must be at least 1.")
        return

    max_warns = limit
    await ctx.send(f"The maximum allowed warns for all users has been set to {limit}.")


async def setup(bot):
    bot.add_command(warn)
    bot.add_command(setmaxwarns)