import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from gamemodes.standard import Standard
from gamemodes.daily import Daily
from gamemodes.feudle import Feudle
from users import User
from wordle import display_error

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
        
    if not (await __in_game(ctx)):
        channel = await __create_private_thread(ctx)
        standard = Standard(USERS[ctx.author.name], channel)
        await standard.run(ctx)

@bot.command(name="daily", aliases=["dw"], brief="Start the daily Wordle challenge", description="Start the daily Wordle challenge")
async def daily(ctx):
    if ctx.author.name not in USERS:
        USERS.update({ctx.author.name : User(ctx.author)})
        
    if not (await __in_game(ctx)):
        channel = await __create_private_thread(ctx)
        daily = Daily(USERS[ctx.author.name], channel)
        await daily.run(ctx)

@bot.command(name="feudle", aliases=["fw"], brief="Start a Feudle game", description="Start a Feudle game")
async def feudle(ctx):
    if ctx.author.name not in USERS:
        USERS.update({ctx.author.name : User(ctx.author)})
        
    if not (await __in_game(ctx)):
        channel = await __create_private_thread(ctx)
        feudle = Feudle(USERS[ctx.author.name], channel)
        await feudle.run(ctx)

async def __in_game(ctx) -> bool:
    if USERS[ctx.author.name].in_game:
        print(f'[WARNING] {ctx.author.name} tried to start a duplicate Wordle game instance')
        await display_error(ctx, "You're already in a Wordle game!", "Use '!q' to quit your game.")
        return True
    return False

async def __create_private_thread(ctx):
    channel = ctx.channel
    if isinstance(channel, discord.Thread):
        if channel.name == f"{ctx.author.display_name}'s Game":
            await channel.purge()
            return channel
        channel = channel.parent
    
    channel = await channel.create_thread(
        name = f"{ctx.author.display_name}'s Game",
        type = discord.ChannelType.private_thread
    )
    await channel.add_user(ctx.author)
    return channel
    
bot.run(TOKEN)
