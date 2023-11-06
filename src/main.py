import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from gamemodes.standard import Standard
from gamemodes.daily import Daily
from gamemodes.feudle import Feudle
from stats import display_statistics
from users import User
from wordle import display_message, display_error

load_dotenv()

COMMAND_PREFIX = "!"
'The command prefix the bot will use.'
TOKEN = os.getenv("DISCORD_TOKEN")
'The token of the discord bot.'
USERS = dict()
'All the users who has interacted with the bot.'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is running!')
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="Wordle"))

@bot.tree.command(name="daily", description="Starts the daily Wordle challenge")
async def daily(interaction:discord.Interaction):
    await __update_users(interaction.user)
    if not (await __in_game(interaction)):
        channel = await __create_private_thread(interaction)
        daily = Daily(USERS[interaction.user.name], channel)
        if not interaction.response.is_done():
            await interaction.response.send_message(f"Created the daily Wordle game in {channel.mention}.", ephemeral=True)
        await daily.run(interaction)

@bot.tree.command(name="feudle", description="Starts a Feudle game")
async def feudle(interaction:discord.Interaction):
    await __update_users(interaction.user)
    if not (await __in_game(interaction)):
        channel = await __create_private_thread(interaction)
        if not interaction.response.is_done():
            await interaction.response.send_message(f"Created a Feudle game in {channel.mention}.", ephemeral=True)
        feudle = Feudle(USERS[interaction.user.name], channel)
        await feudle.run(interaction)

@bot.tree.command(name="standard", description="Starts a standard Wordle game")
async def standard(interaction:discord.Interaction):
    await __update_users(interaction.user)
    if not (await __in_game(interaction)):
        channel = await __create_private_thread(interaction)
        standard = Standard(USERS[interaction.user.name], channel)
        if not interaction.response.is_done():
            await interaction.response.send_message(f"Created a standard Wordle game in {channel.mention}.", ephemeral=True)
        await standard.run(interaction)

@bot.tree.command(name="quit", description="Quit the Wordle game you are playing (WARNING: Counts as a forfeit)")
async def quit(interaction:discord.Interaction):
    await __update_users(interaction.user)
    if USERS[interaction.user.name].in_game:
        USERS[interaction.user.name].in_game.terminate()
        await display_error(interaction, "Forfeit", "You have left the game.")
    else:
        await display_error(interaction, "You are currently not in a game.", "Type '/standard' to start one.")

@bot.tree.command(name="stats", description="Displays your statistics")
async def stats(interaction:discord.Interaction, user:discord.Member = None):
    await __update_users(interaction.user)
    if not user:
        user = interaction.user
    elif user.name not in USERS:
        await __update_users(user)
    await display_statistics(interaction, USERS[user.name])

async def __update_users(user:discord.Member) -> None:
    if user.name not in USERS:
        USERS.update({user.name : User(user)})

async def __in_game(interaction:discord.Interaction) -> bool:
    if USERS[interaction.user.name].in_game:
        await display_error(interaction, "You're already in a Wordle game.", "Use /quit to quit your game.")
        return True
    return False

async def __create_private_thread(interaction:discord.Interaction):
    channel = interaction.channel
    if isinstance(channel, discord.Thread):
        if channel.name == f"{interaction.user.display_name}'s Game":
            await display_message(interaction, "Clearing thread.", "Please wait for a moment for a new game to be created.")
            await channel.purge()
            return channel
        channel = channel.parent

    channel = await channel.create_thread(
        name = f"{interaction.user.display_name}'s Game",
        type = discord.ChannelType.private_thread
    )
    await channel.add_user(interaction.user)
    return channel

bot.run(TOKEN)
