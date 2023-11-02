'''
Standard Wordle gamemode, interactable through Discord.
'''

import sys
import enchant
import discord
sys.path.append("gamemodes/game_utils")
import wordle
import letter
import time

class StandardWordle:
    """
    A class used to represent a Standard Wordle game. Includes Daily Wordle functionality.
    """

    def __init__(self, daily):
        """
        DESC: Constructs a Standard Wordle game.

        PARAMS:
            daily (boolean) - whether or not to use a randomly generated word
        """

        self.game_start_time = time.time()
        "The time when the game was started"
        self.game_time = None
        "Time elapsed between game start and end via a correct guess"
        self.letters = dict()
        "The states of all letters used in the current game"
        
        # build a dictionary for the alphabet for the current game
        for i in range(97, 123):
            self.letters.update({chr(i) : letter.Letter(chr(i), letter.LetterState.NONE)})

        self.daily = daily
        "If True, use daily Wordle Word. If False, generate a random word"
        self.remaining_attempts = 6
        "The number of attempts the player has left to guess the hidden word."
        self.has_guessed_word = False
        "Whether the player has guessed the hidden word."
        self.history = dict()
        "The player\'s history of guessed words for the current game"
        self.dictionary = enchant.Dict("en_US")
        "The dictionary of valid words for the current game"

        # select a random word only if Daily is False
        if daily:
            self.hidden_word = wordle.daily_word()
        else:
            self.hidden_word = wordle.random_word(self.dictionary)
        "The word the player is trying to guess."

    def is_terminated(self) -> bool:
        """
        DESC: Whether the game has been terminated.
        
        RETURNS: (bool) True if the game has been terminated; otherwise False
        """
        return self.has_guessed_word or self.remaining_attempts == 0
    
    def get_letters(self) -> dict:
        """
        DESC: Returns a dictionary of all the user's guesses and corresponding results for the current game
        
        RETURNS: (dict) all of the user's previous guesses for the current game
        """

        return self.letters

    def get_game_time(self):
        return self.game_time

    def get_history(self) -> dict:
        return self.history
    
    def get_guesses_rem(self):
        return self.remaining_attempts
    
    def get_hidden_word(self):
        return self.hidden_word

    def make_guess(self, guess:str):
        """
        Attempt to guess the hidden word.

        Args:
            guess (str): The guess the player made.

        Raises:
            InvalidGuess: Guess is too long, is too short, is not a word in the English dictionary, or
            contains special characters.

        Returns:
            (error_code, ["-", "-", "-", "-", "-"]), where:
            error_code 0 = guess is correct
            error_code 1 = guess is valid but incorrect
            error_code 2 = guess is invalid (too long)
            error_code 3 = guess is invalid (too short)
            error_code 4 = guess is invalid (contains invalid characters)
            error_code 5 = guess is invalid (not a real word)
            error_code 6 = guess is invalid (guess has been guessed already)
            -------------
            ["-", "-", "-", "-", "-"], where:
            a "-" indicates the letter is not present in the hidden_word
            a lowercase letter indicates that letter is present in the hidden_word but in the wrong place
            an uppercase letter indicates that letter is present in the hidden_word and in the right place
        """
        
        if self.remaining_attempts == 0 or self.has_guessed_word:
            return None
        
        wordle_result = wordle.wordle(guess, self.hidden_word, self.history, self.dictionary, self.letters)

        if wordle_result[0] == 0: # guess is valid and correct
            self.has_guessed_word = True
            self.__use_attempt()
            self.game_time = time.time() - self.game_start_time
        elif wordle_result[0] == 1: # guess is valid and incorrect
            self.__use_attempt()
        
        return wordle_result
    
    def __use_attempt(self):
        self.remaining_attempts -= 1

