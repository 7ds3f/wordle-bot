import enchant
import time

from wordle.exceptions import InvalidGuess
from wordle.letter import Letter, LetterState
from users import User

class Wordle:
    """
    A class used to represent a Wordle game.
    """
    
    def __init__(self, hidden_word:str, max_attempts:int, user:User):
        """
        Constructs a Wordle game.

        Args:
            hidden_word (str): The word the player is trying to guess.
        """
        
        self.hidden_word = hidden_word.lower().strip()
        'The word the player is trying to guess.'
        self.user = user
        self.max_attempts = max_attempts
        'The number of attempts the player has to guess the hidden word.'
        self.attempt_number = 0
        self.has_guessed_word = False
        'Whether the player has guessed the hidden word.'
        self.letters_used = dict()
        'All the letters the player has used for each guess.'
        self.history = list()
        "The player's history of guessed words."
        self.start_time = time.time()

        self.user.in_game = True
        
        for i in range(97, 123):
            self.letters_used[chr(i)] = Letter(chr(i))
    
    def elapsed_time(self) -> float:
        return self.end_time - self.start_time

    def remaining_attempts(self) -> int:
        return self.max_attempts - self.attempt_number

    def is_terminated(self) -> bool:
        """
        Whether the game has been terminated.
        
        Returns:
            bool: Returns 'true' if the game has been terminated; otherwise 'false'.
        """
        return self.has_guessed_word or self.attempt_number == self.max_attempts
        
    def terminate(self):
        if not self.is_terminated():
            self.user.forfeits += 1
            self.attempt_number = self.max_attempts
            
        self.user.in_game = False
        self.end_time = time.time()

    def make_guess(self, guess:str) -> list[Letter]:
        """
        Attempt to guess the hidden word.

        Args:
            guess (str): The guess the player made.

        Raises:
            InvalidGuess: Guess is too long, is too short, is not a word in the English dictionary, or
            contains special characters.

        Returns:
            list[Letter]: Returns the guess in color-code. Returns None if the player has already won,
            or if they ran out of attempts.
        """
        
        if self.attempt_number == -1 or self.has_guessed_word:
            return None
        
        guess = guess.strip().lower()
        
        if len(guess) > len(self.hidden_word):
            raise InvalidGuess(guess, "Guess is too long.")
        
        if len(guess) < len(self.hidden_word):
            raise InvalidGuess(guess, "Guess is too short.")
        
        if not guess.isalpha():
            raise InvalidGuess(guess, "Guess contains special characters.")
        
        if not enchant.Dict("en_US").check(guess) and guess != self.hidden_word:
            raise InvalidGuess(guess, "Guess is not a word in the English dictionary.")
        
        return self.__make_guess(guess)
    
    def __make_guess(self, guess:str) -> list[Letter]:
        self.__use_attempt()
        
        if guess == self.hidden_word:
            self.user.wins += 1
            self.has_guessed_word = True
            self.terminate()
            return [Letter(char, LetterState.GREEN) for char in guess]
        
        output = self.__color_code_guess(guess)
        self.history.append(output)
        self.__update_letters_used(output)
        return output
    
    def __color_code_guess(self, guess:str) -> list[Letter]:
        output = [None] * len(self.hidden_word)
        remaining = list(self.hidden_word)

        for i in range(len(self.hidden_word)):
            letter = guess[i]
            if letter == self.hidden_word[i]:
                output[i] = (Letter(letter, LetterState.GREEN))
                self.user.greens_generated += 1
                remaining.remove(letter)
                print(f'GREEN: {letter}')
        
        for i in range(len(self.hidden_word)):
            letter = guess[i]
            if letter in remaining:
                output[i] = Letter(letter, LetterState.YELLOW)
                self.user.yellows_generated += 1
                remaining.remove(letter)
                print(f'YELLOW: {letter}')
            elif not output[i]:
                output[i] = Letter(letter, LetterState.GRAY)
                print(f'GRAY: {letter}')
        
        return output
        
    def __update_letters_used(self, letters:list[Letter]):
        for char in letters:
            letter = self.letters_used[char.letter]
            if char.state.value > letter.state.value:
                letter.state = char.state
        
    def __use_attempt(self):
        self.attempt_number += 1
        if self.attempt_number == self.max_attempts:
            self.user.losses += 1
            self.terminate()
        