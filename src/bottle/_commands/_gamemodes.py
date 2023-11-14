import discord
import games
import graphics
import room

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'standard',
    description = 'Starts a standard Wordle game'
)
async def standard(interaction: discord.Interaction) -> None:
    """
    Starts a standard Wordle game for the user who used the slash command: /standard.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )
    # Creates a room if the user does not have one
    await __create_room(interaction)
    player = PLAYERS[interaction.user.name]
    await games.Standard(player=player).run(interaction)

@bot.tree.command(
    name = 'daily',
    description = 'Starts the daily Wordle challenge'
)
async def daily(interaction: discord.Interaction) -> None:
    """
    Starts the daily Wordle challenge for the user who used the slash command: /daily.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )
    # Creates a room if the user does not have one
    await __create_room(interaction)
    player = PLAYERS[interaction.user.name]
    await games.Daily(player=player).run(interaction)

@bot.tree.command(
    name = 'feudle',
    description = 'Starts a Feudle game'
)
async def feudle(interaction: discord.Interaction) -> None:
    """
    Starts a Feudle game for the user who used the slash command: /feudle.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )
    # Creates a room if the user does not have one
    await __create_room(interaction)
    player = PLAYERS[interaction.user.name]
    await games.Feudle(player=player).run(interaction)

async def __create_room(interaction: discord.Interaction) -> None:
    updated = await update_players(interaction)
    user = interaction.user
    player = PLAYERS[user.name]
    
    if updated:
        if not player.room:
            player.room, _ = await room.create_room(interaction)
            await __created_room(interaction, player.room)
            await player.room.add_user(user)
        elif interaction.channel.name == player.room.name:
            await __clearing_room(interaction)
        else:
            await __clearing_room(interaction, player.room)
    else:
        player.room, created = await room.create_room(interaction)
        if created:
            await __created_room(interaction, player.room)
            await player.room.add_user(user)
        elif interaction.channel.name == player.room.name:
            await __clearing_room(interaction)
        else:
            await __clearing_room(interaction, player.room)

async def __created_room(
    interaction: discord.Interaction,
    room: discord.Thread
) -> None:
    await graphics.display_msg_embed(
        obj = interaction,
        title = 'Created your personalize game room',
        message = f'Access your room here: [{room.mention}]',
        color = discord.Color.blurple()
    )
    
async def __clearing_room(
    interaction: discord.Interaction,
    room: discord.Thread | None = None
) -> None:
    if room:
        await room.edit(archived=False)
        try: await room.purge()
        except: pass
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'Cleared your game room',
            message = f'Visit your room [{room.mention}] to play',
            color = discord.Color.blurple()
        )
    else:
        await interaction.channel.edit(archived=False)
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'Clearing your room',
            message = 'Please wait for a moment for a new game to be created',
            color = discord.Color.blurple()
        )
        try: await interaction.channel.purge()
        except: pass