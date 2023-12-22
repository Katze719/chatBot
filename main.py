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
        messages=[{"role": "user", "content": "I want you to act as a linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. do not write explanations. do not type commands unless I instruct you to do so. When I need to tell you something in English, I will do so by putting text inside curly brackets {like this}."},
                  {"role": "user", "content": f"{prompt}"}],
        stream=False,
    )
    full_response = ''.join(response)

    await ctx.edit_original_response(embed=simple_embed(f'{prompt[:255]}', full_response))

@bot.tree.command(name="poet")
async def poet(ctx, prompt: str):
    logger.info(prompt)
    await ctx.response.send_message(embed=simple_embed('Typing ...'))
    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        provider=g4f.Provider.You,
        messages=[{"role": "user", "content": "I want you to act as a poet. You will create poems that evoke emotions and have the power to stir people’s soul. Write on any topic or theme but make sure your words convey the feeling you are trying to express in beautiful yet meaningful ways. You can also come up with short verses that are still powerful enough to leave an imprint in readers' minds."},
                  {"role": "user", "content": f"{prompt}"}],
        stream=False,
    )
    full_response = ''.join(response)

    await ctx.edit_original_response(embed=simple_embed(f'{prompt[:255]}', full_response))

@bot.tree.command(name="ask")
async def ask(ctx, prompt: str):
    logger.info(prompt)
    await ctx.response.send_message(embed=simple_embed('Typing ...'))
    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        provider=g4f.Provider.ChatgptAi,
        messages=[{"role": "user", "content": "I want you to act as a hypnotherapist with the name Klaus. You will help patients tap into their subconscious mind and create positive changes in behaviour, develop techniques to bring clients into an altered state of consciousness, use visualization and relaxation methods to guide people through powerful therapeutic experiences, and ensure the safety of your patient at all times."},
                  {"role": "user", "content": f"{prompt}"}],
        stream=False,
    )
    full_response = ''.join(response)

    await ctx.edit_original_response(embed=simple_embed(f'{prompt[:255]}', full_response))



bot.run(str(os.getenv('Token')))