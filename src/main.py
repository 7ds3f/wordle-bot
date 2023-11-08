import discord
import os
import random
import time

from discord.ext import commands
from dotenv import load_dotenv
from gamemodes.standard import Standard
from gamemodes.daily import Daily
from gamemodes.feudle import Feudle
from stats import display_statistics
from users import User
from wordle import display_message, display_error

def load_word_files(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.readlines()
        file.close()
        return words
    
standard_words = load_word_files("standard_words.txt")
feudle_words = load_word_files("feudle_words.txt")
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
'The token of the discord bot.'
USERS = dict()
'All the users who has interacted with the bot.'

def __get_prefix(bot, message) -> str:
    return message.content + '!'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=__get_prefix, intents=intents)

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
        seed = time.strftime("%d/%m/%Y")
        rand = random.Random(seed)
        daily = Daily(USERS[interaction.user.name], channel, rand.choice(standard_words).strip())
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
        feudle = Feudle(USERS[interaction.user.name], channel, random.choice(feudle_words).strip())
        await feudle.run(interaction)

@bot.tree.command(name="standard", description="Starts a standard Wordle game")
async def standard(interaction:discord.Interaction):
    await __update_users(interaction.user)
    if not (await __in_game(interaction)):
        channel = await __create_private_thread(interaction)
        standard = Standard(USERS[interaction.user.name], channel, random.choice(standard_words).strip())
        if not interaction.response.is_done():
            await interaction.response.send_message(f"Created a standard Wordle game in {channel.mention}.", ephemeral=True)
        await standard.run(interaction)

@bot.tree.command(name="quit", description="Quit the Wordle game you are playing (WARNING: Counts as a forfeit)")
async def quit(interaction:discord.Interaction):
    await __update_users(interaction.user)
    if USERS[interaction.user.name].in_game:
        USERS[interaction.user.name].in_game.terminate()
        print(interaction.user.name, 'has forfeited their game')
        await display_error(interaction, "Forfeit", "You have left the game, This thread will be deleted in 5 seconds")
        time.sleep(5)
        await (await __search_for_thread(interaction, f"{interaction.user.name}'s Game".capitalize())).delete()
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

@bot.tree.command(name="help", description="displays available commands")
async def help(interaction:discord.Interaction):
    embed = discord.Embed(
            title="Commands",
            description="Bottle has 3 gamemode commands, a quit command, and a stats command",
            color=discord.Color.blurple()
        )
    embed.add_field(name="Standard:", value="Starts a game of Wordle with a random hidden word", inline=False)
    embed.add_field(name="Daily:", value="Starts a game of Wordle with today's hidden word", inline=False)
    embed.add_field(name="Feudle:", value="Starts a game of Feudle where you must guess the missing word in a sentence", inline=False)
    embed.add_field(name="Quit:", value="Ends whatever game you are playing and deletes the thread, counts as a forfeit", inline=False)
    embed.add_field(name="Stats:", value="Displays either your stats or the stats of the person mentioned", inline=False)
    await interaction.response.send_message(embed=embed)

async def __update_users(user:discord.Member) -> None:
    if user.name not in USERS:
        USERS.update({user.name : User(user)})

async def __in_game(interaction:discord.Interaction) -> bool:
    if USERS[interaction.user.name].in_game:
        await display_error(interaction, "You're already in a Wordle game.", "Use /quit to quit your game.")
        return True
    return False

async def __create_private_thread(interaction:discord.Interaction):
    thread_name = f"{interaction.user.name}'s Game".capitalize()
    if interaction.channel.name == thread_name:
        await display_message(interaction, "Clearing thread.", "Please wait for a moment for a new game to be created.")
        await interaction.channel.purge()
        return interaction.channel
    
    thread = await __search_for_thread(interaction, thread_name)
    if not thread:
        channel = interaction.channel.parent if isinstance(interaction.channel, discord.Thread) else interaction.channel
        thread = await channel.create_thread(
            name = thread_name,
            type = discord.ChannelType.private_thread
        )
        thread.invitable = False
        await thread.add_user(interaction.user)
    else:
        await display_message(interaction, f"Clearing your thread, {thread.mention}.", "Please wait for a moment for a new game to be created.")
        await thread.purge()
    return thread

async def __search_for_thread(interaction:discord.Interaction, thread_name:str):
    guild = interaction.guild
    for thread in guild.threads:
        if thread.name == thread_name:
            return thread

bot.run(TOKEN)
