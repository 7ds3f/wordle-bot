import discord
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
    Displays the statistics for a Player.
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )

    # the player whose stats are to be displayed
    player = None
    # the message to contain the stats embed
    message = None
    # list of embeds for each gamemode
    embeds = list()
    
    # define stat page buttons
    class Buttons(discord.ui.View):
        def __init__(self, *, timeout=180):
            super().__init__(timeout=timeout)
            self.current_embed = 0
        @discord.ui.button(label="<",style=discord.ButtonStyle.gray)
        async def left_button(self,interaction:discord.Interaction,button:discord.ui.Button):
            self.current_embed = await get_next_index(button, self.current_embed, len(embeds))
            await message.edit(embed=embeds[self.current_embed])
            await interaction.response.defer()
        @discord.ui.button(label=">",style=discord.ButtonStyle.gray)
        async def right_button(self,interaction:discord.Interaction,button:discord.ui.Button):
            self.current_embed = await get_next_index(button, self.current_embed, len(embeds))
            await message.edit(embed=embeds[self.current_embed])
            await interaction.response.defer()

    # display stats for caller
    if not user:
        # check if stats exist for caller
        if interaction.user.name not in PLAYERS:
            new_player = Player(interaction.user)
            new_player.room = await room.search_room(interaction.guild, interaction.user)
            PLAYERS[interaction.user.name] = new_player
        player = PLAYERS[interaction.user.name]
    # display stats for other specified user
    else:
        if user.name not in PLAYERS:
            new_player = Player(user)
            new_player.room = await room.search_room(interaction.guild, user)
            PLAYERS[user.name] = new_player
        player = PLAYERS[user.name]

    # build stats embeds
    embeds = [build_stats_embed(interaction, player, gamemode) for gamemode in player.stats["gamemodes"]]

    # send the stats embed
    if interaction.response.is_done():
        message = await interaction.followup.send(
            embed = embeds[0],
            ephemeral = True,
            view = Buttons()
        )
    else:
        message = await interaction.response.send_message(
            embed = embeds[0],
            ephemeral = True,
            view = Buttons()
        )

async def get_next_index(button: discord.ui.Button, index: int, num_stats: int) -> int:
    """
    Returns the next valid index given the left or right button, current index, and 
    number of available embeds.

    Returns:
        Returns a valid index.
    """
    if button.label == ">":
        return (index + 1) % num_stats
    elif button.label == "<":
        return (index - 1) % num_stats
    else:
        return index

def build_stats_embed(interaction: discord.Interaction, player: Player, gamemode: str) -> discord.Embed:
    """
    Builds a statistics embed for one gamemode in a Player's statistics dictionary.

    Returns:
        Returns a Discord Embed.
    """
    gamemode_stats = player.stats["gamemodes"][gamemode]
    total_games_completed = gamemode_stats["wins"] + gamemode_stats["losses"]
    if total_games_completed == 0:
        win_rate = 0.00
    else:
        win_rate = (gamemode_stats['wins'] / total_games_completed) * 100

    embed = discord.Embed(
        title = gamemode + " Wordle Statistics",
        color = discord.Color.greyple(),
        description = f"***{total_games_completed} Game Completed***" if total_games_completed == 1 else f"***{total_games_completed} Games Completed***"
    )
    embed.set_author(
        name = player.user.display_name,
        icon_url = player.user.avatar.url
    )
    embed.set_thumbnail(url=interaction.client.user.avatar.url)

    embed.add_field(
        name = "",
        value = f"**Win Rate**: {win_rate:.2f}%",
        inline = False
    )
    for stat in gamemode_stats:
        stat_name = stat
        stat_value = gamemode_stats[stat]

        stat_name = " ".join(stat_name.split('_')).title()

        if stat == "fastest_guess":
            if stat_value < 0:
                stat_value = "None"
            else:
                stat_value = f"{stat_value:.2f} seconds"
        
        embed.add_field(
            name = f"{stat_name}",
            value = f"{stat_value}",
            inline = True
        )

    return embed