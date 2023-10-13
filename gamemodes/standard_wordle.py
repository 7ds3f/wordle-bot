import enchant
import wordle

async def run(ctx):

    def check_guess(message):
        if message.channel.id == ctx.channel.id and message.author == ctx.author:
            return message
    
    d = enchant.Dict("en_US")
    hidden_word = wordle.random_word(d)
    guessed_words = dict()

    print(f"[INFO] {ctx.author} started a new Wordle game (mode=Standard Wordle, hidden_word={hidden_word})")
    await ctx.send(f"Standard Wordle | {ctx.author.mention}\n")

    guesses_rem = 6
    while guesses_rem > 0:
        await ctx.send("Enter a guess...")
        guess = await ctx.bot.wait_for("message", check=check_guess)
        wordle_result = wordle.wordle(guess.content, hidden_word, guessed_words, d)
        if wordle_result[0] == 0:
            await ctx.send(f"CORRECT! | {wordle_result[1]} | {ctx.author.mention}")
            return
        else:
            if wordle_result[0] == 1:
                guesses_rem -= 1
                if guesses_rem != 0:
                    await ctx.send(f"Incorrect, try again! | {guesses_rem} guesses remaining | {ctx.author.mention}")
                    await ctx.send(f"{wordle_result[1]}")
            else:
                await ctx.send(f"Invalid Guess! | {guesses_rem} guesses remaining | {ctx.author.mention}")
    await ctx.send(f"Game Over! Word was {hidden_word} | {ctx.author.mention}")
    return