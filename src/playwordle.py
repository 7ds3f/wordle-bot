import enchant
import random
import textwrap

from wordle import *
from color import Color

if __name__ == "__main__":
    # You can change the game rules here.
    hidden_word: str = random.choice(GamemodeConfig.dictionary('Standard'))
    max_attempts: int = 6
    language: enchant.Dict | None = None

    # Styles
    bold = Color.BOLD
    blue = Color.Foreground.LIGHT_BLUE
    red = Color.Foreground.LIGHT_RED
    green = Color.Foreground.LIME
    yellow = Color.Foreground.GOLD
    gray = Color.Foreground.LIGHT_GRAY

    quit_command: str = "/q"
    game = Wordle(
        hidden_word=hidden_word,
        max_attempts=max_attempts,
        language=language
    )

    # Printing da rules.
    border = Color.styletext(f"{chr(160)}" * 55, Color.STRIKETHROUGH)
    print(textwrap.dedent(f"""
        {border}
        {Color.styletext("BOTTLE", bold, blue)}

        {Color.styletext("How to play?", bold)}
        You have {game.max_attempts} attempts to guess the word.
        
        {Color.styletext("Green", green)} indicates that the letter is in the correct spot.
        {Color.styletext("Yellow", yellow)} indicates that the letter is in the wrong spot.
        {Color.styletext("Gray", gray)} indicates that the letter is not in the word.
        {border}
        
        Guess a {len(game.hidden_word)}-letter word to start:
    """))

    # This is where the game happens.
    while not game.is_terminated():
        user_input = input("")
        if user_input == quit_command:
            Color.print("You have quit your game!", red)
            game.terminate()
            exit(0)

        try:
            sq_letters = game.make_guess(user_input)
        except InvalidGuess as e:
            Color.print(e.__str__(), red)
        else:
            # Prints the states of each letter of the guess.
            for letter in sq_letters:
                print(letter.colored_text(), end="")
            print(f"\t({game.remaining_attempts()} attempts remaining)")

            # Prints all the letter states of this game.
            green_letters = ""
            yellow_letters = ""
            gray_letters = ""
            black_letters = ""

            for letter in game.letters_used.values():
                match letter.state:
                    case LetterState.GREEN:
                        green_letters += letter.value + " "
                    case LetterState.YELLOW:
                        yellow_letters += letter.value + " "
                    case LetterState.GRAY:
                        gray_letters += letter.value + " "
                    case LetterState.BLACK:
                        black_letters += letter.value + " "

            maxlength = max(len(green_letters), len(yellow_letters), len(gray_letters), len(black_letters))
            border = f"{chr(160)}" * (maxlength + 10)
            border = Color.styletext(border, Color.STRIKETHROUGH)

            Color.print(border)
            Color.print(f"Green :   {green_letters}", green)
            Color.print(f"Yellow:   {yellow_letters}", yellow)
            Color.print(f"Gray  :   {gray_letters}", gray)
            Color.print(f"Unused:   {black_letters}")
            Color.print(border + "\n")
    else:
        if game.has_guessed_word:
            Color.print("You have guessed the word!", green)
        else:
            hidden_word = Color.styletext(game.hidden_word, gray)
            Color.print(f"The word was {hidden_word}", red)
