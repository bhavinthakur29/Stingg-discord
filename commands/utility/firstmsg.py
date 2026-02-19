import discord
from discord.ext import commands

@commands.command(name='firstmsg', description='Takes the user to the very first message of a channel.')
async def firstmsg(ctx):
    channel = ctx.channel
    async for message in channel.history(limit=1, oldest_first=True):
        first_message = message
        break
    else:
        await ctx.send("No messages found in this channel.")
        return

    button = discord.ui.Button(style=discord.ButtonStyle.url, label="Go to First Message", url=first_message.jump_url)
    view = discord.ui.View()
    view.add_item(button)

    embed = discord.Embed(title="First Message", description="Click the button below to go to the first message in this channel:", color=discord.Color.blue())
    await ctx.send(embed=embed, view=view)


async def setup(bot):
    bot.add_command(firstmsg)