import discord
import graphics
import room

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'createroom',
    description = 'Creates your personalized gaming room'
)
async def createroom(
    interaction: discord.Interaction,
    private: bool | None = None
) -> None:
    """
    Creates a personalized gaming room for the user who used the slash command: /createroom.
    
    Can create a public room by setting 'private' to True.
    Can create a private room by setting 'private' to False.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )
    user = interaction.user
    guild = interaction.guild
    channel = interaction.channel
    updated = await update_players(user=user, guild=guild)
    player = PLAYERS[user.name]
    
    # If the user has been updated, then the information they hold will always be true.
    # If the user hasn't been updated, then the user's information might be outdated.
    #   If the user's information is outdated, then we change it in real-time.
    #   Otherwise, create the game room for the user.
    if updated:
        if player.room:
            await __room_already_exists(interaction, player.room)
        else:
            player.room, _ = await room.create_room(
                player = user,
                guild = guild,
                channel = channel,
                room_type = private if private is None else (discord.ChannelType.private_thread if private else discord.ChannelType.public_thread)
            )
            await __created_room(interaction, player.room)
            await player.room.edit(archived=True)
            await player.room.add_user(user)
    else:
        player.room, created = await room.create_room(
            player = user,
            guild = guild,
            channel = channel,
            room_type = private if private is None else (discord.ChannelType.private_thread if private else discord.ChannelType.public_thread)
        )
        if created:
            await __created_room(interaction, player.room)
            await player.room.edit(archived=True)
            await player.room.add_user(user)
        else:
            await __room_already_exists(interaction, player.room)

async def __created_room(
    interaction: discord.Interaction,
    room: discord.Thread
) -> None:
    await graphics.display_msg_embed(
        obj = interaction,
        title = 'Created your personalized game room',
        message = f'Access your room here: [{room.mention}]',
        color = discord.Color.blurple()
    )

async def __room_already_exists(
    interaction: discord.Interaction,
    room: discord.Thread
) -> None:
    await graphics.display_msg_embed(
        obj = interaction,
        title = 'Your room already exists',
        message = f'Visit your gaming room here: [{room.mention}]',
        color = discord.Color.red()
    )