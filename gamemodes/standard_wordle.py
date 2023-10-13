import enchant
import wordle

async def run(ctx, interaction, users):

    # check if the guess appears in the same channel as the game
    # check if the guess is sent by the user who started the game
    def check_guess(message):
        # if game was started via the game mode menu
        if interaction != None:
            if message.channel.id == interaction.channel.id and interaction.user == ctx.author:
                return message
        # if game was started via the !sw command
        elif message.channel.id == ctx.channel.id and message.author == ctx.author:
            return message
    
    # load the dictionary and hidden word for the current game
    d = enchant.Dict("en_US")
    hidden_word = wordle.random_word(d)
    guessed_words = dict()

    # [start Standard Wordle Game]
    print(f"[INFO] {ctx.author} started a new Wordle game (mode=Standard Wordle, hidden_word={hidden_word})")
    await ctx.send(f"Standard Wordle | {ctx.author.mention}\n")

    guesses_rem = 6
    while guesses_rem > 0:
        await ctx.send("Enter a guess...")
        guess = await ctx.bot.wait_for("message", check=check_guess)
        #ignore guesses that start with "!", unless it's the quit command ("!q")
        while guess.content[0] == "!":
            if guess.content == "!q":
                print(f"[INFO] {ctx.author} ended their Wordle game (mode=Standard Wordle, hidden_word={hidden_word})")
                await ctx.send(f"Game Cancelled | {ctx.author.mention}")
                users.remove(ctx.author)
                return
            guess = await ctx.bot.wait_for("message", check=check_guess)
        #check the guess with the wordle function
        wordle_result = wordle.wordle(guess.content, hidden_word, guessed_words, d)
        if wordle_result[0] == 0:
            print(f"[INFO] {ctx.author} ended their Wordle game (mode=Standard Wordle, hidden_word={hidden_word})")
            await ctx.send(f"CORRECT! | {wordle_result[1]} | {ctx.author.mention}")
            users.remove(ctx.author)
            return
        else:
            if wordle_result[0] == 1:
                guesses_rem -= 1
                if guesses_rem != 0:
                    await ctx.send(f"Incorrect, try again! | {guesses_rem} guesses remaining | {ctx.author.mention}")
                    await ctx.send(f"{wordle_result[1]}")
            else:
                await ctx.send(f"Invalid Guess! | {guesses_rem} guesses remaining | {ctx.author.mention}")
    print(f"[INFO] {ctx.author} ended their Wordle game (mode=Standard Wordle, hidden_word={hidden_word})")
    await ctx.send(f"Game Over! Word was {hidden_word} | {ctx.author.mention}")
    users.remove(ctx.author)
    return