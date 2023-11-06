import discord
import enchant
import time

from wordle.exceptions import InvalidGuess
from wordle.letter import Letter, LetterState, blank_square
from users import User

class Wordle:
    """
    A class used to represent a Wordle game.
    """

    def __init__(self, hidden_word:str, max_attempts:int, user:User, channel):
        """
        Constructs a Wordle game.

        Args:
            hidden_word (str): The word the player is trying to guess.
            max_attempts (int): The number of attempts the user has to guess the hidden word.
            user (User): The user playing this game.
        """

        self.hidden_word = hidden_word.strip().lower()
        'The word the user is trying to guess.'
        self.user = user
        'The user playing this game.'
        self.channel = channel
        'The channel this game is in'
        self.max_attempts = max_attempts
        'The number of attempts the user has to guess the hidden word.'
        self.attempt_number = 0
        'The number of attempts the user used.'
        self.has_guessed_word = False
        'Whether the user has guessed the hidden word.'
        self.letters_used = dict()
        'All the letters the user has used throughout the game.'
        self.history = list()
        "The user's history of guessed words."
        self.start_time = time.time()
        "The time when the game started."
        self.end_time = None
        "The time when the game terminated."

        self.user.in_game = True
        for i in range(97, 123):
            self.letters_used[chr(i)] = Letter(chr(i))

    def elapsed_time(self) -> float:
        """
        Gets the total time the game ran if the game has terminated. Otherwise,
        gets the time the game has elapsed since it started.

        Returns:
            float: The total time the game has ran, or the time the game has
            elapsed since it started.
        """
        return self.end_time - self.start_time if self.end_time else time.time() - self.start_time

    def remaining_attempts(self) -> int:
        """
        Get the remaining attempts the user has left.
        """
        return self.max_attempts - self.attempt_number

    def is_terminated(self) -> bool:
        """
        Whether the game has been terminated.

        Returns:
            bool: Returns 'true' if the game has been terminated; otherwise 'false'.
        """
        return self.has_guessed_word or self.attempt_number == self.max_attempts

    def terminate(self) -> None:
        """
        Terminates the game, preventing the user from playing.
        """
        self.user.in_game = False
        self.end_time = time.time()

        if not self.is_terminated():
            self.user.forfeits += 1
            self.attempt_number = self.max_attempts
        elif self.has_guessed_word:
            self.user.standard_fastest_guess = min(
                self.elapsed_time(),
                self.user.standard_fastest_guess
            ) if self.user.standard_fastest_guess != -1 else self.elapsed_time()

    def make_guess(self, guess:str) -> list[Letter]:
        """
        Makes an attempt to guess the hidden word.

        Args:
            guess (str): The guess the user made.

        Raises:
            InvalidGuess: Guess is too long, is too short, is not a word in the English dictionary, or
            contains special characters.

        Returns:
            list[Letter]: Returns the guess in color-code. Returns None if the user has already won,
            or if they ran out of attempts.
        """
        if self.is_terminated():
            return None

        guess = guess.strip().lower()

        if len(guess) > len(self.hidden_word):
            raise InvalidGuess(guess, "Guess is too long.")

        if len(guess) < len(self.hidden_word):
            raise InvalidGuess(guess, "Guess is too short.")

        if not guess.isalpha():
            raise InvalidGuess(guess, "Guess contains special characters.")

        # if not enchant.Dict("en_US").check(guess) and guess != self.hidden_word:
        #     raise InvalidGuess(guess, "Guess is not a word in the English dictionary.")

        return self.__make_guess(guess)

    def __make_guess(self, guess:str) -> list[Letter]:
        color_codes = self.__color_code_guess(guess)
        self.history.append(color_codes)
        self.__update_letters_used(color_codes)
        self.__update_user_stats(color_codes)
        self.__use_attempt()
        return color_codes

    def __color_code_guess(self, guess:str) -> list[Letter]:
        if guess == self.hidden_word:
            self.user.wins += 1
            self.has_guessed_word = True
            self.terminate()
            return [Letter(char, LetterState.GREEN) for char in guess]
        return self.__color_code_algorithm(guess)

    def __color_code_algorithm(self, guess:str) -> list[Letter]:
        color_codes = [Letter(char, LetterState.GRAY) for char in guess]
        remaining = list(self.hidden_word)
        possible_yellows = list()
        index = 0

        for hidden_char, guess_char in zip(self.hidden_word, guess):
            if hidden_char == guess_char:
                color_codes[index].state = LetterState.GREEN
                remaining.remove(guess_char)
            elif guess_char in remaining:
                possible_yellows.append((guess_char, index))
            index += 1

        for char, idx in possible_yellows:
            if char in remaining:
                color_codes[idx].state = LetterState.YELLOW
                remaining.remove(char)

        return color_codes

    def __update_letters_used(self, letters:list[Letter]):
        for char in letters:
            letter = self.letters_used[char.letter]
            if char.state.value > letter.state.value:
                letter.state = char.state

    def __update_user_stats(self, letters:list[Letter]):
        for letter in letters:
            match letter.state:
                case LetterState.GRAY:
                    self.user.grays_generated += 1
                case LetterState.YELLOW:
                    self.user.yellows_generated += 1
                case LetterState.GREEN:
                    self.user.greens_generated += 1

    def __use_attempt(self):
        self.attempt_number += 1
        if self.attempt_number == self.max_attempts:
            self.user.losses += 1
            self.terminate()

