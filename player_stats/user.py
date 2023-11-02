class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.game_wins = 0
        self.game_losses = 0
        self.game_forfeits = 0
        self.gray_tiles = 0
        self.yellow_tiles = 0
        self.green_tiles = 0
        self.fastest_guess = 0
        self.in_game = False

    def get_username(self):
        return self.user_id
    
    def get_wins(self):
        return self.game_wins
    
    def get_losses(self):
        return self.game_losses
    
    def get_forfeits(self):
        return self.game_forfeits
    
    def get_gray_tiles(self):
        return self.gray_tiles
    
    def get_yellow_tiles(self):
        return self.yellow_tiles
    
    def get_green_tiles(self):
        return self.green_tiles
    
    def get_fastest_guess(self):
        return self.fastest_guess
    
    def is_in_game(self):
        return self.in_game

    def add_win(self):
        self.game_wins += 1
    
    def add_loss(self):
        self.game_losses += 1

    def add_forfeit(self):
        self.game_forfeits += 1

    def add_gray_tile(self):
        self.gray_tiles += 1

    def add_yellow_tile(self):
        self.yellow_tiles += 1
    
    def add_green_tile(self):
        self.green_tiles += 1

    def set_in_game(self, in_game):
        self.in_game = in_game

    def update_fastest_guess(self, game_time:float):
        if self.fastest_guess == 0 or game_time < self.fastest_guess:
            self.fastest_guess = game_time

    def __hash__(self) -> int:
        return super(User, self.user_id).__hash__()
    