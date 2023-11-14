import discord

from ._config import default_config

async def create_room(
    interaction: discord.Interaction,
    duplicate: bool = False,
    *,
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
    config = default_config()
    if room_type is None:
        room_type = (discord.ChannelType.private_thread if config.getboolean('Private')
                                                        else discord.ChannelType.public_thread)
    if invitable is None:
        invitable = config.getboolean('Invitable')
    if auto_archive_duration is None:
        auto_archive_duration = config.getint('AutoArchiveDuration')
    if slowmode_delay is None:
        slowmode_delay = config.getint('SlowmodeDelay')
    
    player = interaction.user
    if not duplicate:
        guild = interaction.guild
        room = await search_room(guild, player)
        if room:
            return (room, False)
    
    channel = interaction.channel
    channel = channel.parent if isinstance(channel, discord.Thread) else channel
    return (await channel.create_thread(
        name = get_room_name(player),
        type = room_type,
        invitable = invitable,
        auto_archive_duration = auto_archive_duration,
        slowmode_delay = slowmode_delay
    ), True)

async def search_room(
    guild: discord.Guild,
    player: discord.Member | discord.User
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