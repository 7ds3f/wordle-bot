import enchant
import random
import wordle

from .game import Game, player
from .game_config import GameConfig
    
class Standard(Game):
    """
    This class represents a standard Wordle game.
    """
    config = GameConfig('Standard')
    'The default configuration for a standard Wordle game.'
    
    def __init__(
        self,
        *,
        player: player.Player,
        language: enchant.Dict | None = None
    ) -> None:
        super().__init__(
            wordle = wordle.Wordle(
                hidden_word = Standard.random_word(),
                max_attempts = Standard.config.attempts,
                language = (Standard.config.language if language is None else language) if Standard.config.valid_only else language
            ),
            player = player,
            mode = Standard.config.mode
        )
        
    def random_word() -> str:
        """
        Generates a random word for a game.
        """
        return random.choice(Standard.config.dictionary)
    
    def rules(self) -> str:
        """
        The rules of a standard Wordle game.
        """
        return f"""
                **How to play?**
                You have {self.wordle.max_attempts} attempts to guess the word.

                **Green** indicates that the letter is in the correct spot.
                **Yellow** indicates that the letter is in the wrong spot.
                **Gray** indicates that the letter is not in the word.

                Type a {len(self.wordle.hidden_word)}-letter word to start playing.
                """