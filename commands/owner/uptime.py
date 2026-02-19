import time, discord
from discord.ext import commands

start_time = time.time()

@commands.command(description="Displays the bot's uptime.")
@commands.is_owner()
async def uptime(ctx):
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    await ctx.send(embed=discord.Embed(title=':green_circle: UPTIME',description=f"**I have been running for: `{uptime_str}`**", color=discord.Color.green()))


async def setup(bot):
    bot.add_command(uptime)