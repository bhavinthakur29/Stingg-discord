import discord
from discord.ext import commands

def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

@commands.group(name='voice', invoke_without_command=True, description="Voice channel management commands.")
@is_admin()
async def voice(ctx):
    embed = discord.Embed(title="Voice Channel Management", description="Available subcommands:", color=discord.Color.blue())
    embed.add_field(name="Mute", value="Mute a user in a voice channel.", inline=False)
    embed.add_field(name="Unmute", value="Unmute a user in a voice channel.", inline=False)
    embed.add_field(name="Kick", value="Kick a user from a voice channel.", inline=False)
    embed.add_field(name="Deafen", value="Deafen a user in a voice channel.", inline=False)
    embed.add_field(name="Undeafen", value="Undeafen a user in a voice channel.", inline=False)
    embed.add_field(name="Move", value="Move a user to a different voice channel.", inline=False)
    await ctx.send(embed=embed)

@voice.command(name='mute', description="Mute a user in a voice channel.")
@is_admin()
async def mute(ctx, member: discord.Member):
    if not isinstance(ctx.author.voice.channel, discord.VoiceChannel):
        embed = discord.Embed(description=":x: You must be in a voice channel to use this command.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    await member.edit(mute=True)
    embed = discord.Embed(description=f":mute: Muted {member.mention} in {ctx.author.voice.channel.name}.", color=discord.Color.green())
    await ctx.send(embed=embed)

@voice.command(name='unmute', description="Unmute a user in a voice channel.")
@is_admin()
async def unmute(ctx, member: discord.Member):
    if not isinstance(ctx.author.voice.channel, discord.VoiceChannel):
        embed = discord.Embed(description=":x: You must be in a voice channel to use this command.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    await member.edit(mute=False)
    embed = discord.Embed(description=f":loud_sound: Unmuted {member.mention} in {ctx.author.voice.channel.name}.", color=discord.Color.green())
    await ctx.send(embed=embed)

@voice.command(name='kick', description="Kick a user from a voice channel.")
@is_admin()
async def kick(ctx, member: discord.Member=None):
    if member.voice:
        await member.move_to(None)
        await ctx.message.add_reaction('👢')
    else:
        await ctx.send(f":x: {member.mention} is not in a voice channel.")

@voice.command(name='deafen', description="Deafen a user in a voice channel.")
@is_admin()
async def deafen(ctx, member: discord.Member):
    if not isinstance(ctx.author.voice.channel, discord.VoiceChannel):
        embed = discord.Embed(description=":x: You must be in a voice channel to use this command.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    await member.edit(deafen=True)
    embed = discord.Embed(description=f":mute: Deafened {member.mention} in {ctx.author.voice.channel.name}.", color=discord.Color.green())
    await ctx.send(embed=embed)

@voice.command(name='undeafen', description="Undeafen a user in a voice channel.")
@is_admin()
async def undeafen(ctx, member: discord.Member):
    if not isinstance(ctx.author.voice.channel, discord.VoiceChannel):
        embed = discord.Embed(description=":x: You must be in a voice channel to use this command.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    await member.edit(deafen=False)
    embed = discord.Embed(description=f":loud_sound: Undeafened {member.mention} in {ctx.author.voice.channel.name}.", color=discord.Color.green())
    await ctx.send(embed=embed)

async def join_author_vc(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await ctx.bot.join_voice_channel(channel)

async def move_all_members(ctx, new_channel):
    if ctx.author.voice and ctx.author.voice.channel:
        old_channel = ctx.author.voice.channel
        for member in old_channel.members:
            await member.move_to(new_channel)

@voice.command(name='move', description="Move a user to the bot's voice channel.")
@is_admin()
async def move(ctx, target_channel: discord.VoiceChannel):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send('You must be in a voice channel to use this command.')
        return

    members = ctx.author.voice.channel.members

    for member in members:
        await member.move_to(target_channel)
    await ctx.send(f'Successfully moved all users from {ctx.author.voice.channel.mention} to {target_channel.mention}.')


async def setup(bot):
    bot.add_command(voice)