class StandardWordleResponseSender:
    """
    Class used to represent a game status Discord embed sender.
    """
    def __init__(self, ctx, gamemode):
        self.ctx = ctx
        self.gamemode = gamemode
    
    # send embed for game start
    async def send_start_embed(self, user):
        embed=discord.Embed(
            title=self.gamemode,
            color=discord.Color.blurple(),
            description="Type a guess, " + user.mention + "!"
        )
        await self.ctx.send(embed=embed)

    # send embed for ongoing game status
    async def send_game_embed(self, guessed_words, guess_obj, guesses_rem, used_letters):
        embed=discord.Embed(
            title=self.gamemode,
            color=discord.Color.blurple(),
            description="Incorrect. Type another guess!"
        )
        # guessed words
        for guess in guessed_words.keys():
            embed.add_field(name="", value=guessed_words[guess][1], inline=False)
        # letters used
        embed.add_field(name="Letters Used", value="", inline=False)
        # used letters
        letters_row1 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
        letters_row2 = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
        letters_row3 = ["z", "x", "c", "v", "b", "n", "m"]

        letters_str1 = ""
        letters_str2 = ""
        letters_str3 = ""

        for letter in letters_row1:
            letters_str1 += used_letters[letter].get_state()
        for letter in letters_row2:
            letters_str2 += used_letters[letter].get_state()
        for letter in letters_row3:
            letters_str3 += used_letters[letter].get_state()

        embed.add_field(name="", value=letters_str1, inline=False)
        embed.add_field(name="", value=letters_str2, inline=False)
        embed.add_field(name="", value=letters_str3, inline=False)
        # guess counter
        embed.add_field(name="Guess #", value=str(6 - guesses_rem) + "/6", inline=False)
        await self.ctx.send(embed=embed, reference=guess_obj)

    # send embed for game cancellation
    async def send_cancel_embed(self, guess_obj):
        embed=discord.Embed(
            title="Game Cancelled",
            color=discord.Color.red()
        )
        await self.ctx.send(embed=embed, reference=guess_obj)

    # send embed for game win
    async def send_win_embed(self, guessed_words, guess_obj, guesses_rem):
        embed=discord.Embed(
            title=self.gamemode,
            color=discord.Color.green(),
            description="You Won!"
        )
        for guess in guessed_words.keys():
            embed.add_field(name="", value=guessed_words[guess][1], inline=False)
        embed.add_field(name="Guesses Taken", value=str(6 - guesses_rem) + "/6", inline=False)
        await self.ctx.send(embed=embed, reference=guess_obj)

    # send embed for game lose
    async def send_lose_embed(self, guessed_words, guess_obj, hidden_word):
        embed=discord.Embed(
            title=self.gamemode,
            color=discord.Color.red(),
            description="Game Over!"
        )
        for guess in guessed_words.keys():
            embed.add_field(name="", value=guessed_words[guess][1], inline=False)
        embed.add_field(name="Out of Guesses!", value="Word was " + hidden_word.upper(), inline=False)
        await self.ctx.send(embed=embed, reference=guess_obj)
    
     # send embed for invalid guess
    async def send_invalid_embed(self, wordle_result, guess_obj):
        embed=discord.Embed(
            title="Invalid Guess!",
            color=discord.Color.yellow(),
            description="Type another guess!"
        )
        if wordle_result[0] == 2:
            embed.add_field(name="Reason", value="Guess is TOO LONG")
        elif wordle_result[0] == 3:
            embed.add_field(name="Reason", value="Guess is TOO SHORT")
        elif wordle_result[0] == 4:
            embed.add_field(name="Reason", value="Guess contains INVALID CHARACTERS")
        elif wordle_result[0] == 5:
            embed.add_field(name="Reason", value="Guess is NOT A REAL WORD")
        elif wordle_result[0] == 6:
            embed.add_field(name="Reason", value="Guess has ALREADY BEEN TRIED")
        await self.ctx.send(embed=embed, reference=guess_obj)

# starts Standard Wordle game instance
async def run(ctx, interaction, bot_users):
    
    # check if the guess appears in the same channel as the game
    # check if the guess is sent by the user who started the game
    def check_guess(message):
        # game was started via the !newgame menu
        if interaction != None:
            if message.channel.id == interaction.channel.id and message.author == interaction.user:
                return message
        # game was started via the !sw command
        elif message.channel.id == ctx.channel.id and message.author == ctx.author:
            return message

    # start a new Standard Wordle game
    game = StandardWordle(False)

    # initialize a new reponseSender for the current game
    sender = StandardWordleResponseSender(ctx, "Standard Wordle")

    # check how the current game a was started
    # game was started via the !newgame menu
    if interaction != None:
        print(f"[INFO] {interaction.user} started a new Wordle game (mode=Standard Wordle, hidden_word={game.get_hidden_word()})")
        await sender.send_start_embed(interaction.user)
    # game was started via the !sw command
    else:
        print(f"[INFO] {ctx.author} started a new Wordle game (mode=Standard Wordle, hidden_word={game.get_hidden_word()})")
        await sender.send_start_embed(ctx.author)

    # continue listening for guesses while the game is active
    while not game.is_terminated():
        guess = await ctx.bot.wait_for("message", check=check_guess)
        # ignore empty guesses and guesses that start with "!", unless it's the quit command ("!q")
        while guess.content == "" or guess.content[0] == "!":
            if guess.content == "!q" or guess.content == "!quit":
                print(f"[INFO] {ctx.author} quit their Wordle game (mode=Standard Wordle, hidden_word={game.get_hidden_word()})")
                await sender.send_cancel_embed(guess)
                bot_users[ctx.author].set_in_game(False) # change user in_game state
                bot_users[ctx.author].add_forfeit() # increment game forfeits
                return
            guess = await ctx.bot.wait_for("message", check=check_guess)

        # access wordle response for guess
        wordle_result = game.make_guess(guess.content)

        # guess is correct
        if wordle_result[0] == 0:
            print(f"[INFO] {ctx.author} won their Wordle game (mode=Standard Wordle, hidden_word={game.get_hidden_word()})")
            await sender.send_win_embed(game.get_history(), guess, game.get_guesses_rem())
            bot_users[ctx.author].set_in_game(False) # change user in_game state
            bot_users[ctx.author].add_win() # increment game wins
            bot_users[ctx.author].update_fastest_guess(game.get_game_time()) # set fastest guess
            return
        # guess is incorrect
        else:
            if wordle_result[0] == 1:
                for letter_obj in wordle_result[1]:
                    if letter_obj.get_state_id() == 1:
                        bot_users[ctx.author].add_gray_tile()
                    if letter_obj.get_state_id() == 2:
                        bot_users[ctx.author].add_yellow_tile()
                    if letter_obj.get_state_id() == 3:
                        bot_users[ctx.author].add_green_tile()
                if not game.is_terminated():
                    await sender.send_game_embed(game.get_history(), guess, game.get_guesses_rem(), game.get_letters())
            else:
                await sender.send_invalid_embed(wordle_result, guess)
    
    print(f"[INFO] {ctx.author} lost their Wordle game (mode=Standard Wordle, hidden_word={game.get_hidden_word()})")
    await sender.send_lose_embed(game.get_history(), guess, game.get_hidden_word())
    bot_users[ctx.author].set_in_game(False) #change user in_game state
    bot_users[ctx.author].add_loss() # increment game losses
    return