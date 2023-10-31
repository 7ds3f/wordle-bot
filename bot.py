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
    # load token from .env
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    # set bot intents/permissions
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # set of CURRENT bot users
    # contains users which are actively playing any type of Wordle game
    current_users = set()

    # set of ALL bot users
    # contains all users who ever interacted with the bot
    all_users = set()
    
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
    
    # !ng command handler
    @bot.command(name="ng", aliases=["newgame"], brief="Display the Wordle gamemode menu", description="Display the Wordle gamemode menu")
    async def _newgame(ctx):
        # class for gamemode buttons
        class GamemodeSelectionButtons(discord.ui.View):
            def __init__(self, *, timeout=180):
                super().__init__(timeout=timeout)
            
            # Standard Wordle button
            @discord.ui.button(label="Standard Wordle",style=discord.ButtonStyle.primary)
            async def standard_wordle_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.edit_message(content=f"Selected Standard Wordle")
                # check if user is already in an active Wordle game
                if interaction.user in current_users:
                    print(f"[WARN] {interaction.user} tried to start a duplicate Wordle game instance...")
                    await send_in_game_warn_embed(ctx, interaction.user)
                else:
                    current_users.add(interaction.user)
                    await standard_wordle.run(ctx, interaction, current_users)
            
            # Daily Wordle button
            @discord.ui.button(label="Daily Wordle",style=discord.ButtonStyle.primary)
            async def daily_wordle_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.edit_message(content=f"Selected Daily Wordle")
                # check if user is already in an active Wordle game
                if interaction.user in current_users:
                    print(f"[WARN] {interaction.user} tried to start a duplicate Wordle game instance...")
                    await send_in_game_warn_embed(ctx, interaction.user)
                else:
                    current_users.add(interaction.user)
                    await daily_wordle.run(ctx, interaction, current_users)
            
            # Feudle Wordle button
            @discord.ui.button(label="Feudle",style=discord.ButtonStyle.primary)
            async def feudle_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.edit_message(content=f"Selected Feudle")

            # Multiplayer Wordle button
            @discord.ui.button(label="Multiplayer Wordle",style=discord.ButtonStyle.primary)
            async def multiplayer_wordle_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.edit_message(content=f"Selected Multiplayer Wordle")
        
        await ctx.send(
            "Select a gamemode:",view=GamemodeSelectionButtons()
        )
    
    # !sw (standard wordle) command handler
    @bot.command(name="sw", aliases=["standard", "standardwordle"], brief="Start a Standard Wordle game", description="Start a Standard Wordle game")
    async def _sw(ctx):
        if ctx.author in current_users:
            print(f"[WARN] {ctx.author} tried to start a duplicate Wordle game instance...")
            await send_in_game_warn_embed(ctx, ctx.author)
        else:   
            current_users.add(ctx.author)
            await standard_wordle.run(ctx, None, current_users)

    # !dw (daily wordle) command handler
    @bot.command(name="dw", aliases=["daily", "dailywordle"], brief="Start a Daily Wordle game", description="Start a Daily Wordle game")
    async def _dw(ctx):
        if ctx.author in current_users:
            print(f"[WARN] {ctx.author} tried to start a duplicate Wordle game instance...")
            await send_in_game_warn_embed(ctx, ctx.author)
        else:
            current_users.add(ctx.author)
            await daily_wordle.run(ctx, None, current_users)
    
    # !q (quit) command handler
    @bot.command(name="q", aliases=["quit"], brief="Quit your current Wordle game", description="Quit your current Wordle game")
    async def _q(ctx):
        return
    
    # !greet command handler
    # print custom emoji example with embed
    @bot.command(name="greet", aliases=["info", "about"], brief="Display BOTTLE's info", description="Display BOTTLE's info")
    async def _greet(ctx):
        embed = discord.Embed(
            title="Hello!",
            description="Thanks for using BOTTLE!",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Authors:", value="EggieVAL, CasterNinja, LucaVits, SoumayahIlias, timcuber37, and 7ds3f", inline=False)
        await ctx.send(embed=embed)

    bot.run(TOKEN)
