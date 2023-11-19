import discord

from discord.ext import commands
from .botconfig import *

__intents = discord.Intents.default()
__intents.members = True
__intents.message_content = True

def __get_prefix(_, message: discord.Message) -> str:
    return Config.command_prefix() if Config.enable_command_prefix() else message.content + '!'

bot = commands.Bot(
    command_prefix = __get_prefix,
    intents = __intents
)

import bottle.cmds

def run() -> None:
    bot.run(TOKEN)