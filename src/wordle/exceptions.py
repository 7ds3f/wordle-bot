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