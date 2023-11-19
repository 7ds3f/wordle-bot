import json

from .wordle_config import WordleConfig

# Opens and loads the database that contains all the square letter emojis.
__file = open(WordleConfig.square_letter_emojis())
__data = json.load(__file)

blank_square: str = __data['blank_square']
'The blank square emoji.'
black_squares: dict[str, str] = __data['black_squares']
'All the black square emojis.'
gray_squares: dict[str, str] = __data['gray_squares']
'All the gray square emojis.'
yellow_squares: dict[str, str] = __data['yellow_squares']
'All the yellow square emojis.'
green_squares: dict[str, str] = __data['green_squares']
'All the green square emojis.'

__file.close()
    