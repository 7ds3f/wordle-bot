import log
import sys
from ..bot import bot

@bot.event
async def on_error(event: str, *args, **kwargs):
    exc = sys.exc_info()
    log.bottle.error(f"Uncaught exception in event {event}", exc_info=exc)
    