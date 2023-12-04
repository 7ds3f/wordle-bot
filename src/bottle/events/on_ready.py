import log
from ..bot import bot

@bot.event
async def on_ready() -> None:
    log.bottle.info(f'{bot.user.name} is running!')
    await bot.tree.sync()
    log.bottle.info(f'Finished syncing')