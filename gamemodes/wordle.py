'''
Wordle algorithm + random word generation functions.
'''

import enchant
import random
import string
import time
import linecache

# dictionaries for custom emoji letter display
gray_letters_dict = {
    "a": "<:a_gray:1162435739192148038>",
    "b": "<:b_gray:1162437701723750574>",
    "c": "<:c_gray:1162437702990446744>",
    "d": "<:d_gray:1162437706807267390>",
    "e": "<:e_gray:1162437709172846615>",
    "f": "<:f_gray:1162437711685226626>",
    "g": "<:g_gray:1162437714201808896>",
    "h": "<:h_gray:1162437716240240660>",
    "i": "<:i_gray:1162437718345777244>",
    "j": "<:j_gray:1162437719461482687>",
    "k": "<:k_gray:1162437720539402240>",
    "l": "<:l_gray:1162437721499910376>",
    "m": "<:m_gray:1162437723223773286>",
    "n": "<:n_gray:1162437726533058570>",
    "o": "<:o_gray:1162437867491053689>",
    "p": "<:p_gray:1162437901334876250>",
    "q": "<:q_gray:1162437730114998312>",
    "r": "<:r_gray:1162437939083624548>",
    "s": "<:s_gray:1162437734636470464>",
    "t": "<:t_gray:1162438000190427277>",
    "u": "<:u_gray:1162437737371144322>",
    "v": "<:v_gray:1162438118142644294>",
    "w": "<:w_gray:1162438154549219328>",
    "x": "<:x_gray:1162437740596580482>",
    "y": "<:y_gray:1162438311814631492>",
    "z": "<:z_gray:1162438313370730546>"
}
yellow_green_letters_dict = {
    "a": "<:a_yellow:1162452541783691456>",
    "b": "<:b_yellow:1162452544702914580>",
    "c": "<:c_yellow:1162452547391459538>",
    "d": "<:d_yellow:1162452550558167152>",
    "e": "<:e_yellow:1162452553385123870>",
    "f": "<:f_yellow:1162452554727297044>",
    "g": "<:g_yellow:1162452555968815278>",
    "h": "<:h_yellow:1162452593780465705>",
    "i": "<:i_yellow:1162452595428827238>",
    "j": "<:j_yellow:1162452597349826851>",
    "k": "<:k_yellow:1162452598410973284>",
    "l": "<:l_yellow:1162452600965308537>",
    "m": "<:m_yellow:1162452605071544340>",
    "n": "<:n_yellow:1162452649648590939>",
    "o": "<:o_yellow:1162452651787690065>",
    "p": "<:p_yellow:1162452653645758564>",
    "q": "<:q_yellow:1162452655440920626>",
    "r": "<:r_yellow:1162452657638740090>",
    "s": "<:s_yellow:1162452660562182204>",
    "t": "<:t_yellow:1162452755315703891>",
    "u": "<:u_yellow:1162452756813066280>",
    "v": "<:v_yellow:1162452758549499927>",
    "w": "<:w_yellow:1162452761166761994>",
    "x": "<:x_yellow:1162452764144701520>",
    "y": "<:y_yellow:1162497511307608076>",
    "z": "<:z_yellow:1162497513140527124>",
    "A": "<:a_green:1162498445790171176>",
    "B": "<:b_green:1162498447715352586>",
    "C": "<:c_green:1162498448600334376>",
    "D": "<:d_green:1162498449581817916>",
    "E": "<:e_green:1162498450559086652>",
    "F": "<:f_green:1162498451850936412>",
    "G": "<:g_green:1162498452824019127>",
    "H": "<:h_green:1162498487515107339>",
    "I": "<:i_green:1162498489025036360>",
    "J": "<:j_green:1162498490216235038>",
    "K": "<:k_green:1162498490853765221>",
    "L": "<:l_green:1162498492984459294>",
    "M": "<:m_green:1162498493991092244>",
    "N": "<:n_green:1162498538463314073>",
    "O": "<:o_green:1162498539499290824>",
    "P": "<:p_green:1162498540711456871>",
    "Q": "<:q_green:1162498542246559824>",
    "R": "<:r_green:1162498543496474654>",
    "S": "<:s_green:1162498545094512713>",
    "T": "<:t_green:1162498568460972082>",
    "U": "<:u_green:1162498569308213268>",
    "V": "<:v_green:1162498570759454730>",
    "W": "<:w_green:1162498571908677682>",
    "X": "<:x_green:1162498573561237594>",
    "Y": "<:y_green:1162498575016677510>",
    "Z": "<:z_green:1162498576283357184>"
}

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
def wordle_helper(guess, hidden_word):
    guess = guess.lower()
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

