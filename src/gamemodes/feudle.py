import random
import os
import openai

from wordle import *
from wordle.exceptions import InvalidGuess
from wordle.letter import blank_square
from dotenv import load_dotenv

load_dotenv()

WORD_FILE_PATH = "standard_words.txt"
"The file path to the words a feudle Wordle game will use."
MAX_ATTEMPTS = 6
"The maximum attempts a feudle Wordle game will allow."
TOKEN = os.getenv("CHATGPT_TOKEN")
"The token of the ChatGPT API"

openai.api_key = TOKEN

def random_word() -> str:
    """
    Generates a random word from the text file indicated by WORD_FILE_PATH.

    Returns:
        str: A random word from the standard word pool.
    """
    with open(WORD_FILE_PATH, 'r', encoding='utf-8') as file:
        words = file.readlines()
        return random.choice(words).strip()

def word_phrase(hidden_word) -> str:
    """
    Generates a censored usage phrase for hidden_word

    Returns:
        str: a usage phrase for hidden_word
    """
    phrase = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "Given a single word, you need to create a short sentence using this word which examplifies the meaning of the word. Then replace this word in the sentence with a blank (_____)."},
        {"role": "user", "content": hidden_word}
      ]
    )

    return phrase

class Feudle(Wordle):
    """
    A class used to represent a feudle Wordle game.
    """

    def __init__(self, user):
        """
        Constructs a feudle Wordle game.

        In a feudle Wordle game, a user only has 6 guesses
        and the hidden word is 5-letters long. The player will also
        be provided with a censored phrase that demonstrates
        the usage of the hidden word.
        """
        self.random_word = random_word()
        super().__init__(self.random_word, MAX_ATTEMPTS, user)
        self.game_status = blank_game_embed(self, "Feudle Wordle")
        self.word_phrase = word_phrase(self.random_word)
        print(self.word_phrase)

    async def run(self, ctx, channel):
        """
        Runs the game.

        Args:
            ctx: The context.
            channel: The channel messages will be sent to.
        """
        print(f"{self.user.user.name} started a Wordle game (mode:Feudle, hidden_word={self.hidden_word})")
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
            gamemode = "Feudle Wordle",
            rules =
            f"""
            **How to play?**
            You have {self.max_attempts} attempts to fill in the missing word in a sentence.

            **Green** indicates that the letter is in the correct spot.
            **Yellow** indicates that the letter is in the wrong spot.
            **Gray** indicates that the letter is not in the word.

            Type a word to start playing.
            """
        )
