import discord

from ..bot import bot

@bot.tree.command(
    name = 'help',
    description = 'Displays available commands'
)
async def help(
    interaction: discord.Interaction,
    user: discord.Member | discord.User = None
) -> None:
    embed = discord.Embed(
        title = 'Help',
        description = 'List of all commands',
        color = discord.Color.blurple()
    )
    embed.set_thumbnail(url=bot.user.avatar.url)
    
    for slash_cmd in bot.tree.walk_commands():
        embed.add_field(
            name = f'/{slash_cmd.name}',
            value = slash_cmd.description if slash_cmd.description else slash_cmd.name,
            inline = False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)