from discord.ext import commands
import discord
from db.database import save_prefix, get_prefix, load_all_prefixes

# Populated at startup by main.py; prefix module uses bot.custom_prefixes
custom_prefixes = {}

# Get prefix function
def get_bot_prefix(bot, message):
    return custom_prefixes.get(message.guild.id, "s.")  # Default prefix

# Command to set prefix
@commands.command(name='prefix', aliases=['p'], description="Set a custom prefix for this server.")
@commands.has_permissions(manage_guild=True)
async def botPrefix(ctx, prefix: str):
    guild_id = ctx.guild.id
    print(f"Changing prefix for guild {guild_id} to '{prefix}'")
    
    # Save to MongoDB
    if save_prefix(guild_id, prefix):
        # Update both the module-level and bot's custom_prefixes dictionaries
        custom_prefixes[guild_id] = prefix
        ctx.bot.custom_prefixes[guild_id] = prefix

        embed = discord.Embed(
            title='Prefix changed',
            description=f"The custom prefix for this server has been changed to `{prefix}`.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Type `{prefix}help` for help commands.")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Error saving prefix. Please try again.")


async def setup(bot):
    bot.add_command(botPrefix)
    # Point module's custom_prefixes at bot's so the prefix command updates one dict
    import sys
    sys.modules['commands.utility.prefix'].custom_prefixes = bot.custom_prefixes