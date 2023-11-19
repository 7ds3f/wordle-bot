import discord

class ArrowMenuNavigation(discord.ui.View):
    def __init__(
        self,
        *,
        menus: list[discord.Embed],
        timeout: float = 180
    ) -> None:
        super().__init__(timeout=timeout)
        self.menus = menus
        self.current_value: int = 0

    @discord.ui.button(
        label = '<',
        style = discord.ButtonStyle.gray
    )
    async def navigate_left(
        self,
        interaction: discord.Interaction,
        _: discord.ui.Button
    ) -> None:
        self.current_value = (self.current_value - 1) % len(self.menus)
        await interaction.response.edit_message(embed=self.menus[self.current_value])

    @discord.ui.button(
        label = '>',
        style = discord.ButtonStyle.gray
    )
    async def navigate_right(
        self,
        interaction: discord.Interaction,
        _: discord.ui.Button
    ) -> None:
        self.current_value = (self.current_value + 1) % len(self.menus)
        await interaction.response.edit_message(embed=self.menus[self.current_value])
