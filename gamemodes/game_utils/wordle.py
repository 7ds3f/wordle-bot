'''
Wordle algorithm + word generation functions.
'''

import enchant
import random
import string
import time
import linecache
import letter

def wordle_helper(guess:str, hidden_word:str, game_letters:dict) -> tuple:
    """
    DESC: checks if a user's guess matches the hidden word. A guess string will be converted into
    a list of Letter objects, each representing a different letter in the guess.

    MODIFIES: game_letters - the state of the used letters will be updated in game_letters

    PARAMS: guess (str) - the user's guess
            hidden_word (str) - the hidden word
            game_letters (dict) - a dictionary of the whole alphabet and each letter's status for the current game

    RETURNS: (tuple(bool, list(Letter))) (success_boolean, [Letter, Letter, Letter, Letter, Letter]), where:
    success_boolean True = guess and hidden_word match
    success_boolean False = guess and hidden_word do NOT match
    -------------
    [Letter, Letter, Letter, Letter, Letter], where
    each Letter object represents a letter in the guess. Each letter's state
    will reflect its validity relative to the hidden word. 
    """

    guess = guess.lower()
    hidden_word = hidden_word.lower()

    result = []
    for char in guess:
        result.append(letter.Letter(char, letter.LetterState.GRAY))
        game_letters[char].set_state(letter.LetterState.GRAY, False)

    # guess is correct
    if guess == hidden_word:
        for char_idx in range(len(guess)):
            result[char_idx].set_state(letter.LetterState.GREEN, True)
            game_letters[guess[char_idx]].set_state(letter.LetterState.GREEN, True)
        return (True, result)
    # guess is NOT correct
    else:
        #initialize and load dictionaries for guess and hidden_word
        guess_dict = dict()
        hidden_word_dict = dict()

        for char_index in range(5):
            guess_dict.update({guess[char_index] : set()})
            hidden_word_dict.update({hidden_word[char_index] : set()})
        for char_index in range(5):
            guess_dict[guess[char_index]].add(char_index)
            hidden_word_dict[hidden_word[char_index]].add(char_index)

        #compare word dictionaries and update result
        to_remove = set()
        for char in guess_dict.keys():
            if char in hidden_word_dict:
                for index in guess_dict[char]:
                    if index in hidden_word_dict[char]:
                        result[index] = letter.Letter(char, letter.LetterState.GREEN)
                        game_letters[char].set_state(letter.LetterState.GREEN, False)
                        to_remove.add(index)
                guess_dict[char] = guess_dict[char] - to_remove
                hidden_word_dict[char] = hidden_word_dict[char] - to_remove
                to_remove.clear()

                hidden_word_rem = len(hidden_word_dict[char])
                guess_rem = len(guess_dict[char])
                i = 0
                j = 0
                while (i < hidden_word_rem) and (j < guess_rem):
                    result[min(guess_dict[char])] = letter.Letter(char, letter.LetterState.YELLOW)
                    game_letters[char].set_state(letter.LetterState.YELLOW, False)
                    i += 1
                    j += 1

        """
        # Edmond's superior algorithm
        remaining = list(hidden_word)
        
        for hidden_char, guess_char in zip(hidden_word, guess):
            if guess_char == hidden_char:
                result.append(letter.Letter(guess_char, letter.LetterState.GREEN))
                game_letters[guess_char].set_state(letter.LetterState.GREEN, False)
                remaining.remove(guess_char)
            elif guess_char in remaining:
                result.append(letter.Letter(guess_char, letter.LetterState.YELLOW))
                game_letters[guess_char].set_state(letter.LetterState.YELLOW, False)
                remaining.remove(guess_char)
            else:
                result.append(letter.Letter(guess_char, letter.LetterState.GRAY))
                game_letters[guess_char].set_state(letter.LetterState.GRAY, False)
        """

        return (False, result)

