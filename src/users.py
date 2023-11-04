from discord import Member

class User:
    def __init__(self, user:Member):
        self.user = user
        self.wins = 0
        self.losses = 0
        self.forfeits = 0
        self.grays_generated = 0
        self.yellows_generated = 0
        self.greens_generated = 0
        self.fastest_guess = -1
        self.in_game = False