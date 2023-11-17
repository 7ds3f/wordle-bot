import discord
import games
import room
import json
import os
import shutil

from ._config import *

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
        player_config = default_config()
        'The default configuration for a Player'
        self.user = user
        'The discord member or user.'
        self.room: discord.Thread | None = None
        'The gaming room of a player.'
        self.in_game: games.Game | None = None
        'The game the player is in.'
        self.path_to_stats = os.path.join(player_config.get('StatisticsFolder'), user.name + "_stats.json")
        'The path to this Player\'s statistics json file'
        self.stats = None
        'A dictionary of all Player statistics in the Player\'s stats json file'

        # locate PLayer stats json
        # if Player stats file exists + is accessible
        if os.path.isfile(self.path_to_stats) and os.access(self.path_to_stats, os.R_OK):
            print(f"Statistics for Player {self.user.name} loaded successfully!")
            with open(self.path_to_stats, 'r') as file:
                    self.stats = json.load(file)
        # if Player stats file does not exist
        else:
            print(f"Statistics missing for Player {self.user.name}. Creating new file...")
            # create a path for new statistics json
            new_stats_path = os.path.join(player_config.get('StatisticsFolder'), self.user.name + "_stats.json")
            # try to copy blank stats template to new path and set player stats member variable
            try:
                shutil.copy(player_config.get("StatisticsTemplate"), new_stats_path)
                with open(self.path_to_stats, 'r') as file:
                    self.stats = json.load(file)
                print(f"Successfully created new statistics json for Player {self.user.name}!")
            except Exception as e:
                print(f"Failed to create new statistics json for Player {self.user.name}: {e}")
        

    def update_fastest_guess(self, gamemode: str, time: float):
        if self.stats["gamemodes"][gamemode]["fastest_guess"] < 0 or time < self.stats["gamemodes"][gamemode]["fastest_guess"]:
            self.stats["gamemodes"][gamemode]["fastest_guess"] = time

    def rewrite_player_json(self):
        with open(self.path_to_stats, 'w') as file:
                json.dump(self.stats, file, indent=4)

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