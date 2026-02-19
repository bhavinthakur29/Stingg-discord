import discord
from discord.ext import commands

def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

@commands.command(name='nick', description="Change the nickname of a user.")
@is_admin()
async def nick(ctx, user: discord.Member, new_nickname: str):
    await user.edit(nick=new_nickname)
    embed = discord.Embed(title="Nickname Changed", description="Successfully changed {}'s nickname to **{}**.".format(user.name.mention, new_nickname), color=discord.Color.green())
    await ctx.send(embed=embed)


async def setup(bot):
    bot.add_command(nick)