from wordle import *
from wordle.exceptions import InvalidGuess

MAX_ATTEMPTS = 6
"The maximum attempts a standard Wordle game will allow."

class Standard(Wordle):
    """
    A class used to represent a standard Wordle game.
    """

    def __init__(self, user:User, channel, hidden_word):
        """
        Constructs a standard Wordle game.

        In a standard Wordle game, a user only has 6 guesses
        and the hidden word is 5-letters long.

        Args:
            user (User): The user playing this game.
            channel: The channel this game is in.
        """
        super().__init__(hidden_word, MAX_ATTEMPTS, user, channel)
        self.game_status = blank_game_embed(self, "Standard Wordle")
        
    async def run(self, interaction:discord.Interaction):
        """
        Runs the game.

        Args:
            interaction (Interaction): The interaction.
        """
        print(f"{self.user.user.name} started a Wordle game (mode:Standard, hidden_word={self.hidden_word})")
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
