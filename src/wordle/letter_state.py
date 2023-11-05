from enum import Enum
    
class LetterState(Enum):
    """
    An enum used to represent the state of a Wordle letter.
    """
    
    BLACK = 0
    'Letters that have not been used in a guess yet.'
    
    GRAY = 1
    'Letters that are not in the answer.'
    
    YELLOW = 2
    'Letters that are in the answer, but in the wrong place.'
    
    GREEN = 3
    'Letters that are in the answer and in the right place.'