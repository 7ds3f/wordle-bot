import configparser

# The configuration for a Wordle game.
config = configparser.ConfigParser()
config.read('src/assets/.config/wordle.ini')

def dictionary_config() -> configparser.SectionProxy:
    """
    Returns the dictionary configuration of a Wordle game.
    """
    return config['DICTIONARY']

def emoji_config() -> configparser.SectionProxy:
    """
    Returns the emoji configuration of a Wordle game.
    """
    return config['EMOJI']