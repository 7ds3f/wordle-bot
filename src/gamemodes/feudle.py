import random
import requests

from wordle import *
from wordle.exceptions import InvalidGuess
from wordle.letter import blank_square

MAX_ATTEMPTS = 6
"The maximum attempts a Feudle game will allow."

def word_phrase(hidden_word) -> str:
    """
    Generates a censored usage phrase for hidden_word

    Returns:
        str: a usage phrase for hidden_word
    """

    # if word is in dictionary
    try:
        # fetch word data from api
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{hidden_word}"
        meanings = requests.get(url).json()[0]["meanings"]

        # get all word phrases (if any) for all meanings
        phrases = []
        for meaning in meanings:
            for definition in meaning["definitions"]:
                if 'example' not in definition: continue
                
                phrase = f' {definition["example"]}'
                index = phrase.find(f' {hidden_word}')
                if index == -1: continue
                
                phrase = phrase[1:index+1] + (blank_square * len(hidden_word)) + phrase[index + len(hidden_word) + 1:]
                phrases.append(phrase)
                
        if phrases: return random.choice(phrases)
    except:
        pass
    return None

class Feudle(Wordle):
    """
    A class used to represent a Feudle game.
    """

    def __init__(self, user:User, channel, hidden_word):
        """
        Constructs a Feudle game.

        In a Feudle game, a user only has 6 guesses and the
        hidden word is 5-letters long. The player will also
        be provided with a censored phrase that demonstrates
        the usage of the hidden word.

        Args:
            user (User): The user playing this game.
            channel: The channel this game is in.
        """
        print(f"Generating a phrase for a new Feudle game...")
        self.random_word = hidden_word
        self.word_phrase = word_phrase(self.random_word)
        # while not self.word_phrase:
        #     self.random_word = random_word()
        #     self.word_phrase = word_phrase(self.random_word)
        super().__init__(self.random_word, MAX_ATTEMPTS, user, channel)
        self.game_status = blank_game_embed(self, "Feudle")

    async def run(self, interaction:discord.Interaction):
        """
        Runs the game.

        Args:
            interaction (Interaction): The interaction.
        """
        print(f"{self.user.user.name} started a Wordle game (mode:Feudle, hidden_word={self.hidden_word})")
        await self.__display_rules()
        while not self.is_terminated():
            guess = await self.__get_guess(interaction)
            try:
                color_codes = self.make_guess(guess)
                if not color_codes: return
                update_game_embed(self.game_status, self, color_codes)
                self.game_status.description = f"*{self.word_phrase}*"
                await self.channel.send(embed=self.game_status)
            except InvalidGuess as e:
                await display_warning(self.channel, "Invalid Guess", e.message)

        if self.won:
            await interaction.channel.send('Congrats, you guessed {} in {} guess(es)!'
                                           .format(self.hidden_word, self.attempt_number))
        else:
            await interaction.channel.send('You\'ve run out of guesses, the word was {}.'
                                           .format(self.hidden_word))

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
            gamemode = "Feudle Wordle",
            rules =
            f"""
            **How to play?**
            You have {self.max_attempts} attempts to fill in a sentence's missing word.

            **Green** indicates that the letter is in the correct spot.
            **Yellow** indicates that the letter is in the wrong spot.
            **Gray** indicates that the letter is not in the word.

            *{self.word_phrase}*

            Type a word to start playing.
            """
        )
