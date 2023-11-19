import discord
import lobby

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'createlobby',
    description = 'Creates a lobby where players can play against each other'
)
async def createlobby(
    interaction: discord.Interaction,
    private: bool = False
) -> None:
    """
    Creates a gaming lobby where players can join. This enables players to face against each other
    players in a Wordle game.

    The owner of the lobby can customize the game the players will be playing by initiating
    additional commands. For example, to change or select the gamemode, the owner of the lobby will
    type in the respective command. So, if they wanted to play Feudle, they will type /feudle after
    they created a lobby.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = False,
        thinking = True
    )
    user = interaction.user
    guild = interaction.guild
    await update_players(user=user, guild=guild)
    player = PLAYERS[user.name]
    
    await interaction.followup.send(
        embed = lobby.Lobby.build_menu(user),
        ephemeral = True,
        view = lobby.Lobby(player=player)
    )
