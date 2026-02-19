import discord
from discord.ext import commands

@commands.group(name='clear', aliases=['purge', 'clean'], invoke_without_command=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = None):
    """Clears a number of recent messages."""
    if amount is None:
        await ctx.send("Please specify how many messages to delete. Example: `.clear 10`", delete_after=5)
        return

    if amount <= 0:
        await ctx.send("Amount must be greater than 0.", delete_after=5)
        return

    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Cleared {len(deleted) - 1} messages.", delete_after=5)

@clear.command(name='bot')
@commands.has_permissions(manage_messages=True)
async def clear_bot(ctx, amount: int = 50):
    """Clears messages sent by bots."""
    limit = min(max(1, amount), 100) + 1
    deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author.bot, before=ctx.message)
    await ctx.send(f"Cleared {len(deleted)} bot messages.", delete_after=5)

@clear.command(name='human')
@commands.has_permissions(manage_messages=True)
async def clear_human(ctx, amount: int = 10):
    """Clears messages sent by human users."""
    limit = min(max(1, amount), 100) + 1
    deleted = await ctx.channel.purge(limit=limit, check=lambda m: not m.author.bot, before=ctx.message)
    await ctx.send(f"Cleared {len(deleted)} human messages.", delete_after=5)

@clear.command(name='user')
@commands.has_permissions(manage_messages=True)
async def clear_user(ctx, user: discord.User, amount: int = 10):
    """Clears messages from a specific user (mention or ID)."""
    limit = min(max(1, amount), 100) + 1
    deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author.id == user.id, before=ctx.message)
    await ctx.send(f"Cleared {len(deleted)} messages from {user.mention}.", delete_after=5)


async def setup(bot):
    bot.add_command(clear)