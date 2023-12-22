import discord
import os
import logging
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger('discord')
logger.name = 'application'

EMBED_COLOR=0xFEC200

def simple_embed(title, text=''):
    embed = discord.Embed(title=title,description=text, color=EMBED_COLOR)
    return embed


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
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

bot.run(str(os.getenv('Token')))