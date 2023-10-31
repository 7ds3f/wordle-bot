'''
Daily Wordle gamemode, interactable through Discord.
'''
import standard_wordle

# starts Daily Wordle game instance
async def run(ctx, interaction, users):

    # check if the guess appears in the same channel as the game
    # check if the guess is sent by the user who started the game
    def check_guess(message):
        # game was started via the !newgame menu
        if interaction != None:
            if message.channel.id == interaction.channel.id and message.author == interaction.user:
                return message
        # game was started via the !sw command
        elif message.channel.id == ctx.channel.id and message.author == ctx.author:
            return message
    
   # start a new Standard Wordle game
    game = standard_wordle.StandardWordle(True)

    # initialize a new reponseSender for the current game
    sender = standard_wordle.StandardWordleResponseSender(ctx, "Daily Wordle")

    # check how the current game a was started
    # game was started via the !newgame menu
    if interaction != None:
        print(f"[INFO] {interaction.user} started a new Wordle game (mode=Daily Wordle, hidden_word={game.get_hidden_word()})")
        await sender.send_start_embed(interaction.user)
    # game was started via the !dw command
    else:
        print(f"[INFO] {ctx.author} started a new Wordle game (mode=Daily Wordle, hidden_word={game.get_hidden_word()})")
        await sender.send_start_embed(ctx.author)

    # continue listening for guesses while the game is active
    while not game.is_terminated():
        guess = await ctx.bot.wait_for("message", check=check_guess)
        # ignore empty guesses and guesses that start with "!", unless it's the quit command ("!q")
        while guess.content == "" or guess.content[0] == "!":
            if guess.content == "!q" or guess.content == "!quit":
                print(f"[INFO] {ctx.author} quit their Wordle game (mode=Daily Wordle, hidden_word={game.get_hidden_word()})")
                await sender.send_cancel_embed(guess)
                users.remove(ctx.author)
                return
            guess = await ctx.bot.wait_for("message", check=check_guess)

        # access wordle response for guess
        wordle_result = game.make_guess(guess.content)

        # guess is correct
        if wordle_result[0] == 0:
            print(f"[INFO] {ctx.author} won their Wordle game (mode=Daily Wordle, hidden_word={game.get_hidden_word()})")
            await sender.send_win_embed(game.get_history(), guess, game.get_guesses_rem())
            users.remove(ctx.author) #remove user from bot's active users list
            return
        # guess is incorrect
        else:
            if wordle_result[0] == 1:
                if not game.is_terminated():
                    await sender.send_game_embed(game.get_history(), guess, game.get_guesses_rem(), game.get_letters())
            else:
                await sender.send_invalid_embed(wordle_result, guess)

    print(f"[INFO] {ctx.author} lost their Wordle game (mode=Daily Wordle, hidden_word={game.get_hidden_word()})")
    await sender.send_lose_embed(game.get_history(), guess, game.get_hidden_word())
    users.remove(ctx.author) #remove user from bot's active users list
    return