import discord
import graphics
import room

from ..bot import bot
from player import *

@bot.tree.command(
    name = 'stats',
    description = 'Displays your statistics'
)
async def stats(
    interaction: discord.Interaction,
    user: discord.Member | discord.User = None
) -> None:
    """
    Displays the statistics for a player.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )

    user = interaction.user if user is None else user
    guild = interaction.guild
    await update_players(user=user, guild=guild)
    player = PLAYERS[user.name]

    menus = [build_stats_menu(interaction, player, gamemode) for gamemode in player.stats['gamemodes']]
    await interaction.followup.send(
        embed = menus[0],
        ephemeral = True,
        view = graphics.ArrowMenuNavigation(menus=menus)
    )

def build_stats_menu(
    interaction: discord.Interaction,
    player: Player,
    gamemode: str
) -> discord.Embed:
    """
    Builds a statistics embed for one gamemode in a Player's statistics dictionary.

    Returns:
        Returns a Discord Embed.
    """
    gamemode_stats: dict[str, int] = player.stats['gamemodes'][gamemode]
    total_games_completed = gamemode_stats['wins'] + gamemode_stats['losses']
    total_games_played = total_games_completed + gamemode_stats['forfeits']
    win_rate = None if total_games_completed == 0 else gamemode_stats['wins'] * 100 / total_games_completed

    menu = discord.Embed(
        title = f'{gamemode} Statistics',
        color = discord.Color.greyple(),
        description = f"""
                       {'***1 Game Completed****' if total_games_completed == 1 else f'***{total_games_completed} Games Completed***'}
                       {'***1 Game Played***' if total_games_played == 1 else f'***{total_games_played} Games Played***'}
                       """
    )
    menu.set_author(
        name = player.user.display_name,
        icon_url = player.user.avatar.url
    )
    menu.set_thumbnail(url=interaction.client.user.avatar.url)
    menu.add_field(
        name = '',
        value = f'**Win Rate**: None' if win_rate is None else f'**Win Rate**: {win_rate:.2f}%',
        inline = False
    )
    for stat in gamemode_stats:
        value = gamemode_stats[stat]
        name = ' '.join(stat.split('_')).title()

        if stat == 'fastest_guess':
            value = None if value < 0 else f'{value:.2f} seconds'
        
        menu.add_field(
            name = name,
            value = value,
            inline = True
        )
    return menu