import discord

from player import *

class Lobby(discord.ui.View):
    def __init__(
        self,
        *,
        player: Player,
        timeout: float = 180
    ) -> None:
        super().__init__(timeout=timeout)
        self.players = [player]
        self.mode = 'Standard'

    def build_menu(user: discord.Member | discord.User) -> discord.Embed:
        menu = discord.Embed(
            title = f"{user.display_name.capitalize()}'s Lobby",
            color = discord.Color.greyple()
        )
        menu.set_thumbnail(url=user.avatar.url)
        menu.add_field(
            name = '',
            value = f'**Leader:** {user.name}',
            inline = True
        )
        menu.add_field(
            name = '',
            value = '**Mode:** Standard',
            inline = False
        )
        menu.add_field(
            name = 'Players',
            value = '',
            inline = False
        )
        return menu

    @discord.ui.button(
        label = 'Join',
        style = discord.ButtonStyle.green
    )
    async def join(
        self,
        interaction: discord.Interaction,
        _: discord.ui.Button
    ) -> None:
        user = interaction.user
        guild = interaction.guild
        await update_players(user=user, guild=guild)
        player = PLAYERS[user.name]

        if player in self.players:
            return
        
        self.players.append(player)
        menu = interaction.message.embeds[0]
        menu.add_field(
            name = '',
            value = f'{user.display_name} ({user.name})',
            inline = False
        )
        await interaction.response.edit_message(embed=menu)

    @discord.ui.button(
        label = 'Leave',
        style = discord.ButtonStyle.red
    )
    async def leave(
        self,
        interaction: discord.Interaction,
        _: discord.ui.Button
    ) -> None:
        user = interaction.user
        guild = interaction.guild
        await update_players(user=user, guild=guild)
        player = PLAYERS[user.name]

        if player == self.players[0]:
            return

        try:
            index = self.players.index(player)
            self.players.pop(index)
            
            menu = interaction.message.embeds[0]
            menu.remove_field(index + 2)
            await interaction.response.edit_message(embed=menu)
        except: pass
