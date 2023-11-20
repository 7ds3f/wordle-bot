import discord
import graphics
import json

from ..bot import bot

@bot.tree.command(
    name = 'leaderboard',
    description = 'Displays the global or local Wordle leaderboard'
)
async def leaderboard(
    interaction: discord.Interaction,
    gamemode: str = None,
    showoff: bool = False,
    dropdown: bool = True,
    display_global: bool = True
) -> None:
    # TODO: Add guild leaderboard support
    """
    Displays the global leaderboard
    """
    await interaction.response.defer(ephemeral=(not showoff), thinking=True)
    guild = interaction.guild

    # TODO: create a config for leaderboards and remove this hardcoded path
    with open("src/assets/leaderboards/global_leaderboard.json", 'r') as file:
        leaderboard = json.load(file)

    if not gamemode:
        await graphics.display_msg_embed(
            interaction,
            title = "Please specify a gamemode",
            description = "Ex. /leaderboard standard",
            color = discord.Color.red()
        )
        return
    else:
        gamemode = gamemode.lower().capitalize()

    if gamemode not in leaderboard["gamemodes"]:
        await graphics.display_msg_embed(
            interaction,
            title = "Gamemode does not exist",
            description = "Enter a valid gamemode",
            color = discord.Color.red()
        )
        return

    if dropdown:
        menus: dict[str, discord.Embed] = {}
        options: dict[str, str] = {}

        for stat in leaderboard["gamemodes"][gamemode]:
            formatted_stat = format_stat(stat)
            menus[formatted_stat] = build_leaderboard_embed(interaction, leaderboard, gamemode, stat, formatted_stat)
            options[formatted_stat] = f'Display {formatted_stat.lower()} statistics'

        await graphics.DropdownNavigationMenu.create_and_display(interaction=interaction, menus=menus, options=options)
    else:
        menus = [build_leaderboard_embed(interaction, leaderboard, gamemode, stat, format_stat(stat)) for stat in leaderboard["gamemodes"][gamemode]]
        await graphics.ArrowNavigationMenu.create_and_display(interaction=interaction, menus=menus)

def format_stat(stat: str, *, title: bool=True) -> str:
    """
    Capitalizes a statistic and removes underscores
    """
    result = " ".join(stat.split('_'))
    if title:
        return result.title()
    else:
        return result

def build_leaderboard_embed(interaction: discord.Interaction, leaderboard: dict(),
gamemode: str, stat: str, formatted_stat: str = None, length: int = 5) -> discord.Embed:
    """
    Builds a leaderboard embed for one gamemode in the leaderboard dictionary.

    Returns:
        Returns a Discord Embed.
    """
    if formatted_stat:
        stat_name = formatted_stat
    else:
        stat_name = stat

    embed = discord.Embed(
            title = gamemode + " Wordle Leaderboard",
            description=f"***{stat_name}***",
            color = discord.Color.orange()
    )
    embed.set_author(
        name = interaction.user.display_name,
        icon_url = interaction.user.avatar.url
    )
    embed.set_footer(text="Global Leaderboard")

    stat_players = leaderboard["gamemodes"][gamemode][stat]
    player_idx = 0
    for player in stat_players:
        if player_idx == length-1:
            break
        if player_idx == 0:
            embed.add_field(
                name = "",
                value = f"**{player_idx + 1}. {player} - {stat_players[player]:.2f} sec.**" if stat == "fastest_guess" else f"**{player_idx + 1}. {player} - {stat_players[player]}**",
                inline = False
            )
        else:
            embed.add_field(
                name = "",
                value = f"**{player_idx + 1}.** {player} - {stat_players[player]:.2f} sec." if stat == "fastest_guess" else f"**{player_idx + 1}.** {player} - {stat_players[player]}",
                inline = True
            )

        player_idx += 1

    return embed
