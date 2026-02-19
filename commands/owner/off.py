import discord
import asyncio
from discord.ext import commands

@commands.command(name='off', description='OWNER ONLY: Shuts the bot down.')
@commands.is_owner()
async def off(ctx):
    powering_off = discord.Embed(title=":mobile_phone_off:Powering Off", description="Attempting to Power Off ...", color=0xFF0000)
    deleting_logs = discord.Embed(title=":mobile_phone_off:Powering Off", description="Deleting saved logs from console ...", color=0xFF0000)
    deleting_prefixes = discord.Embed(title=":mobile_phone_off:Powering Off", description="Saving state and cleaning up ...", color=0xFF0000)
    erasing_bot_data = discord.Embed(title=":mobile_phone_off:Powering Off", description="Erasing all bot data for security concerns ...", color=0xFF0000)
    goodbye = discord.Embed(description="```diff\n-GOOD BYE!\n- SEE YOU SOON AROUND.```", color=0xFF0000)

    message = await ctx.send(embed=powering_off)

    try:
        await asyncio.sleep(2)
        await message.edit(embed=deleting_logs)
        await asyncio.sleep(0.5)
        await message.edit(embed=deleting_prefixes)
        await asyncio.sleep(0.5)
        await message.edit(embed=erasing_bot_data)
        await asyncio.sleep(2)
        await message.edit(embed=goodbye)
    except discord.NotFound:
        pass

    print(f'{ctx.bot.user.name}#{ctx.bot.user.discriminator} turned off.')
    await ctx.bot.close()


async def setup(bot):
    bot.add_command(off)