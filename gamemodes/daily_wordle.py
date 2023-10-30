# same as Daily_wordle except selects a word based on what day it is
import enchant
import discord
import wordle

async def run(ctx, interaction, users):

    # check if the guess appears in the same channel as the game
    # check if the guess is sent by the user who started the game
    def check_guess(message):
        # if game was started via the !newgame menu
        if interaction != None:
            if message.channel.id == interaction.channel.id and message.author == interaction.user:
                return message
        # if game was started via the !sw command
        elif message.channel.id == ctx.channel.id and message.author == ctx.author:
            return message

    #embed for game cancellation
    cancel_embed=discord.Embed(
        title="Game Cancelled",
        color=discord.Color.red()
    )

    # embed for game start
    async def send_start_embed(ctx, user):
        embed=discord.Embed(
            title="Daily Wordle",
            color=discord.Color.blurple(),
            description="Type a guess, " + user.mention + "!"
        )
        await ctx.send(embed=embed)

    # embed for ongoing game status
    async def send_game_embed(ctx, guessed_words, guesses_rem, guess, guess_obj):
        embed=discord.Embed(
            title="Daily Wordle",
            color=discord.Color.blurple(),
            description="Incorrect. Type another guess!"
        )
        for guess in guessed_words.keys():
            embed.add_field(name="", value=guessed_words[guess][1], inline=False)
        embed.add_field(name="Guess #", value=str(6 - guesses_rem) + "/6", inline=False)
        await ctx.send(embed=embed, reference=guess_obj)

    # embed for game win
    async def send_win_embed(ctx, guessed_words, guesses_rem, guess, guess_obj):
        embed=discord.Embed(
            title="Daily Wordle",
            color=discord.Color.green(),
            description="You Won!"
        )
        for guess in guessed_words.keys():
            embed.add_field(name="", value=guessed_words[guess][1], inline=False)
        embed.add_field(name="Guesses Taken", value=str(6 - guesses_rem) + "/6", inline=False)
        await ctx.send(embed=embed, reference=guess_obj)

    # embed for game lose
    async def send_lose_embed(ctx, guessed_words, guess, guess_obj, hidden_word):
        embed=discord.Embed(
            title="Daily Wordle",
            color=discord.Color.red(),
            description="Game Over!"
        )
        for guess in guessed_words.keys():
            embed.add_field(name="", value=guessed_words[guess][1], inline=False)
        embed.add_field(name="Out of Guesses!", value="Word was " + hidden_word.upper(), inline=False)
        await ctx.send(embed=embed, reference=guess_obj)
    
    # embed for invalid guess
    async def send_invalid_embed(ctx, wordle_result, guess_obj):
        embed=discord.Embed(
            title="Invalid Guess!",
            color=discord.Color.yellow(),
            description="Type another guess!"
        )
        if wordle_result[0] == 2:
            embed.add_field(name="Reason", value="Guess is TOO LONG")
        elif wordle_result[0] == 3:
            embed.add_field(name="Reason", value="Guess is TOO SHORT")
        elif wordle_result[0] == 4:
            embed.add_field(name="Reason", value="Guess is contains INVALID CHARACTERS")
        elif wordle_result[0] == 5:
            embed.add_field(name="Reason", value="Guess is NOT A REAL WORD")
        elif wordle_result[0] == 6:
            embed.add_field(name="Reason", value="Guess has ALREADY BEEN TRIED")
        await ctx.send(embed=embed, reference=guess_obj)
    
    # load the dictionary and hidden word for the current game
    d = enchant.Dict("en_US")
    hidden_word = wordle.random_word(d)
    guessed_words = dict()

    # [start Daily Wordle Game]
    if interaction != None:
        print(f"[INFO] {interaction.user} started a new Wordle game (mode=Daily Wordle, hidden_word={hidden_word})")
        await send_start_embed(ctx, interaction.user)
    else:
        print(f"[INFO] {ctx.author} started a new Wordle game (mode=Daily Wordle, hidden_word={hidden_word})")
        await send_start_embed(ctx, ctx.author)

    guesses_rem = 6
    while guesses_rem > 0:
        guess = await ctx.bot.wait_for("message", check=check_guess)
        # ignore empty guesses and guesses that start with "!", unless it's the quit command ("!q")
        while guess.content == "" or guess.content[0] == "!":
            if guess.content == "!q":
                print(f"[INFO] {ctx.author} quit their Wordle game (mode=Daily Wordle, hidden_word={hidden_word})")
                await ctx.send(embed=cancel_embed, reference=guess)
                users.remove(ctx.author)
                return
            guess = await ctx.bot.wait_for("message", check=check_guess)
        # check the guess with the wordle function
        wordle_result = wordle.wordle(guess.content, hidden_word, guessed_words, d)
        if wordle_result[0] == 0:
            guesses_rem -= 1
            print(f"[INFO] {ctx.author} won their Wordle game (mode=Daily Wordle, hidden_word={hidden_word})")
            await send_win_embed(ctx, guessed_words, guesses_rem, guess.content, guess)
            users.remove(ctx.author)
            return
        else:
            if wordle_result[0] == 1:
                guesses_rem -= 1
                if guesses_rem != 0:
                    await send_game_embed(ctx, guessed_words, guesses_rem, guess.content, guess)
            else:
                await send_invalid_embed(ctx, wordle_result, guess)
    print(f"[INFO] {ctx.author} lost their Wordle game (mode=Daily Wordle, hidden_word={hidden_word})")
    await send_lose_embed(ctx, guessed_words, guesses_rem, guess, hidden_word)
    users.remove(ctx.author)
    return