import discord
import graphics
import room

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'myroom',
    description = 'Displays your room'
)
async def myroom(interaction: discord.Interaction) -> None:
    """
    Displays the user's room information when executing the slash command: /myroom.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )
    user = interaction.user
    guild = interaction.guild
    updated = await update_players(user=user, guild=guild)
    player = PLAYERS[user.name]
    
    # If the user has been updated, then the information they hold will always be true.
    # If the user hasn't been updated, then the user's information might be outdated.
    #   If the user's information is outdated, then we change it in real-time.
    #   Otherwise, create the game room for the user.
    if updated:
        if player.room:
            await __display_room(interaction, player)
        else:
            await __room_does_not_exist(interaction)
        return
    
    player.room = await room.search_room(player=user, guild=guild)
    if player.room:
        await __display_room(interaction, player)
    else:
        await __room_does_not_exist(interaction)
            
async def __display_room(
    interaction: discord.Interaction,
    player: Player
) -> None:
    await graphics.display_msg_embed(
        obj = interaction,
        title = player.room.name,
        message = f'Access your gaming room here: [{player.room.mention}]',
        color = discord.Color.blurple()
    )

async def __room_does_not_exist(interaction: discord.Interaction) -> None:
    await graphics.display_msg_embed(
        obj = interaction,
        title = 'Your room does not exist',
        message = f'Type /createroom or start a game to create your room',
        color = discord.Color.blurple()
    )
