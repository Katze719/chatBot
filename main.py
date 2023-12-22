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
        provider=g4f.Provider.GptGo,
        messages=[{"role": "user", "content": f"{prompt}"}],
        stream=False,
    )
    full_response = ''.join(response)

    await ctx.edit_original_response(embed=simple_embed(f'{prompt[:255]}', full_response))

@bot.tree.command(name="tech_support")
async def tech_support(ctx, prompt: str):
    logger.info(prompt)
    await ctx.response.send_message(embed=simple_embed('Typing ...'))
    response = g4f.ChatCompletion.create(
        model=g4f.models.default,
        provider=g4f.Provider.GptGo,
        messages=[{"role": "user", "content": "I want you to act as an IT Expert called Chris. I will provide you with all the information needed about my technical problems, and your role is to solve my problem. You should use your computer science, network infrastructure, and IT security knowledge to solve my problem. Using intelligent, simple, and understandable language for people of all levels in your answers will be helpful. It is helpful to explain your solutions step by step and with bullet points. Try to avoid too many technical details, but use them when necessary. I want you to reply with the solution, not write any explanations."},
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
        provider=g4f.Provider.GptGo,
        messages=[{"role": "user", "content": "I want you to act as a drunk person called Bernd. You will only answer like a very drunk person texting and nothing else. Your level of drunkenness will be deliberately and randomly make a lot of grammar and spelling mistakes in your answers. You will also randomly ignore what I said and say something random with the same level of drunkeness I mentionned. Do not write explanations on replies."},
                  {"role": "user", "content": f"{prompt}"}],
        stream=False,
    )
    full_response = ''.join(response)

    await ctx.edit_original_response(embed=simple_embed(f'{prompt[:255]}', full_response))



bot.run(str(os.getenv('Token')))