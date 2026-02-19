import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from langdetect import detect
import langcodes

@commands.command(description="Translate a message to English.")
async def translate(ctx, *, message: str):
    try:
        language_code = detect(message)
        
        language = langcodes.Language.get(language_code).display_name()

        translated = GoogleTranslator(source='auto', target='en').translate(message)
        await ctx.send(embed=discord.Embed(title=f"Translation ({language})", description=translated))
    except Exception as e:
        await ctx.send(f"Translation failed.\n```{e}```")
