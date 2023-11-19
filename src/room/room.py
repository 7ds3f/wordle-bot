import discord

from .roomconfig import *

async def create_room(
    *,
    player: discord.Member | discord.User,
    guild: discord.Guild,
    channel: discord.Thread | discord.TextChannel,
    duplicate: bool = False,
    room_type: discord.ChannelType | None = None,
    invitable: bool | None = None,
    auto_archive_duration: int | None = None,
    slowmode_delay: int | None = None
) -> tuple[discord.Thread, bool]:
    """
    Attempts to create a room for the user of the interaction.

    Returns:
        The first element is the room that belongs to the player.
        The second element is whether that room was created or not.
    """
    if room_type is None:
        room_type = (discord.ChannelType.private_thread if Config.private() else discord.ChannelType.public_thread)
    if invitable is None:
        invitable = Config.invitable()
    if auto_archive_duration is None:
        auto_archive_duration = Config.auto_archive_duration()
    if slowmode_delay is None:
        slowmode_delay = Config.slowmode_delay()
    
    if not duplicate:
        room = await search_room(player=player, guild=guild)
        if room:
            return (room, False)
    
    channel = channel.parent if isinstance(channel, discord.Thread) else channel
    return (await channel.create_thread(
        name = get_room_name(player),
        type = room_type,
        invitable = invitable,
        auto_archive_duration = auto_archive_duration,
        slowmode_delay = slowmode_delay
    ), True)

async def search_room(
    *,
    player: discord.Member | discord.User,
    guild: discord.Guild
) -> discord.Thread | None:
    """
    Searches for the player's room in the given guild.
    """
    room_name = get_room_name(player)
    for room in guild.threads:
        if room.name == room_name:
            return room
        
    for channel in guild.channels:
        if not isinstance(channel, discord.TextChannel):
            continue
        async for room in channel.archived_threads(private=True):
            if room.name == room_name:
                return room
        async for room in channel.archived_threads(private=False):
            if room.name == room_name:
                return room

def get_room_name(player: discord.Member | discord.User) -> str:
    """
    Gets the name of the player's room.
    """
    return f"{player.name.capitalize()}'s Room"