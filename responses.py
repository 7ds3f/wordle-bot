def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == "!help":
        return "I am a discord bot dedicated to wordle. Currently under production!"