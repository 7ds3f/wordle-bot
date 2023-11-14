import enchant
import random
import time
import wordle

from .game import Game, player
from .game_config import GameConfig
    
class Daily(Game):
    """
    This class represents the daily Wordle challenge.
    """
    config = GameConfig('Daily')
    'The default configuration for the daily Wordle challenge.'
    
    def __init__(
        self,
        *,
        player: player.Player,
        language: enchant.Dict | None = None
    ) -> None:
        super().__init__(
            wordle = wordle.Wordle(
                hidden_word = Daily.daily_word(),
                max_attempts = Daily.config.attempts,
                language = (Daily.config.language if language is None else language) if Daily.config.valid_only else language
            ),
            player = player,
            mode = Daily.config.mode
        )
        
    def daily_word() -> str:
        """
        Generates the word of the day.
        """
        seed = time.strftime('%d/%m/%Y')
        rand = random.Random(seed)
        return rand.choice(Daily.config.dictionary)
        
    def rules(self) -> str:
        """
        The rules of the daily Wordle challenge.
        """
        return f"""
                **How to play?**
                You have {self.wordle.max_attempts} attempts to guess the word.

                **Green** indicates that the letter is in the correct spot.
                **Yellow** indicates that the letter is in the wrong spot.
                **Gray** indicates that the letter is not in the word.

                Type a {len(self.wordle.hidden_word)}-letter word to start playing.
                """