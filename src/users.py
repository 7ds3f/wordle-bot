from discord import Member

class User:
    """
    A user is a Discord member in a guild (server). Each user has their own statistics
    tracking the results from Wordle games.
    """
    def __init__(self, user:Member):
        """
        Constructs a user.

        Args:
            user (Member): A Discord member.
        """

        self.user = user
        'The Discord member of a user.'
        self.wins = 0
        'The number of games a user has won.'
        self.losses = 0
        'The number of games a user has lost.'
        self.forfeits = 0
        'The number of games a user has quit.'
        self.grays_generated = 0
        'The number of gray tiles a user has generated from playing.'
        self.yellows_generated = 0
        'The number of yellow tiles a user has generated from playing.'
        self.greens_generated = 0
        'The number of greens tiles a user has generated from playing.'
        self.standard_fastest_guess = -1
        'The fastest time it took a user to guess the correct word in a standard Wordle game.'
        self.in_game = False
        'Whether a user is currently playing a game.'