def blank_game_embed(game:Wordle, gamemode:str) -> discord.Embed:
    """
    Generates a blank game embed based on the given Wordle game.

    Args:
        game (Wordle): The Wordle game.
        gamemode (str): The name of the gamemode.

    Returns:
        Embed: The blank game embed of a Wordle game.
    """
    empty_word = blank_square * len(game.hidden_word)
    embed = discord.Embed(
        title = gamemode,
        color = discord.Color.yellow()
    )
    embed.set_author(
        name = game.user.user.display_name,
        icon_url = game.user.user.avatar.url
    )
    for _ in range(game.max_attempts):
        embed.add_field(name="", value=empty_word, inline=False)

    qwerty_keyboard = [
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
        ["z", "x", "c", "v", "b", "n", "m"]
    ]
    keyboard_ui = [''.join(game.letters_used[letter].emoji() for letter in keys) for keys in qwerty_keyboard]
    for ui in keyboard_ui:
        embed.add_field(name="", value=ui, inline=False)

    return embed

def update_game_embed(embed:discord.Embed, game:Wordle, word:list[Letter]) -> None:
    """
    Updates the game embed of a Wordle game. The given word will be inserted in the
    next empty row.

    Args:
        embed (Embed): The embed to update.
        game (Wordle): The Wordle game of the embed.
        word (list[Letter]): The word used for updating.
    """
    color_codes = ''.join(letter.emoji() for letter in word)
    embed.set_field_at(
        index = game.attempt_number - 1,
        name = "",
        value = color_codes,
        inline = False
    )
    if game.has_guessed_word:
        for _ in range(3):
            embed.remove_field(game.max_attempts)
            embed.color=discord.Color.green()
    else:
        qwerty_keyboard = [
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
            ["z", "x", "c", "v", "b", "n", "m"]
        ]
        keyboard_ui = [''.join(game.letters_used[letter].emoji() for letter in keys) for keys in qwerty_keyboard]
        for i in range(3):
            embed.set_field_at(
                index = game.max_attempts + i,
                name = "",
                value = keyboard_ui[i],
                inline = False
            )

async def display_rules(game:Wordle, gamemode:str, rules:str):
    """
    Displays the rules of a Wordle game.

    Args:
        game (Wordle): The game the rules apply to.
        gamemode (str): The name of the gamemode.
        rules (str): The rules of the game.
    """
    embed = discord.Embed(
        title = gamemode,
        color = discord.Color.blurple(),
        description = rules
    )
    embed.set_author(
        name = game.user.user.display_name,
        icon_url = game.user.user.avatar.url
    )
    await game.channel.send(embed=embed)

async def display_error(channel, title:str, message:str):
    """
    Displays an error message to a channel.

    Args:
        channel: The channel the error message will be sent to.
        title (str): The title of the embed.
        message (str): The message/description of the embed.
    """
    embed = discord.Embed(
        title = title,
        color = discord.Color.red(),
        description = message
    )
    await channel.send(embed=embed)

async def display_warning(channel, title:str, message:str):
    """
    Displays a warning message to a channel.

    Args:
        channel: The channel the warning message will be sent to.
        title (str): The title of the embed.
        message (str): The message/description of the embed.
    """
    embed = discord.Embed(
        title = title,
        color = discord.Color.yellow(),
        description = message
    )
    await channel.send(embed=embed)

async def display_message(channel, title:str, message:str):
    """
    Displays a message to a channel.

    Args:
        channel: The channel the message will be sent to.
        title (str): The title of the embed.
        message (str): The message/description of the embed.
    """
    embed = discord.Embed(
        title = title,
        color = discord.Color.blurple(),
        description = message
    )
    await channel.send(embed=embed)
