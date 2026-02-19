"""
Help command: categories and per-command help.
Categories match the actual loaded commands (Owner, Moderation, Utility).
"""
import os
import discord
from discord.ext import commands
from discord.ext.commands import Group
from dotenv import load_dotenv

load_dotenv()
INVITE = os.getenv("INVITE_LINK") or ""


# Single source of truth: category name -> list of (command name, short description)
CATEGORIES = {
    "Owner": [
        ("off", "Shuts the bot down."),
        ("server", "Server count and names. Subcommands: `count`, `names`."),
        ("uptime", "Display the bot's uptime."),
    ],
    "Moderation": [
        ("ban", "Ban a user from the server. Sends a DM."),
        ("kick", "Kick a user from the server."),
        ("mute", "Mute a user (optional duration)."),
        ("unmute", "Unmute a previously muted user."),
        ("warn", "Warn a user. Auto-mute after max warns."),
        ("setmaxwarns", "Set the maximum warns before auto-mute."),
        ("silentban", "Ban a user without notifying them."),
        ("unban", "Unban a user by ID."),
        ("voice", "Voice channel management. Subcommands: mute, unmute, kick, deafen, undeafen, move."),
        ("nick", "Change a member's nickname."),
        ("role", "Role management. Subcommands: `give`, `remove`."),
        ("clear", "Delete messages. Subcommands: bot, human, user; or use with amount."),
    ],
    "Utility": [
        ("avatar", "Display a user's or server's avatar/banner. Aliases: av."),
        ("channel", "Channel management. Subcommands: nuke, rename, clone."),
        ("prefix", "Set this server's command prefix. Aliases: p."),
        ("firstmsg", "Jump to the first message in this channel."),
        ("info", "Info subcommands: role, user, server."),
        ("listing", "List subcommands: admins, mods, norole, role, roles, channels, bots, bans, recent."),
        ("mc", "Member count in this server."),
        ("timer", "Countdown timer. Alias: t."),
        ("translate", "Translate text to English."),
        ("join", "Connect the bot to your voice channel."),
        ("leave", "Disconnect the bot from voice."),
        ("vcc", "Count users in a voice channel by ID."),
    ],
}


def _bot_avatar(ctx):
    if ctx.bot.user.avatar:
        return ctx.bot.user.avatar.url
    return ctx.bot.user.default_avatar.url


def _usage_embed():
    return discord.Embed(
        description="```diff\n- <> = required\n- [] = optional```",
        color=discord.Color.blue(),
    )


@commands.group(name="help", invoke_without_command=True, description="List categories and command help.")
async def help_command(ctx, *, query: str = None):
    prefix = ctx.prefix
    bot_name = ctx.bot.user.name
    avatar_url = _bot_avatar(ctx)
    # First word only (e.g. "help ban" or "help owner")
    category_or_command = (query or "").strip().split()[0] if query else None

    # If no argument, show main help with categories
    if not category_or_command:
        embed = discord.Embed(title=bot_name, color=discord.Color.blue())
        embed.set_author(name=bot_name, icon_url=avatar_url)
        embed.set_footer(text=f"Use `{prefix}help <category>` or `{prefix}help <command>`")
        invite_line = f"\n[Invite]({INVITE})" if INVITE else ""
        embed.description = (
            f"Prefix for this server: `{prefix}`\n"
            f"Use `{prefix}help owner`, `{prefix}help moderation`, or `{prefix}help utility` for a category.\n"
            f"Use `{prefix}help <command>` for details on a command.{invite_line}"
        )
        value = "• :crown: Owner\n• :shield: Moderation\n• :gear: Utility"
        embed.add_field(name="Categories", value=value, inline=True)
        await ctx.send(embed=embed)
        return

    arg = category_or_command.lower()

    # Category pages
    if arg == "owner":
        await _send_category(ctx, "Owner", ":crown: Owner commands", prefix, avatar_url)
        return
    if arg == "moderation" or arg == "mod":
        await _send_category(ctx, "Moderation", ":shield: Moderation commands", prefix, avatar_url)
        return
    if arg == "utility":
        await _send_category(ctx, "Utility", ":gear: Utility commands", prefix, avatar_url)
        return

    # Per-command help: try custom handler first, then generic
    cmd = ctx.bot.get_command(arg)
    if cmd:
        await _send_command_help(ctx, cmd, prefix, avatar_url)
        return

    # Unknown
    await ctx.send(f"No category or command named `{arg}`. Use `{prefix}help` for categories.", delete_after=5)


async def _send_category(ctx, category_key, title, prefix, avatar_url):
    embed = discord.Embed(title=title, color=discord.Color.blue())
    embed.set_author(name=ctx.bot.user.name, icon_url=avatar_url)
    embed.set_footer(text=f"Use `{prefix}help <command>` for usage.")
    for name, desc in CATEGORIES.get(category_key, []):
        embed.add_field(name=f"{prefix}{name}", value=desc, inline=False)
    await ctx.send(embed=embed)


