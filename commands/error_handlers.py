import discord
from discord.ext import commands

async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        prefix = ctx.prefix
        await ctx.send(
            f"Command not found. Use `{prefix}help` for a list of commands.",
            delete_after=5
        )
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please check the command usage.", delete_after=5)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Bad argument. Please provide a valid argument.", delete_after=5)
    else:
        await ctx.send("An error occurred. Please try again or check the command usage.", delete_after=5)

async def on_error(event, *args, **kwargs):
    print(f"An error occurred in {event}: {args!r}")
