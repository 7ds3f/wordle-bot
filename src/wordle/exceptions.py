class InvalidGuess(Exception):
    """
    An exception raised for invalid guesses in a Wordle game.
    """
    
    def __init__(self, guess:str, message:str):
        """
        Constructs an invalid guess exception.

        Args:
            guess (str): The guess that caused the exception.
            message (str): The message explaining why the exception was raised.
        """
        
        super().__init__(message)
        
        self.guess = guess
        'The guess that caused the exception.'
        self.message = message
        'The message explaining why the exception was raised.'

class InvalidLetter(Exception):
    """
    An exception raised for invalid Wordle letter.
    """
    
    def __init__(self, letter:str, message:str):
        """
        Constructs an invalid letter exception.

        Args:
            letter (str): The letter that caused the exception.
            message (str): The message explaining why the exception was raised.
        """
        
        super().__init__(message)
        
        self.guess = letter
        'The letter that caused the exception.'
        self.message = message
        'The message explaining why the exception was raised.'