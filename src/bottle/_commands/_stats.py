import discord

from ..bot import bot

@bot.tree.command(
    name = 'stats',
    description = 'Displays your statistics'
)
async def stats(
    interaction: discord.Interaction,
    user: discord.Member | discord.User = None
) -> None:
    pass