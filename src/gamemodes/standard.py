import discord
import random

from wordle import Wordle
from wordle.exceptions import InvalidGuess
from wordle.letter import no_letter

WORD_FILEPATH = "words.txt"

class Standard(Wordle):
    def __init__(self, user):
        with open(WORD_FILEPATH, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            super().__init__("MAKAF", 6, user)
            # super().__init__(random.choice(lines), 6, user)

        empty_word = ""
        for i in range(len(self.hidden_word)):
            empty_word += no_letter
        
        self.game_status = discord.Embed(
            title = "Standard Wordle",
            color = discord.Color.blurple()
        )
        self.game_status.set_author(
            name = self.user.user.display_name,
            icon_url = self.user.user.avatar.url
        )

        for i in range(self.max_attempts):
            self.game_status.add_field(
                name = "",
                value = empty_word,
                inline = False
            )
        
    async def run(self, ctx, channel):
        await self.__display_rules(ctx)
        print(f'[INFO] {self.user.user.name} started a Wordle game (mode=Standard, hidden_word={self.hidden_word})')
        while not self.is_terminated():
            guess = await self.__get_guess(ctx, channel)
            
            try:
                color_codes = self.make_guess(guess)
                self.__update_fields(color_codes)
                await self.__display_game_status(ctx)
                if self.has_guessed_word:
                    print(f'[INFO] {self.user.user.name} has won their game')
                    # TODO: win embed
                    # TODO: update fastest guess
            except InvalidGuess as e:
                # TODO: embed error
                pass

    async def __get_guess(self, ctx, channel) -> str:
        def check_guess(message):
            if message.channel.id == ctx.channel.id and self.user.user == message.author:
                return message
            
        guess = await ctx.bot.wait_for("message", check=check_guess)
        guess = guess.content
        while guess == '' or guess[0] == "!":
            if guess == '!q' or guess == '!quit':
                print(f'[INFO] {self.user.user.name} quit their Wordle game')
                # cancel embed
                self.terminate()
                return
            guess = await ctx.bot.wait_for("message", check=check_guess)
            guess = guess.content
        return guess
        
    async def __display_rules(self, channel):
        embed = discord.Embed(
            title = "Standard Wordle",
            color = discord.Color.blurple(),
            description =
            f"""
            **How to play?**
            You have {self.max_attempts} attempts to guess the word.

            **Green** indicates that the letter is in the correct spot.
            **Yellow** indicates that the letter is in the wrong spot.
            **Gray** indicates that the letter is not in the word.
            
            Type a word to start playing.
            """
        )

        embed.set_author(
            name = self.user.user.display_name,
            icon_url = self.user.user.avatar.url
        )

        await channel.send(embed=embed)

    async def __display_error(self, channel, message:str):
        pass

    async def __display_warning(self, channel, message:str):
        pass

    async def __display_message(self, channel, message:str):
        pass

    async def __display_game_status(self, channel):
        letters_row1 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
        letters_row2 = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
        letters_row3 = ["z", "x", "c", "v", "b", "n", "m"]

        letters_str1 = ""
        letters_str2 = " "
        letters_str3 = "  "

        for letter in letters_row1:
            letters_str1 += self.letters_used[letter].emoji()
        for letter in letters_row2:
            letters_str2 += self.letters_used[letter].emoji()
        for letter in letters_row3:
            letters_str3 += self.letters_used[letter].emoji()

        if self.attempt_number == 1:
            self.game_status.add_field(name="", value=letters_str1, inline=False)
            self.game_status.add_field(name="", value=letters_str2, inline=False)
            self.game_status.add_field(name="", value=letters_str3, inline=False)
        else:
            self.game_status.set_field_at(index=self.max_attempts, name="", value=letters_str1, inline=False)
            self.game_status.set_field_at(index=self.max_attempts+1, name="", value=letters_str2, inline=False)
            self.game_status.set_field_at(index=self.max_attempts+2, name="", value=letters_str3, inline=False)
        await channel.send(embed=self.game_status)

    def __update_fields(self, guess):
        color_codes = ""
        for letter in guess:
            color_codes += letter.emoji()

        index = self.attempt_number - 1
        self.game_status.set_field_at(
            index = index,
            name = "",
            value = color_codes,
            inline = False
        )
