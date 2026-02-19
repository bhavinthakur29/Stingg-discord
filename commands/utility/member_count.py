import discord
from discord.ext import commands

@commands.command(name='mc', description='Displays number of members in the server.')
async def member_count(ctx):
    total_members = ctx.guild.member_count
    total_humans = sum(not member.bot for member in ctx.guild.members)
    total_bots = sum(member.bot for member in ctx.guild.members)
    
    embed = discord.Embed(title='Member Count', description=f':100: : {total_members} members\n:man_bowing: : {total_humans} humans\n:robot: : {total_bots} bots', color=discord.Color.blue())
    await ctx.send(embed=embed)


async def setup(bot):
    bot.add_command(member_count)