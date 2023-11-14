import discord

from ..bot import bot

@bot.tree.command(
    name = 'leaderboard',
    description = 'Displays the leaderboard of this server'
)
async def leaderboard(interaction: discord.Interaction) -> None:
    pass