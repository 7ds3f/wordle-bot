import discord
import graphics
import json

from ..bot import bot

@bot.tree.command(
    name = 'leaderboard',
    description = 'Displays the leaderboard of this server'
)
async def leaderboard(
    interaction: discord.Interaction,
    gamemode: str = None
) -> None:
    # TODO: Add guild leaderboard support
    """
    Displays the global leaderboard
    """
    # Prevents the bot from throwing an error for taking too long to send a response
    await interaction.response.defer(
        ephemeral = True,
        thinking = True
    )
    # the dictionary representing the current leaderboard json file
    # TODO: create a config for leaderboards and remove this hardcoded path
    with open("src/assets/leaderboards/global_leaderboard.json", 'r') as file:
        leaderboard = json.load(file)
    # the message to contain the stats embed
    message = None
    # list of embeds for each gamemode
    embeds = list()

    # define leaderboard page buttons
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
    
    # build stats embeds
    embeds = [build_leaderboard_embed(interaction, leaderboard, gamemode, stat) for stat in leaderboard["gamemodes"][gamemode]]

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

async def get_next_index(button: discord.ui.Button, index: int, num_gamemodes: int) -> int:
    """
    Returns the next valid index given the left or right button, current index, and 
    number of available gamemodes.

    Returns:
        Returns a valid index.
    """
    if button.label == ">":
        return (index + 1) % num_gamemodes
    elif button.label == "<":
        return (index - 1) % num_gamemodes
    else:
        return index

def build_leaderboard_embed(interaction: discord.Interaction, leaderboard: dict(), gamemode: str, stat: str) -> discord.Embed:
    """
    Builds a leaderboard embed for one gamemode in the leaderboard dictionary.

    Returns:
        Returns a Discord Embed.
    """
    stat_name = " ".join(stat.split('_')).title()

    embed = discord.Embed(
            title = gamemode + " Wordle Leaderboard",
            description=f"***{stat_name}***",
            color = discord.Color.orange()
    )
    embed.set_author(
        name = interaction.user.display_name,
        icon_url = interaction.user.avatar.url
    )
    #embed.set_thumbnail(url=interaction.client.user.avatar.url)
    embed.set_footer(text="Global Leaderboard")

    stat_players = leaderboard["gamemodes"][gamemode][stat]
    player_idx = 0
    for player in stat_players:

        if stat == "fastest_guess":
            pass
        
        if player_idx == 0:
            embed.add_field(
                name = "",
                value = f"**{player_idx + 1}. {player} - {stat_players[player]}**",
                inline = False
            )
        else:
            embed.add_field(
                name = "",
                value = f"**{player_idx + 1}.** {player} - {stat_players[player]}",
                inline = True
            )
        
        player_idx += 1

    return embed