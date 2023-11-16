import discord
import graphics

from ..bot import bot
from player import *

@bot.tree.command(
    name = 'stats',
    description = 'Displays your statistics'
)
async def stats(
    interaction: discord.Interaction,
    user: discord.Member | discord.User = None
) -> None:
    """
    Displays the statistics for a Player.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )

    player = PLAYERS[user.name]

    embed = discord.Embed(
        title = "Statistics",
        color = discord.Color.greyple()
    )
    embed.set_author(
        name = player.user.display_name,
        icon_url = user.player.user.avatar.url
    )

    if interaction.response.is_done():
        await interaction.followup.send(
            embed = embed,
            ephemeral = True
        )
    else:
        await interaction.response.send_message(
            embed = embed,
            ephemeral = True
        )