async def _send_command_help(ctx, cmd, prefix, avatar_url):
    """Send help for a command. Uses custom embeds for known commands, else generic."""
    name = cmd.name
    custom = _CUSTOM_HELP.get(name)
    if custom:
        embed = custom(ctx, prefix, avatar_url)
        await ctx.send(embed=embed)
        return
    # Generic: description + signature; for groups list subcommands
    embed = discord.Embed(title=f"{prefix}{name}", color=discord.Color.blue())
    embed.set_author(name="Help", icon_url=avatar_url)
    if cmd.help:
        embed.description = cmd.help
    if isinstance(cmd, Group) and cmd.commands:
        sub = ", ".join(f"`{c.name}`" for c in sorted(cmd.commands, key=lambda c: c.name))
        embed.add_field(name="Subcommands", value=sub, inline=False)
    if hasattr(cmd, "clean_params") and cmd.clean_params:
        params = " ".join(f"<{p}>" for p in cmd.clean_params if p != "ctx")
        if params.strip():
            embed.add_field(name="Usage", value=f"`{prefix}{name} {params.strip()}`", inline=False)
    await ctx.send(embed=embed)


def _custom_embed_base(ctx, title, prefix, avatar_url):
    embed = _usage_embed()
    embed.set_author(name=title, icon_url=avatar_url)
    return embed


# Custom detailed help for commands that need usage/params
def _help_ban(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Ban a user and optionally send a DM.", inline=False)
    e.add_field(name="Parameters", value="`user` – user to ban\n`reason` – (optional) reason", inline=False)
    e.add_field(name="Usage", value=f"`{prefix}ban <user> [reason]`", inline=False)
    return e


def _help_kick(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Kick a user from the server.", inline=False)
    e.add_field(name="Parameters", value="`user` – user to kick\n`reason` – (optional)", inline=False)
    e.add_field(name="Usage", value=f"`{prefix}kick <user> [reason]`", inline=False)
    return e


def _help_mute(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Mute a user. Duration optional (indefinite if omitted).", inline=False)
    e.add_field(name="Parameters", value="`user` – user to mute\n`duration` – (optional) e.g. 1h, 30m", inline=False)
    e.add_field(name="Usage", value=f"`{prefix}mute <user> [duration]`", inline=False)
    return e


def _help_silentban(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Ban without notifying the user.", inline=False)
    e.add_field(name="Usage", value=f"`{prefix}silentban <user>`", inline=False)
    return e


def _help_unban(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Unban a user by ID.", inline=False)
    e.add_field(name="Usage", value=f"`{prefix}unban <user_id>`", inline=False)
    return e


def _help_unmute(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Unmute a previously muted user.", inline=False)
    e.add_field(name="Usage", value=f"`{prefix}unmute <user>`", inline=False)
    return e


def _help_warn(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Warn a user. Use `setmaxwarns` to set auto-mute threshold.", inline=False)
    e.add_field(name="Parameters", value="`user` – user to warn\n`reason` – (optional)", inline=False)
    e.add_field(name="Usage", value=f"`{prefix}warn <user> [reason]`", inline=False)
    return e


def _help_setmaxwarns(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Set how many warns before auto-mute.", inline=False)
    e.add_field(name="Usage", value=f"`{prefix}setmaxwarns <number>`", inline=False)
    return e


def _help_voice(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Voice channel management.", inline=False)
    e.add_field(name="Subcommands", value=(
        f"`{prefix}voice mute <user>` – Mute in VC\n"
        f"`{prefix}voice unmute <user>` – Unmute in VC\n"
        f"`{prefix}voice kick <user>` – Kick from VC\n"
        f"`{prefix}voice deafen <user>` – Deafen\n"
        f"`{prefix}voice undeafen <user>` – Undeafen\n"
        f"`{prefix}voice move <user>` – Move users to another channel"
    ), inline=False)
    return e


def _help_nick(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Change a member's nickname.", inline=False)
    e.add_field(name="Usage", value=f"`{prefix}nick <user> <new_nickname>`", inline=False)
    return e


def _help_role(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Give or remove roles.", inline=False)
    e.add_field(name="Usage", value=(
        f"`{prefix}role give <user> <role> [role...]`\n"
        f"`{prefix}role remove <user> <role> [role...]`"
    ), inline=False)
    return e


def _help_clear(ctx, prefix, avatar_url):
    e = _custom_embed_base(ctx, "Moderation", prefix, avatar_url)
    e.add_field(name="", value="> Delete messages. Use with amount or subcommands.", inline=False)
    e.add_field(name="Usage", value=(
        f"`{prefix}clear <amount>` – delete that many messages\n"
        f"`{prefix}clear bot [amount]` – delete bot messages\n"
        f"`{prefix}clear human [amount]` – delete user messages\n"
        f"`{prefix}clear user <user> [amount]` – delete messages from a user"
    ), inline=False)
    return e


_CUSTOM_HELP = {
    "ban": _help_ban,
    "kick": _help_kick,
    "mute": _help_mute,
    "silentban": _help_silentban,
    "unban": _help_unban,
    "unmute": _help_unmute,
    "warn": _help_warn,
    "setmaxwarns": _help_setmaxwarns,
    "voice": _help_voice,
    "nick": _help_nick,
    "role": _help_role,
    "clear": _help_clear,
}


async def setup(bot):
    bot.add_command(help_command)
