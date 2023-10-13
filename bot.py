import sys
import discord
from discord.ext import commands
sys.path.append("gamemodes")
import standard_wordle
#import responses

'''
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
'''

# start the bot
def run_discord_bot():
    TOKEN = "MTE1NjYwMDYzNjU0NTE3OTY3OQ.G9AnaM.VdVSNB_1w1h2Lwq-u3Dam4wI2HsX31UzLtaHEA"
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    users = set()

    #TODO: maybe use text formatting instead of custom emojis?
    gray_letters_dict = {
        "a": "<:a_gray:1162435739192148038>",
        "b": "<:b_gray:1162437701723750574>",
        "c": "<:c_gray:1162437702990446744>",
        "d": "<:d_gray:1162437706807267390>",
        "e": "<:e_gray:1162437709172846615>",
        "f": "<:f_gray:1162437711685226626>",
        "g": "<:g_gray:1162437714201808896>",
        "h": "<:h_gray:1162437716240240660>",
        "i": "<:i_gray:1162437718345777244>",
        "j": "<:j_gray:1162437719461482687>",
        "k": "<:k_gray:1162437720539402240>",
        "l": "<:l_gray:1162437721499910376>",
        "m": "<:m_gray:1162437723223773286>",
        "n": "<:n_gray:1162437726533058570>",
        "o": "<:o_gray:1162437867491053689>",
        "p": "<:p_gray:1162437901334876250>",
        "q": "<:q_gray:1162437730114998312>",
        "r": "<:r_gray:1162437939083624548>",
        "s": "<:s_gray:1162437734636470464>",
        "t": "<:t_gray:1162438000190427277>",
        "u": "<:u_gray:1162437737371144322>",
        "v": "<:v_gray:1162438118142644294>",
        "w": "<:w_gray:1162438154549219328>",
        "x": "<:x_gray:1162437740596580482>",
        "y": "<:y_gray:1162438311814631492>",
        "z": "<:z_gray:1162438313370730546>"
    }
    yellow_green_letters_dict = {
        "a": "<:a_yellow:1162452541783691456>",
        "b": "<:b_yellow:1162452544702914580>",
        "c": "<:c_yellow:1162452547391459538>",
        "d": "",
        "e": "",
        "f": "",
        "g": "",
        "h": "",
        "i": "",
        "j": "",
        "k": "",
        "l": "",
        "m": "",
        "n": "",
        "o": "",
        "p": "",
        "q": "",
        "r": "",
        "s": "",
        "t": "",
        "u": "",
        "v": "",
        "w": "",
        "x": "",
        "y": "",
        "z": "",
        "A": "",
        "B": "",
        "C": "",
        "D": "",
        "E": "",
        "F": "",
        "G": "",
        "H": "",
        "I": "",
        "J": "",
        "K": "",
        "L": "",
        "M": "",
        "N": "",
        "O": "",
        "P": "",
        "Q": "",
        "R": "",
        "S": "",
        "T": "",
        "U": "",
        "V": "",
        "W": "",
        "X": "",
        "Y": "",
        "Z": ""
    }
    
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
                else:
                    users.add(interaction.user)
                    await standard_wordle.run(ctx, interaction, users)
            @discord.ui.button(label="Daily Wordle",style=discord.ButtonStyle.primary)
            async def daily_wordle_button(self,interaction:discord.Interaction,button:discord.ui.Button):
                await interaction.response.edit_message(content=f"Selected Daily Wordle")
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
        else:   
            users.add(ctx.author)
            await standard_wordle.run(ctx, None, users)
    
    # !q (quit) command handler
    @bot.command(name="q")
    async def _q(ctx):
        return
    
    # !greet command handler
    # print custom emoji example
    @bot.command(name="greet")
    async def _greet(ctx):
        await ctx.send(f"{gray_letters_dict['h']} {gray_letters_dict['i']}")

    '''
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username}: {user_message} ({channel})')

        if user_message.startswith("?"):
            user_message = user_message[1:]
            await send_message(message, user_message, True)
        else:
            await send_message(message, user_message, False)
    '''

    bot.run(TOKEN)
