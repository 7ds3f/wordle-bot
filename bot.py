import sys
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
sys.path.append("gamemodes")
import standard_wordle
import daily_wordle

# start the bot
def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    users = set()
    
    # embed for duplicate game instance warning
    async def send_in_game_warn_embed(ctx, user):
        embed=discord.Embed(
            title="You're already in a Wordle game!",
            description="Use \"!q\" to quit current game, " + user.mention + ".",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    # bot startup greeting
    @bot.event
    async def on_ready():
        print(f'{bot.user} is running!')
    
    # !newgame command handler
    @bot.command(name="newgame")
    async def _newgame(ctx):
        # container for gamemode buttons
        class GamemodeSelectionButtons(discord.ui.View):
            def __init__(self, *, timeout=180):
                super().__init__(timeout=timeout)
            @discord.ui.button(label="Standard Wordle",style=discord.ButtonStyle.primary)
            async def standard_wordle_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.edit_message(content=f"Selected Standard Wordle")
                if interaction.user in users:
                    print(f"[WARN] {interaction.user} tried to start a duplicate Wordle game instance...")
                    await send_in_game_warn_embed(ctx, interaction.user)
                else:
                    users.add(interaction.user)
                    await standard_wordle.run(ctx, interaction, users)
            @discord.ui.button(label="Daily Wordle",style=discord.ButtonStyle.primary)
            async def daily_wordle_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.edit_message(content=f"Selected Daily Wordle")
                if interaction.user in users:
                    print(f"[WARN] {interaction.user} tried to start a duplicate Wordle game instance...")
                    await send_in_game_warn_embed(ctx, interaction.user)
                else:
                    users.add(interaction.user)
                    await daily_wordle.run(ctx, interaction, users)
            @discord.ui.button(label="Feudle",style=discord.ButtonStyle.primary)
            async def feudle_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.edit_message(content=f"Selected Feudle")
            @discord.ui.button(label="Multiplayer Wordle",style=discord.ButtonStyle.primary)
            async def multiplayer_wordle_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.edit_message(content=f"Selected Multiplayer Wordle")
        
        await ctx.send(
            "Select a gamemode:",view=GamemodeSelectionButtons()
        )
    
    # !sw (standard wordle) command handler
    @bot.command(name="sw")
    async def _sw(ctx):
        if ctx.author in users:
            print(f"[WARN] {ctx.author} tried to start a duplicate Wordle game instance...")
            await send_in_game_warn_embed(ctx, ctx.author)
        else:   
            users.add(ctx.author)
            await standard_wordle.run(ctx, None, users)

    # !dw (daily wordle) command handler
    @bot.command(name="dw")
    async def _dw(ctx):
        if ctx.author in users:
            print(f"[WARN] {ctx.author} tried to start a duplicate Wordle game instance...")
            await send_in_game_warn_embed(ctx, ctx.author)
        else:
            users.add(ctx.author)
            await daily_wordle.run(ctx, None, users)
    
    # !q (quit) command handler
    @bot.command(name="q")
    async def _q(ctx):
        return
    
    # !greet command handler
    # print custom emoji example with embed
    @bot.command(name="greet")
    async def _greet(ctx):
        embed = discord.Embed(
            title="Hello!",
            description="Thanks for using BOTTLE!",
            color=discord.Color.blurple()
        )
        await ctx.send(embed=embed)

    bot.run(TOKEN)
