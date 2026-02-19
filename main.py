import discord, os, asyncio, nacl
from discord.ext import commands
from dotenv import load_dotenv
import importlib.util

from commands.utility.prefix import load_all_prefixes
from commands.error_handlers import on_command_error, on_error
from commands.helpcommand import help_command   
from commands.utility.translate import translate

load_dotenv()

token = os.getenv('BOT_TOKEN')

# Default prefix for servers that haven't set one and for DMs
DEFAULT_PREFIX = "s."

def get_prefix(bot, message):
    """Only server-specific prefixes (from MongoDB); default if none set."""
    if message.guild:
        return bot.custom_prefixes.get(message.guild.id, DEFAULT_PREFIX)
    return DEFAULT_PREFIX

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)
# bot = commands.Bot(command_prefix=get_prefix, intents=intents)

# Admin check
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

# Set bot status
@bot.event
async def on_ready():
    print(f'{bot.user.name} #{bot.user.discriminator} has connected to Discord({discord.__version__})')
    status_messages = [
        discord.Activity(type=discord.ActivityType.listening, name=f"{DEFAULT_PREFIX}help"),
        discord.Activity(type=discord.ActivityType.watching, name="Unique commands"),
        discord.Activity(type=discord.ActivityType.competing, name="Bot Race")
    ]
    current_status = 0
    while True:
        await bot.change_presence(activity=status_messages[current_status], status=discord.Status.online)
        current_status = (current_status + 1) % len(status_messages)
        await asyncio.sleep(10)

# Command auto-loader
async def load_commands_from_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                path = os.path.join(root, file)
                module_name = path.replace("/", ".").replace("\\", ".")[:-3]  # Remove `.py`
                spec = importlib.util.spec_from_file_location(module_name, path)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    if hasattr(module, "setup"):
                        await module.setup(bot)
                        print(f"[OK] Loaded: {module_name}")
                except Exception as e:
                    print(f"[FAIL] {module_name}: {e}")

# Custom command: .cmd and .cmdhelp
@bot.command(name='cmd', with_app_command=True)
async def cmd(ctx):
    command_names = sorted([c.name for c in bot.commands])
    embed = discord.Embed(title=f"Available Commands ({len(command_names)})", color=discord.Color.blue())
    for i in range(0, len(command_names), 10):
        embed.add_field(name=f"{i+1}-{i+10}", value="\n".join(command_names[i:i+10]), inline=True)
    embed.set_footer(text=f'Type `{ctx.prefix}cmdhelp` for info.')
    try:
        await ctx.author.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("I can't DM you. Please allow DMs from this server.", delete_after=5)

@bot.command()
async def cmdhelp(ctx):
    embed = discord.Embed(title="Command Help", color=discord.Color.green())
    for c in bot.commands:
        if c.help:
            embed.add_field(name=c.name, value=c.help, inline=False)
    try:
        await ctx.author.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("I can't DM you. Please allow DMs from this server.", delete_after=5)

# Mention prefix reply: show this server's prefix only
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.guild and bot.user.mentioned_in(message):
        server_prefix = bot.custom_prefixes.get(message.guild.id, DEFAULT_PREFIX)
        embed = discord.Embed(
            description=f"My prefix for this server is `{server_prefix}`. Use `{server_prefix}help` for commands.",
            color=discord.Color.blue()
        )
        await message.channel.send(embed=embed)
        return
    await bot.process_commands(message)

# Change command name
@bot.command()
async def change(ctx, old_command_name: str, new_command_name: str):
    old_command = bot.get_command(old_command_name)
    if old_command:
        async def new_command(ctx):
            await old_command.callback(ctx)
        bot.remove_command(old_command_name)
        bot.add_command(commands.Command(new_command, name=new_command_name))
        await ctx.send(f"Renamed `{old_command_name}` → `{new_command_name}`.")
    else:
        await ctx.send(f"Command `{old_command_name}` not found.")

# Example ping command
@bot.command()
@is_admin()
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(embed=discord.Embed(description=f'Pong! `{latency:.2f}ms`'), delete_after=10)

# Add error handlers
bot.add_listener(on_command_error, 'on_command_error')
bot.add_listener(on_error, 'on_error')

# Loading the command externally
bot.add_command(help_command)
bot.add_command(translate)


async def main():
    async with bot:
        bot.custom_prefixes = load_all_prefixes()
        print(f"Loaded {len(bot.custom_prefixes)} custom prefixes at startup")

        await load_commands_from_folder("commands")
        await bot.start(token)

asyncio.run(main())
