import random
import requests

from wordle import *
from wordle.exceptions import InvalidGuess
from wordle.letter import blank_square

WORD_FILE_PATH = "feudle_words.txt"
"The file path to the words a Feudle game will use."
MAX_ATTEMPTS = 6
"The maximum attempts a Feudle game will allow."

def random_word() -> str:
    """
    Generates a random word from the text file indicated by WORD_FILE_PATH.

    Returns:
        str: A random word from the standard word pool.
    """
    with open(WORD_FILE_PATH, 'r', encoding='utf-8') as file:
        words = file.readlines()
        return random.choice(words).strip()

#TODO: this is SLOWWWW
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
        word_data = requests.get(url).json()

        # get all word phrases (if any) for all meanings
        phrases = []
        for meaning_idx in range(0, len(word_data[0]["meanings"])):
            for definition in word_data[0]["meanings"][meaning_idx]["definitions"]:
                if "example" in definition and hidden_word in definition["example"].split():
                    phrases.append(definition["example"])

        # if no phrases for the word were found
        if not phrases:
            return "-1"
        else:
            # pick a random phrase + split it
            phrase_list = phrases[random.randint(0, len(phrases)-1)].split()
            phrase_list[0] = phrase_list[0].capitalize()

            # remove all occurences of the hidden word from the phrase
            word_count = phrase_list.count(hidden_word)
            while word_count > 0:
                phrase_list[phrase_list.index(hidden_word)] = blank_square * len(hidden_word)
                word_count -= 1
            return " ".join(phrase_list)
    # if word is not in dictionary
    except:
        return "-1"

class Feudle(Wordle):
    """
    A class used to represent a Feudle game.
    """

    def __init__(self, user:User, channel):
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
        #TODO: this is SLOWWWW
        print(f"Generating a phrase for a new Feudle game...")
        self.random_word = random_word()
        self.word_phrase = word_phrase(self.random_word)
        while self.word_phrase == "-1":
            self.random_word = random_word()
            self.word_phrase = word_phrase(self.random_word)
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