PARAMS: guess - user's guess
        hidden_word - hidden word
        guessed_words - dictionary of valid guesses and results in current game
dictionary of valid words (d)

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
def wordle(guess, hidden_word, guessed_words, d):
    # [check guess validity]
    # guess is more than 5 characters
    if len(guess) > 5:
        return (2, ["-", "-", "-", "-", "-"])
    # guess is less than 5 characters
    if len(guess) < 5:
        return (3, ["-", "-", "-", "-", "-"])
    # guess contains invalid characters
    if not guess.isalpha():
        return (4, ["-", "-", "-", "-", "-"])
    # guess is not a real word
    if not d.check(guess.upper()):
        return (5, ["-", "-", "-", "-", "-"])
    # convert guess to all lowercase
    guess = guess.lower()
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
            # add guess and text-based + discord fomatted result to guessed_words
            guessed_words.update({guess : (compare_result[1], result_format(guess, compare_result))})
            return (0, compare_result[1])
        # guess is incorrect
        else:
            # add guess and text-based + discord fomatted result to guessed_words
            guessed_words.update({guess : (compare_result[1], result_format(guess, compare_result))})
            return (1, compare_result[1])


'''
DESC: Generates a random word by joining 5 random characters and checking if result is a word.
Has an optional mode to track execution time and attempts

PARAMS: d - dictionary of english words
        Mode - enables test mode, false by default

PRINTS: If in test mode: the word, attempts, and execution time in seconds

RETURNS: a random word
'''
#TODO come up with a more efficient way to do this
def random_word(d, Mode=False):
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


'''
DESC: Generates a daily word by using the current date as a seed for the random number generator

PARAMS: d - dictionary of english words
        Mode - enables test mode, false by default
        
PRINTS: If in test mode: the word, attempts, and execution time in seconds

RETURNS: a random word
'''
def daily_word():
    # set the seed
    seed = time.strftime("%d/%m/%Y")
    random.seed(seed)
    # select a random number from 0 to 5756 (number of 5 letter words in the dictionary)
    random_num = random.randint(0, 5756)
    # select the word from sgb-words.txt at the random number
    word = linecache.getline("sgb-words.txt", random_num)
    # remove the newline character from the word
    word = word[:-1]
    return word.upper()


'''
DESC: converts a wordle_result from the wordle() function into colored letters formatted for Discord

PARMS: wordle_result - result from wordle() function

RETURNS: string of colored letters corresponding to wordle_result
'''
def result_format(guess, wordle_result):
    global gray_letters_dict
    global yellow_green_letters_dict
    result = ""
    if wordle_result[1][0] == "-":
            result += (" " + gray_letters_dict[guess[0]])
    else:
        result += (" " + yellow_green_letters_dict[wordle_result[1][0]])
    for index in range(1, len(wordle_result[1])):
        if wordle_result[1][index] == "-":
            result += (" " + gray_letters_dict[guess[index]])
        else:
            result += (" " + yellow_green_letters_dict[wordle_result[1][index]])
    return result

'''
DESC: wordle test function
'''
def main():
    d = enchant.Dict("en_US")
    hidden_word = random_word(d)
    print("Hidden Word:", hidden_word)
    guessed_words = dict()

    guess = input("Enter a guess (-1 to exit)...\n")
    while (guess != "-1"):
        wordle_result = wordle(guess, hidden_word, guessed_words, d)
        if wordle_result[0] == 0:
            print("wordle(): guess is valid and CORRECT", guessed_words[guess])
            print('\nThanks for playing! You got %s in %d (valid & distinct) tries.\n' % (hidden_word, len(guessed_words)))
            break
        elif wordle_result[0] == 1:
            print("wordle(): guess is valid but INCORRECT", guessed_words[guess])
        elif wordle_result[0] == 2:
            print("wordle(): guess is TOO LONG")
        elif wordle_result[0] == 3:
            print("wordle(): guess is TOO SHORT")
        elif wordle_result[0] == 4:
            print("wordle(): guess contains INVALID CHARACTERS")
        elif wordle_result[0] == 5:
            print("wordle(): guess is NOT A REAL WORD")
        elif wordle_result[0] == 6:
            print("wordle(): guess has been ALREADY GUESSED", guessed_words[guess])
        else:
            print("wordle(): ERROR")
        guess = input("Enter another guess...\n")

if __name__ == "__main__":
    print("Running wordle()...")
    main()

