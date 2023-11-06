import random
import time

from wordle import *
from wordle.exceptions import InvalidGuess

WORD_FILE_PATH = "standard_words.txt"
"The file path to the words a daily Wordle game will use."
MAX_ATTEMPTS = 6
"The maximum attempts a daily Wordle game will allow."

def daily_word() -> str:
    """
    Picks a new word from the text file indicated by WORD_FILE_PATH per day.

    Returns:
        str: A word from the daily word pool.
    """
    seed = time.strftime("%d/%m/%Y")
    rand = random.Random(seed)
    with open(WORD_FILE_PATH, 'r', encoding='utf-8') as file:
        words = file.readlines()
        return rand.choice(words).strip()

class Daily(Wordle):
    """
    A class used to represent a daily Wordle game.
    """

    def __init__(self, user:User, channel):
        """
        Constructs a daily Wordle game.

        In a daily Wordle game, a user only has 6 guesses
        and the hidden word is 5-letters long.

        Args:
            user (User): The user playing this game.
            channel: The channel this game is in.
        """
        super().__init__(daily_word(), MAX_ATTEMPTS, user, channel)
        self.game_status = blank_game_embed(self, "Daily Wordle")

    async def run(self, interaction:discord.Interaction):
        """
        Runs the game.

        Args:
            interaction (Interaction): The interaction.
        """
        print(f"{self.user.user.name} started a Wordle game (mode:Daily, hidden_word={self.hidden_word})")
        await self.__display_rules()
        while not self.is_terminated():
            guess = await self.__get_guess(interaction)
            try:
                color_codes = self.make_guess(guess)
                if not color_codes: return
                update_game_embed(self.game_status, self, color_codes)
                await self.channel.send(embed=self.game_status)
            except InvalidGuess as e:
                await display_warning(self.channel, "Invalid Guess", e.message)

    async def __get_guess(self, interaction:discord.Interaction) -> str:
        def check_guess(message):
            if message.channel.id == self.channel.id and message.author == self.user.user:
                return message

        guess = await interaction.client.wait_for("message", check=check_guess)
        if not self.is_terminated():
            await guess.delete()
            return guess.content

    async def __display_rules(self):
        await display_rules(
            game = self,
            gamemode = "Daily Wordle",
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
