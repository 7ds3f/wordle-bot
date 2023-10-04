'''
Baseline Wordle algorithm functions. Checks if a guess is valid and correct.
'''

'''
DESC: checks if a user's guess matches the hidden word.
PARAMS: user's guess (guess), hidden word (hidden_word)
RETURNS: (success_boolean, ["-", "-", "-", "-", "-"]), where:
    success_boolean True = guess and hidden_word match
    success_boolean False = guess and hidden_word do NOT match
    -------------
    ["-", "-", "-", "-", "-"], where
    a "-" indicates the letter is not present in the hidden_word
    a lowercase letter indicates that letter is present in the hidden_word but in the wrong place
    an uppercase letter indicates that letter is present in the hidden_word and in the right place
'''
#TODO: test this more
def wordle_helper(guess, hidden_word):
    hidden_word = hidden_word.lower()
    # guess is correct
    if guess == hidden_word:
        return (True, [*guess.upper()])
    # guess is NOT correct
    else:
        #initialize and load dictionaries for guess and hidden_word
        result = ["-", "-", "-", "-", "-"]
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
        for letter in guess_dict.keys():
            if letter in hidden_word_dict:
                for index in guess_dict[letter]:
                    if index in hidden_word_dict[letter]:
                        result[index] = letter.upper()
                        to_remove.add(index)
                guess_dict[letter] = guess_dict[letter] - to_remove
                hidden_word_dict[letter] = hidden_word_dict[letter] - to_remove
                to_remove.clear()

                hidden_word_rem = len(hidden_word_dict[letter])
                guess_rem = len(guess_dict[letter])
                i = 0
                j = 0
                while (i < hidden_word_rem) and (j < guess_rem):
                    result[min(guess_dict[letter])] = letter
                    i += 1
                    j += 1

        return (False, result)

'''
DESC: checks if a user's guess is valid and matches the hidden word. See below for validity checks. Note: this function does not
track guess count.
PARAMS: user's guess (guess), hidden word (hidden_word), dictionary of valid guesses and results in current game (guessed_words)
RETURNS: (error_code, ["-", "-", "-", "-", "-"]), where:
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
'''
def wordle(guess, hidden_word, guessed_words):
    # [check guess validity]
    # guess is more than 5 characters
    if len(guess) > 5:
        return (2, ["-", "-", "-", "-", "-"])
    # guess is less than 5 characters
    if len(guess) < 5:
        return (3, ["-", "-", "-", "-", "-"])
    # guess contains invalid characters
    for character in guess:
        if not character.isalpha():
            return (4, ["-", "-", "-", "-", "-"])
    # convert guess to all lowercase
    guess = guess.lower()
    # guess is not a real word
    #TODO: implement a way to check if word is in the dictionary
    # guess has been tried already in the current game
    if guess in guessed_words:
        return (6, guessed_words[guess])
    # guess has NOT been tried already in the current game
    else:
        # guess is valid
        # [compare guess against hidden_word]
        compare_result = wordle_helper(guess, hidden_word)
        # guess is correct
        if compare_result[0]:
            return (0, compare_result[1])
        # guess is incorrect
        else:
            # add guess and result to guessed_words
            guessed_words.update({guess : compare_result[1]})
            return (1, compare_result[1])

if __name__ == "__main__":
    # wordle() test loop
    hidden_word = "chose"
    guessed_words = dict()
    word_list = set()

    print("Running wordle()...")
    guess = input("Enter a guess (-1 to exit)...\n")
    while (guess != "-1"):
        wordle_result = wordle(guess, hidden_word, guessed_words)
        if wordle_result[0] == 0:
            print("wordle(): guess is valid and CORRECT", wordle_result[1])
        elif wordle_result[0] == 1:
            print("wordle(): guess is valid but INCORRECT", wordle_result[1])
        elif wordle_result[0] == 2:
            print("wordle(): guess is TOO LONG")
        elif wordle_result[0] == 3:
            print("wordle(): guess is TOO SHORT")
        elif wordle_result[0] == 4:
            print("wordle(): guess contains INVALID CHARACTERS")
        elif wordle_result[0] == 5:
            print("wordle(): guess is NOT A REAL WORD")
        elif wordle_result[0] == 6:
            print("wordle(): guess has been ALREADY GUESSED", wordle_result[1])
        else:
            print("wordle(): ERROR")
        guess = input("Enter another guess...\n")
