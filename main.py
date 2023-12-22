import discord
import os
import logging
import g4f
import asyncio
from discord.ext import commands
from discord import app_commands

g4f.debug.logging = False  # Enable debug logging
g4f.debug.check_version = False  # Disable automatic version checking

logger = logging.getLogger('discord')
logger.name = 'application'

EMBED_COLOR=0xFEC200

def simple_embed(title, text=''):
    embed = discord.Embed(title=title,description=text, color=EMBED_COLOR)
    return embed


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    logger.info("Bot is Online")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Chating"))
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.exception(e)

@bot.tree.command(name="ping")
async def ping(ctx):
    """
    Pings the bot and send a response with the time needed in ms

    Usage:
    !ping
    """
    await ctx.response.send_message(embed=simple_embed(f"Pong! {round(bot.latency * 1000)}ms"))

@bot.tree.command(name="base_prompt")
async def base_prompt(ctx, prompt: str):
    logger.info(prompt)
    await ctx.response.send_message(embed=simple_embed('Typing ...'))
    await asyncio.sleep(0)
    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        provider=g4f.Provider.You,
        messages=[{"role": "user", "content": f"{prompt}"}],
        stream=False,
    )
    full_response = ''.join(response)

    await ctx.edit_original_response(embed=simple_embed(f'{prompt[:255]}', full_response))

@bot.tree.command(name="linux_terminal")
async def linux_terminal(ctx, prompt: str):
    logger.info(prompt)
    await ctx.response.send_message(embed=simple_embed('Typing ...'))
    await asyncio.sleep(0)
    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        provider=g4f.Provider.You,
        messages=[{"role": "user", "content": "I want you to act as a linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. do not write explanations. do not type commands unless I instruct you to do so. When I need to tell you something in English, I will do so by putting text inside curly brackets {like this}. My first command is pwd"},
                  {"role": "user", "content": f"{prompt}"}],
        stream=False,
    )
    full_response = ''.join(response)

    await ctx.edit_original_response(embed=simple_embed(f'{prompt[:255]}', full_response))

bot.run(str(os.getenv('Token')))