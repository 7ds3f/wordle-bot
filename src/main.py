import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from gamemodes.standard import Standard
from gamemodes.daily import Daily
from gamemodes.feudle import Feudle
from users import User

load_dotenv()

COMMAND_PREFIX = "!"
'The command prefix the bot will use.'
TOKEN = os.getenv("DISCORD_TOKEN")
'The token of the discord bot.'
USERS = dict()
'All the users who has interacted with the bot.'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is running!')
    await bot.change_presence(activity=discord.Game(name="Wordle"))

@bot.command(name="standard", aliases=["sw"], brief="Start a standard Wordle game", description="Start a standard Wordle game")
async def standard(ctx):
    if ctx.author.name not in USERS:
        USERS.update({ctx.author.name : User(ctx.author)})

    if USERS[ctx.author.name].in_game:
        print(f'[WARNING] {ctx.author.name} tried to start a duplicate Wordle game instance')
        # await warning embed
    else:
        standard = Standard(USERS[ctx.author.name])
        await standard.run(ctx, None)

@bot.command(name="daily", aliases=["dw"], brief="Start the daily Wordle challenge", description="Start the daily Wordle challenge")
async def daily(ctx):
    if ctx.author.name not in USERS:
        USERS.update({ctx.author.name : User(ctx.author)})

    if USERS[ctx.author.name].in_game:
        print(f'[WARNING] {ctx.author.name} tried to start a duplicate Wordle game instance')
        # await warning embed
    else:
        daily = Daily(USERS[ctx.author.name])
        await daily.run(ctx, None)

@bot.command(name="feudle", aliases=["fw"], brief="Start a Feudle game", description="Start a Feudle game")
async def feudle(ctx):
    if ctx.author.name not in USERS:
        USERS.update({ctx.author.name : User(ctx.author)})

    if USERS[ctx.author.name].in_game:
        print(f'[WARNING] {ctx.author.name} tried to start a duplicate Wordle game instance')
        # await warning embed
    else:
        feudle = Feudle(USERS[ctx.author.name])
        await feudle.run(ctx, None)

bot.run(TOKEN)
