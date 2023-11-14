import discord

from discord.ext import commands
from ._config import *

__intents = discord.Intents.default()
__intents.members = True
__intents.message_content = True

def __get_prefix(_, message: discord.Message) -> str:
    token = token_config()
    return token.get('CommandPrefix') if token.getboolean('EnableCommandPrefix') else message.content + '!'

bot = commands.Bot(
    command_prefix = __get_prefix,
    intents = __intents
)

import bottle._commands

def run() -> None:
    bot.run(TOKEN)