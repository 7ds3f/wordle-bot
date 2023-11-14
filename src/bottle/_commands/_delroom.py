import discord
import graphics
import room

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'delroom',
    description = 'Deletes your personalized gaming room'
)
async def delroom(interaction: discord.Interaction) -> None:
    """
    Deletes a personalized gaming room for the user who used the slash command: /delroom.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )
    updated = await update_players(interaction)
    user = interaction.user
    player = PLAYERS[user.name]
    
    # If the user has been updated, then the information they hold will always be true.
    # If the user hasn't been updated, then the user's information might be outdated.
    #   If the user's information is outdated, then we change it in real-time.
    #   Otherwise, delete the user's room.
    if updated:
        if player.room:
            await player.room.delete()
            await __deleted_room(interaction)
            player.room = None
        else:
            await __room_does_not_exist(interaction)
        return
    
    player.room = await room.search_room(interaction.guild, user)
    if not player.room:
        await __room_does_not_exist(interaction)
        player.in_game = None
    elif player.in_game:
        await __in_game(interaction)
    else:
        await player.room.delete()
        await __deleted_room(interaction)
        player.room = None
            
async def __deleted_room(interaction: discord.Interaction) -> None:
    try:
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'Deleted your room',
            message = 'Type /createroom or start a game to create a new room',
            color = discord.Color.blurple()
        )
    except: pass
            
async def __room_does_not_exist(interaction: discord.Interaction) -> None:
    await graphics.display_msg_embed(
        obj = interaction,
        title = 'Your room does not exist',
        message = 'Type /createroom or start a game to create your room',
        color = discord.Color.red()
    )
    
async def __in_game(interaction: discord.Interaction) -> None:
    await graphics.display_msg_embed(
        obj = interaction,
        title = 'You are currently in a game',
        message = 'Type /quit to exit your game',
        color = discord.Color.red()
    )