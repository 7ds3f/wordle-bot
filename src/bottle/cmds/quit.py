import discord
import graphics
import room

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'quit',
    description = 'Quit (forfeit) the Wordle game you are playing'
)
async def quit(interaction: discord.Interaction) -> None:
    """
    Quits the user's game when they execute the command: /quit.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )
    
    # If the user has been updated, then the information they hold will always be true.
    # If the user hasn't been updated, then the user's information might be outdated.
    #   If the user's information is outdated, then we change it in real-time.
    #   Otherwise, quit the game the user is playing.
    user = interaction.user
    guild = interaction.guild
    updated = await update_players(user=user, guild=guild)
    player = PLAYERS[user.name]
    
    if updated or not player.in_game:
        await __not_in_game(interaction)
        return
        
    player.room = await room.search_room(player=user, guild=guild)
    player.in_game.update_statistics()
    player.in_game.terminate()

    if not player.room:
        await __missing_room(interaction)
    else:
        await __quitting_game(interaction)
        await player.room.edit(archived=True)

async def __not_in_game(interaction: discord.Interaction) -> None:
    await graphics.display_msg_embed(
        obj = interaction,
        title = 'You are currently not in a game',
        message = 'Type /<gamemode> to start one',
        color = discord.Color.red()
    )
    
async def __missing_room(interaction: discord.Interaction) -> None:
    await graphics.display_msg_embed(
        obj = interaction,
        title = 'You are missing your room',
        message = 'Force quitting your game',
        color = discord.Color.red()
    )
    
async def __quitting_game(interaction: discord.Interaction) -> None:
    await graphics.display_msg_embed(
        obj = interaction,
        title = 'Forfeited',
        message = 'You have left the game',
        color = discord.Color.red()
    )