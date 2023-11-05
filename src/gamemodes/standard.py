import random

from wordle import *
from wordle.exceptions import InvalidGuess
from wordle.letter import blank_square

WORD_FILE_PATH = "standard_words.txt"
"The file path to the words a standard Wordle game will use."

MAX_ATTEMPTS = 6
"The maximum attempts a standard Wordle game will allow."

def random_word() -> str:
    """
    Generates a random word from the text file indicated by WORD_FILE_PATH.
    
    Returns:
        str: A random word from the standard word pool.
    """
    with open(WORD_FILE_PATH, 'r', encoding='utf-8') as file:
        words = file.readlines()
        return random.choice(words).strip()

class Standard(Wordle):
    """
    A class used to represent a standard Wordle game.
    """

    def __init__(self, user):
        """
        Constructs a standard Wordle game.

        In a standard Wordle game, a user only has 6 guesses
        and the hidden word is 5-letters long.
        """
        super().__init__(random_word(), MAX_ATTEMPTS, user)
        self.game_status = blank_game_embed(self, "Standard Wordle")
        
    async def run(self, ctx, channel):
        """
        Runs the game.

        Args:
            ctx: The context.
            channel: The channel messages will be sent to.
        """
        print(f"{self.user.user.name} started a Wordle game (mode:Standard, hidden_word={self.hidden_word})")
        await self.__display_rules(ctx)
        while not self.is_terminated():
            guess = await self.__get_guess(ctx, ctx)
            try:
                color_codes = self.make_guess(guess)
                update_game_embed(self.game_status, self, color_codes)
                await ctx.send(embed=self.game_status)
            except InvalidGuess as e:
                await display_warning(ctx, "Invalid Guess", e.message)
                pass

    async def __get_guess(self, ctx, channel) -> str:
        def check_guess(message):
            if message.channel.id == ctx.channel.id and self.user.user == message.author:
                return message
            
        guess = await ctx.bot.wait_for("message", check=check_guess)
        guess = guess.content
        while guess == '' or guess[0] == "!":
            if guess == '!q' or guess == '!quit':
                self.terminate()
                await display_error(channel, "Forfeited", "You have left the game.")
                return
            guess = await ctx.bot.wait_for("message", check=check_guess)
            guess = guess.content
        return guess
        
    async def __display_rules(self, channel):
        await display_rules(
            channel = channel,
            game = self,
            gamemode = "Standard Wordle",
            rules =
            f"""
            **How to play?**
            You have {self.max_attempts} attempts to guess the word.

            **Green** indicates that the letter is in the correct spot.
            **Yellow** indicates that the letter is in the wrong spot.
            **Gray** indicates that the letter is not in the word.
            
            Type a word to start playing.
            """
        )