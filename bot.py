import sys
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
sys.path.append("gamemodes")
sys.path.append("player_stats")
import user
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

    # dictionary of ALL bot users
    # contains all users who ever interacted with the bot
    bot_users = dict()
    
    # embed for user stats
    async def send_user_stats_embed(ctx, user):
        embed=discord.Embed(
            title="User Statistics",
            description=user.mention,
            color=discord.Color.blurple()
        )
        embed.add_field(name="", value="Game Wins: " + str(bot_users[user].get_wins()), inline=False)
        embed.add_field(name="", value="Game Losses: " + str(bot_users[user].get_losses()), inline=False)
        embed.add_field(name="", value="Game Forfeits: " + str(bot_users[user].get_forfeits()), inline=False)
        embed.add_field(name="", value="Gray Tiles: " + str(bot_users[user].get_gray_tiles()), inline=False)
        embed.add_field(name="", value="Yellow Tiles: " + str(bot_users[user].get_yellow_tiles()), inline=False)
        embed.add_field(name="", value="Green Tiles: " + str(bot_users[user].get_green_tiles()), inline=False)
        if bot_users[user].get_wins() == 0:
            embed.add_field(name="", value=f"Fastest Guess: N/A", inline=False)
        else:
            embed.add_field(name="", value=f"Fastest Guess: {bot_users[user].get_fastest_guess()/60:.2f} minute(s)", inline=False)
        await ctx.send(embed=embed)

    # embed for new user warning
    async def send_new_user_embed(ctx, user):
        embed=discord.Embed(
            title="User Statistics",
            description="No user data. Use \"!ng\" to start a new game, " + user.mention + ".",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)

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
                # add user to the bot if the user has never used it before + start the game
                if interaction.user not in bot_users:
                    bot_users.update({interaction.user : user.User(interaction.user)})
                    bot_users[interaction.user].set_in_game(True)
                    await standard_wordle.run(ctx, interaction, bot_users)
                # check if existing user is in a game already
                else:
                    # if existing user is in a game already, send warning embed
                    if bot_users[interaction.user].is_in_game():
                        print(f"[WARN] {interaction.user} tried to start a duplicate Wordle game instance...")
                        await send_in_game_warn_embed(ctx, interaction.user)
                    # if existing user is NOT in a game already, start a new game
                    else:
                        bot_users[interaction.user].set_in_game(True)
                        await standard_wordle.run(ctx, interaction, bot_users)
            
            # Daily Wordle button
            @discord.ui.button(label="Daily Wordle",style=discord.ButtonStyle.primary)
            async def daily_wordle_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.edit_message(content=f"Selected Daily Wordle")
                # add user to the bot if the user has never used it before + start the game
                if interaction.user not in bot_users:
                    bot_users.update({interaction.user : user.User(interaction.user)})
                    bot_users[interaction.user].set_in_game(True)
                    await daily_wordle.run(ctx, interaction, bot_users)
                # check if existing user is in a game already
                else:
                    # if existing user is in a game already, send warning embed
                    if bot_users[interaction.user].is_in_game():
                        print(f"[WARN] {interaction.user} tried to start a duplicate Wordle game instance...")
                        await send_in_game_warn_embed(ctx, interaction.user)
                    # if existing user is NOT in a game already, start a new game
                    else:
                        bot_users[interaction.user].set_in_game(True)
                        await daily_wordle.run(ctx, interaction, bot_users)
            
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
        # add user to the bot if the user has never used it before + start the game
        if ctx.author not in bot_users:
            bot_users.update({ctx.author : user.User(ctx.author)})
            bot_users[ctx.author].set_in_game(True)
            await standard_wordle.run(ctx, None, bot_users)
        # check if existing user is in a game already
        else:
            # if existing user is in a game already, send warning embed
            if bot_users[ctx.author].is_in_game():
                print(f"[WARN] {ctx.author} tried to start a duplicate Wordle game instance...")
                await send_in_game_warn_embed(ctx, ctx.author)
            # if existing user is NOT in a game already, start a new game
            else:
                bot_users[ctx.author].set_in_game(True)
                await standard_wordle.run(ctx, None, bot_users)

    # !dw (daily wordle) command handler
    @bot.command(name="dw", aliases=["daily", "dailywordle"], brief="Start a Daily Wordle game", description="Start a Daily Wordle game")
    async def _dw(ctx):
        # add user to the bot if the user has never used it before + start the game
        if ctx.author not in bot_users:
            bot_users.update({ctx.author : user.User(ctx.author)})
            bot_users[ctx.author].set_in_game(True)
            await daily_wordle.run(ctx, None, bot_users)
        # check if existing user is in a game already
        else:
            # if existing user is in a game already, send warning embed
            if bot_users[ctx.author].is_in_game():
                print(f"[WARN] {ctx.author} tried to start a duplicate Wordle game instance...")
                await send_in_game_warn_embed(ctx, ctx.author)
            # if existing user is NOT in a game already, start a new game
            else:
                bot_users[ctx.author].set_in_game(True)
                await daily_wordle.run(ctx, None, bot_users)
    
    # !q (quit) command handler
    @bot.command(name="q", aliases=["quit"], brief="Quit your current Wordle game", description="Quit your current Wordle game")
    async def _q(ctx):
        return
    
    # !s (stats) command handler
    @bot.command(name="s", aliases=["stats"], brief="Display user statistics", description="Display user statistics")
    async def _s(ctx):
        if ctx.author not in bot_users:
            await send_new_user_embed(ctx, ctx.author)
        else:
            await send_user_stats_embed(ctx, ctx.author)
    
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
