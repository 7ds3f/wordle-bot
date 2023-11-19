import discord
import games
import json
import os
import room
import shutil

from typing import Any
from .playerconfig import *

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
        self.stats_file = os.path.join(Config.path(), user.name + ".stats.json")
        'The path to this Player\'s statistics json file'
        self.stats = Player.get_statistics(user, self.stats_file)
        'A dictionary of all Player statistics in the Player\'s stats json file'

    def get_statistics(
        user: discord.Member | discord.User,
        filename: str | None = None
    ) -> Any:
        if filename is None or not os.path.isfile(filename) or not os.access(filename, os.R_OK):
            try:
                template = cfg.get_target_file(path=Config.path(), file=Config.template())
                shutil.copy(template, filename)
            except:
                print(f'Failed to create new statistics file for {user.name}')
                return
        
        print(f'Statistics for Player {user.name} loaded successfully!')
        with open(filename, 'r') as file:
            return json.load(file)
        
    def update_fastest_guess(self, gamemode: str, time: float) -> None:
        stats = self.stats['gamemodes'][gamemode]
        fastest_guess = stats['fastest_guess']
        stats['fastest_guess'] = time if fastest_guess == -1 else min(fastest_guess, time)

    def update_player_file(self) -> None:
        with open(self.stats_file, 'w') as file:
            json.dump(self.stats, file, indent=4)

PLAYERS: dict[str, Player] = dict()
'The list of all the players who has interacted with the bot or was detected by the bot.'

async def update_players(
    *,
    user: discord.Member | discord.User,
    guild: discord.Guild
) -> bool:
    """
    Updates the list of players.

    Returns:
        Returns true if the players list has been updated.
    """
    if not user or user.name in PLAYERS:
        return False
    
    player = Player(user)
    player.room = await room.search_room(player=user, guild=guild)
    PLAYERS[user.name] = player
    return True