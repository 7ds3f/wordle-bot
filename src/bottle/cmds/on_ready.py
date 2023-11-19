import discord

from ..bot import bot

@bot.event
async def on_ready() -> None:
    """
    The on_ready event tells Console that BOTTLE is running, and syncs with slash commands.
    
    During runtime, BOTTLE will be seen as 'playing Wordle.'
    """
    print(f'{bot.user} is running!')
    await bot.tree.sync()
    await bot.change_presence(
        activity = discord.Game('Wordle')
    )