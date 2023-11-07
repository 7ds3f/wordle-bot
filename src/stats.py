import discord

from users import User

async def display_statistics(interaction:discord.Interaction, user:User):
    """
    Displays a user's statistics.
    """
    embed=discord.Embed(
        title="User Statistics",
        color=discord.Color.greyple()
    )
    embed.set_author(
        name = user.user.display_name,
        icon_url = user.user.avatar.url
    )

    embed.add_field(name="", value="Game Wins: " + str(user.wins), inline=False)
    embed.add_field(name="", value="Game Losses: " + str(user.losses), inline=False)
    embed.add_field(name="", value="Game Forfeits: " + str(user.forfeits), inline=False)
    embed.add_field(name="", value="Gray Tiles: " + str(user.grays_generated), inline=False)
    embed.add_field(name="", value="Yellow Tiles: " + str(user.yellows_generated), inline=False)
    embed.add_field(name="", value="Green Tiles: " + str(user.greens_generated), inline=False)
    
    if user.wins == 0:
        embed.add_field(name="", value=f"Fastest Guess: N/A", inline=False)
    elif user.standard_fastest_guess/60 < 1:
        embed.add_field(name="", value=f"Fastest Guess: {user.standard_fastest_guess/360:.2f} second(s)", inline=False)
    else:
        embed.add_field(name="", value=f"Fastest Guess: {user.standard_fastest_guess/60:.2f} minute(s)", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)
