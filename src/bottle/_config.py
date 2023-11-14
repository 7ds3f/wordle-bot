import configparser
import os

from dotenv import load_dotenv

# The configuration for BOTTLE.
config = configparser.ConfigParser()
config.read('src/assets/.config/bot.ini')

# Loads the discord token.
load_dotenv(config['TOKEN']['Path'])
TOKEN = os.getenv(config['TOKEN']['Name'])

# These are needed for the bot to run.
if 'TOKEN' not in config:
    raise ValueError(f'Missing [TOKEN] section in "bot.ini"')
if 'Path' not in config['TOKEN']:
    raise ValueError(f'Missing Path under the [TOKEN] section in "bot.ini"')
if 'Name' not in config['TOKEN']:
    raise ValueError(f'Missing Name under the [TOKEN] section in "bot.ini"')

def default_config() -> configparser.SectionProxy:
    """
    Returns the default configuration of BOTTLE.
    """
    return config['DEFAULT']

def token_config() -> configparser.SectionProxy:
    """
    Returns the token configuration of BOTTLE.
    """
    return config['TOKEN']