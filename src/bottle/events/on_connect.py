import log
from discord import Game
from ..bot import bot

@bot.event
async def on_connect() -> None:
    log.bottle.info(f"{bot.user.name} is connecting")
    await bot.change_presence(activity=Game('Wordle'))
    log.bottle.info(f"Changed bot's activity to playing Wordle")