def wordle(guess:str, hidden_word:str, guessed_words:dict, d:enchant.Dict, game_letters:dict) -> tuple:
    """
    DESC: checks if a user's guess is valid and matches the hidden word. See below for validity checks. 
    A guess string will be converted into a list of Letter objects, each representing a different letter
    in the guess. 
    
    MODIFIES: guessed_words - every valid guess and its result will be added to guessed_words
              game_letters - the state of the used letters will be updated in game_letters

    PARAMS: guess (str) - the user's guess
            hidden_word (str) - the hidden word
            guessed_words (dict) - dictionary of valid guesses and results in current game
            d (enchant.Dict) - a dictionary of valid words in some language
            game_letters (dict) - a dictionary of the whole alphabet and each letter's status for the current game

    RETURNS: (error_code, [Letter, Letter, Letter, Letter, Letter]), where:
    error_code 0 = guess is correct
    error_code 1 = guess is valid but incorrect
    error_code 2 = guess is invalid (too long)
    error_code 3 = guess is invalid (too short)
    error_code 4 = guess is invalid (contains invalid characters)
    error_code 5 = guess is invalid (not a real word)
    error_code 6 = guess is invalid (guess has been guessed already)
    -------------
    [Letter, Letter, Letter, Letter, Letter], where
    each Letter object represents a letter in the guess. Each letter's state
    will reflect its validity relative to the hidden word. 

    If this value is [None, None, None, None, None], the guess is invalid
    """
    
    # [check guess validity]
    # guess is more than 5 characters
    if len(guess) > 5:
        return (2, [None, None, None, None, None])
    # guess is less than 5 characters
    if len(guess) < 5:
        return (3, [None, None, None, None, None])
    # guess contains invalid characters
    if not guess.isalpha():
        return (4, [None, None, None, None, None])
    # guess is not a real word
    if not d.check(guess.upper()):
        return (5, [None, None, None, None, None])
    # convert guess to all lowercase
    guess = guess.lower()
    # guess has been tried already in the current game
    if guess in guessed_words:
        return (6, guessed_words[guess])
    # guess has NOT been tried already in the current game
    else:
        # guess is valid
        # [compare guess against hidden_word]
        compare_result = wordle_helper(guess, hidden_word, game_letters)
        # guess is correct
        if compare_result[0]:
            # add guess and text-based + discord fomatted result to guessed_words
            guessed_words.update({guess : (compare_result[1], result_format(compare_result))})
            return (0, compare_result[1])
        # guess is incorrect
        else:
            # add guess and text-based + discord fomatted result to guessed_words
            guessed_words.update({guess : (compare_result[1], result_format(compare_result))})
            return (1, compare_result[1])

#TODO come up with a more efficient way to do this
def random_word(d:enchant.Dict, Mode:bool=False) -> str:
    """
    DESC: Generates a random word by joining 5 random characters and checking if result is a word.
    Has an optional mode to track execution time and attempts

    PARAMS: d - dictionary of english words
            Mode - enables test mode, False by default

    PRINTS: If in test mode: the word, attempts, and execution time in seconds

    RETURNS: (str) a random word
    """

    start_time = time.time()
    count = 0
    word = ''
    # Try diferent combinations until a valid word is generated
    while True:
        count += 1
        # Generates 5 random chars and joins them into a word
        word = ''.join([random.choice(string.ascii_uppercase) for _ in range(5)])
        if d.check(word): break
    
    #If in test mode, prints some stats
    if Mode:
        print('Got [ %s ] in [ %d ] tries, took [ %s ] seconds' % (word, count, time.time()-start_time))
    
    return word

def daily_word() -> str:
    """
    DESC: Generates a daily word by using the current date as a seed for the random number generator
        
    RETURNS: (str) a word based on the time of day
    """
    # set the seed
    seed = time.strftime("%d/%m/%Y")
    random.seed(seed)
    # select a random number from 0 to 5756 (number of 5 letter words in the dictionary)
    random_num = random.randint(0, 5756)
    # select the word from sgb-words.txt at the random number
    word = linecache.getline("game_utils/sgb-words.txt", random_num)
    # remove the newline character from the word
    word = word[:-1]
    return word.upper()

def result_format(wordle_result:tuple) -> str:
    """
    DESC: converts a wordle_result from the wordle() function into a string of Discord emoji identifiers
          which correspond to letter states

    PARMS: wordle_result (tuple) - result from wordle() function

    RETURNS: (str) string of colored letter identifiers corresponding to wordle_result
    """

    result = ""
    for letter in wordle_result[1]:
        result += letter.get_state()
    return result

def main():
    """
    DESC: wordle test function
    """

    d = enchant.Dict("en_US")
    hidden_word = "atoms"
    print("Hidden Word:", hidden_word)
    guessed_words = dict()
    game_letters = dict()
    # build a dictionary for the alphabet for the current game
    for i in range(97, 123):
        game_letters.update({chr(i) : letter.Letter(chr(i), letter.LetterState.NONE)})

    guess = input("Enter a guess (-1 to exit)...\n")
    while (guess != "-1"):
        wordle_result = wordle(guess, hidden_word, guessed_words, d, game_letters)
        if wordle_result[0] == 0:
            print("wordle(): guess is valid and CORRECT", guessed_words[guess])
            print('\nThanks for playing! You got %s in %d (valid & distinct) tries.\n' % (hidden_word, len(guessed_words)))
            break
        elif wordle_result[0] == 1:
            print("wordle(): guess is valid but INCORRECT", guessed_words[guess][0])
        elif wordle_result[0] == 2:
            print("wordle(): guess is TOO LONG")
        elif wordle_result[0] == 3:
            print("wordle(): guess is TOO SHORT")
        elif wordle_result[0] == 4:
            print("wordle(): guess contains INVALID CHARACTERS")
        elif wordle_result[0] == 5:
            print("wordle(): guess is NOT A REAL WORD")
        elif wordle_result[0] == 6:
            print("wordle(): guess has been ALREADY GUESSED", guessed_words[guess][0])
        else:
            print("wordle(): ERROR")
        guess = input("Enter another guess...\n")

if __name__ == "__main__":
    print("Running wordle()...")
    main()

