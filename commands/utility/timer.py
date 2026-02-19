import asyncio, re, discord
from discord.ext import commands

@commands.command(aliases=['t'], description='Starts a countdown timer for the time specified.')
async def timer(ctx, duration: str):
    time_regex = re.compile(r'(\d+)([smh])')
    match = time_regex.findall(duration)
    if not match:
        await ctx.send("Invalid duration. Please use the format '.timer 10s' or '.timer 1m10s'.")
        return

    total_seconds = 0
    for amount, unit in match:
        if unit == 's':
            total_seconds += int(amount)
        elif unit == 'm':
            total_seconds += int(amount) * 60
        elif unit == 'h':
            total_seconds += int(amount) * 3600

    remaining_seconds = total_seconds
    embed = discord.Embed(title=":alarm_clock:Timer", color=discord.Color.blue())
    embed.add_field(name="Time Remaining:", value=f"{remaining_seconds} seconds")

    message = await ctx.send(embed=embed)
    await ctx.defer()

    while remaining_seconds > 0:
        await asyncio.sleep(5)
        remaining_seconds -= 5
        embed.set_field_at(0, name="Time Remaining", value=f"{remaining_seconds} seconds")
        await message.edit(embed=embed)

    await ctx.send(f"{ctx.author.mention}, your timer has ended!", delete_after=10)


async def setup(bot):
    bot.add_command(timer)