import log
from player import update_players_data
from ..bot import bot

@bot.event
async def on_disconnect() -> None:
    update_players_data()
    log.bottle.info(f"{bot.user.name} is disconnecting")
