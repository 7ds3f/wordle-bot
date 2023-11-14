import discord
import graphics
import time
import wordle
import player

from abc import abstractmethod

_NAME_KEY = 'Name'
_DICT_KEY = 'Dictionary'
_ATTEMPT_KEY = 'MaxAttempts'

class Game:
    """
    This an extension to the Wordle game. It allows for the creation of new Wordle variants.
    There can only be one player playing a game instance. These games are timed to elevate
    a competitive environment.
    
    The game class also adds extra functionality that the Wordle class does not offer. And
    that is explicitly stating whether the player has won, lost, or forfeited the game.
    """
    def __init__(
        self,
        *,
        wordle: wordle.Wordle,
        player: player.Player,
        mode: str
    ) -> None:
        """
        Constructs some kind of Wordle game for the given player.
        """
        self.wordle = wordle
        self.player = player
        self.player.in_game = self
        self.mode = mode
        
        self.start_time: float = time.time()
        self.end_time: float | None = None
        
        self.game_embed = self.create_game_embed()
        self.embeds = [self.game_embed]
        
    @abstractmethod
    def rules(self) -> str:
        """
        These are the rules for this Wordle game. Different types of Wordle games may have
        different rules.
        """
        pass
    
    async def display_rules(self) -> None:
        """
        Displays the rules in an embed, and sends it to Discord.
        """
        await graphics.display_msg_embed(
            obj = self.player.room,
            title = self.mode,
            message = self.rules(),
            color = discord.Color.blurple()
        )
        
    async def run(self, interaction: discord.Interaction) -> None:
        """
        Runs the game until the player has ran out of attempts, has guess the word, or has
        forfeited.
        """
        print(f'{self.player.user} started a Wordle game (mode:{self.mode}, hidden_word={self.wordle.hidden_word})')
        
        # Always display the rules before starting the game
        # Afterwards, we wait for a guess from the player.
        await self.display_rules()
        while not self.wordle.is_terminated():
            guess = await self.wait_for_guess(interaction)
            await self.make_guess(guess)
            
    async def wait_for_guess(self, interaction: discord.Interaction) -> str:
        """
        Waits for a guess from the player. After they have made a guess, return the guess
        in the form of a string.
        """
        def check_guess(message: discord.Message) -> discord.Message | None:
            if message.channel.id == self.player.room.id and message.author == self.player.user:
                return message
        
        guess: discord.Message = await interaction.client.wait_for('message', check=check_guess)
        if not self.wordle.is_terminated():
            await guess.delete()
            return guess.content
        
    async def make_guess(self, guess: str) -> None:
        """
        Simulates the standard Wordle game by making a guess. Warns the player if they
        provided with a bad guess. This does not use up an attempt.
        """
        try:
            squares = self.wordle.make_guess(guess)
            if squares is not None:
                await self.update(squares)
                await self.player.room.send(embeds=self.embeds)
        except wordle.InvalidGuess as e:
            await graphics.display_msg_embed(
                obj = self.player.room,
                title = 'Invalid Guess',
                message = e.message,
                color = discord.Color.yellow()
            )
            
    async def update(self, squares: list[wordle.SquareLetter]) -> None:
        """
        Updates the state of this game. Mainly, it updates the UI or embed of this game.
        The game is updated after every guess made.
        """
        emojis = ''.join(letter.emoji() for letter in squares)
        self.game_embed.set_field_at(
            index = self.wordle.attempt_number - 1,
            name = '',
            value = emojis,
            inline = False
        )
        
        if self.wordle.is_terminated():
            self.game_embed.color = discord.Color.green() if self.has_won() else discord.Color.red()
            for _ in range(3):
                self.game_embed.remove_field(self.wordle.max_attempts)
        else:
            keyboard = self.create_keyboard()
            for i in range(3):
                self.game_embed.set_field_at(
                    index = self.wordle.max_attempts + i,
                    name = '',
                    value = keyboard[i],
                    inline = False
                )
    
    def create_game_embed(self, color: discord.Color = discord.Color.yellow()) -> discord.Embed:
        """
        Creates a blank game state of this Wordle game. This is updated after every guess
        made.
        """
        blank_word = wordle.SquareLetter.blank_square * len(self.wordle.hidden_word)
        embed = discord.Embed(
            title = self.mode,
            color = color
        )
        embed.set_author(
            name = self.player.user.display_name,
            icon_url = self.player.user.avatar.url
        )
        
        [embed.add_field(
            name = '',
            value = blank_word,
            inline = False
        ) for _ in range(self.wordle.max_attempts)]
        
        keyboard = self.create_keyboard()
        [embed.add_field(
            name = '',
            value = keys,
            inline = False
        ) for keys in keyboard]
        return embed
    
    def create_keyboard(self) -> list[str]:
        """
        Creates a keyboard representation of all the letters used and their states. This
        keyboard shows the player what letters they should use, letters they should try,
        to use, and letters they should avoid.
        """
        qwerty_keyboard = [
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
            ["z", "x", "c", "v", "b", "n", "m"]
        ]
        return [''.join(self.wordle.letters_used[letter].emoji() for letter in keys) for keys in qwerty_keyboard]
    
    def elapsed_time(self) -> float:
        """
        The time it has elapsed since the start of the game. This is usually used to measure
        the time it took to end the game. However, if the game has not ended yet, it will
        return the time it has been alive.
        """
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time
    
    def terminate(self) -> None:
        """
        Terminates the game. Winning, losing, or forfeiting will elicit termination of the
        game.
        """
        self.wordle.terminate()
        self.player.in_game = None
        
    def has_won(self) -> bool:
        """
        Returns whether the player has won.
        """
        return self.wordle.has_guessed_word
    
    def has_lost(self) -> bool:
        """
        Returns whether the player has lost.
        """
        return self.wordle.has_guessed_word is False and self.wordle.attempt_number == self.wordle.max_attempts
    
    def has_forfeited(self) -> bool:
        """
        Returns whether the player has forfeited.
        """
        return self.wordle.has_guessed_word is False and self.wordle.attempt_number < self.wordle.max_attempts
        
    