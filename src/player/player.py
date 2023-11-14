import discord
import games
import room

class Player:
    """
    A Player is a discord member or user. The difference between a member and user is that
    a member belongs to a guild. A user is their general account that is not associated
    with a guild.
    
    Players have records of all games they have played. For every game they play, they
    accumulate points and scores. These are their statistics, which can be seen by any
    other player.
    """
    def __init__(self, user: discord.Member | discord.User) -> None:
        """
        Constructs a player of the discord member or user.
        """
        self.user = user
        'The discord member or user.'
        self.room: discord.Thread | None = None
        'The gaming room of a player.'
        self.in_game: games.Game | None = None
        'The game the player is in.'
        
PLAYERS: dict[str, Player] = dict()
'The list of all the players who has interacted with the bot or was detected by the bot.'

async def update_players(interaction: discord.Interaction) -> bool:
    """
    Updates the list of players.

    Returns:
        Returns true if the players list has been updated.
    """
    user = interaction.user
    if not user or user.name in PLAYERS:
        return False
    
    player = Player(user)
    player.room = await room.search_room(interaction.guild, user)
    PLAYERS[user.name] = player
    return True