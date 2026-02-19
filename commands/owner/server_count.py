import discord
from discord.ext import commands

@commands.group(invoke_without_command=True)
@commands.is_owner()
async def server(ctx):
    available_subcommands = [command.name for command in server.commands]
    embed = discord.Embed(title='Available subcommands for `server`', description="\n".join(available_subcommands), color=discord.Colour.blue())
    await ctx.send(embed=embed)

@server.command(description="Display the number of servers the bot is in.")
async def count(ctx):
    total_members = 0
    for guild in ctx.bot.guilds:
        total_members += sum(1 for member in guild.members if not member.bot)
    guild_count = len(ctx.bot.guilds)
    await ctx.send(embed=discord.Embed(title='Server Count', description=f"I am currently monitoring `{total_members} members` (excluding bots) in `{guild_count} servers`.", color=discord.Color.blue()))

@server.command(description="Display the names of servers the bot is in.")
async def names(ctx):
    server_names = [guild.name for guild in ctx.bot.guilds]
    formatted_names = "\n".join(server_names)
    await ctx.send(embed=discord.Embed(title='Server Names', description=f"```{formatted_names}```", color=discord.Color.blue()))


async def setup(bot):
    bot.add_command(server)