import configparser

# The configuration for a Player.
config = configparser.ConfigParser()
config.read('src/assets/.config/player.ini')

# These are needed for the bot to run.
if 'DEFAULT' not in config:
    raise ValueError(f'Missing [DEFAULT] section in "player.ini"')
if 'StatisticsTemplate' not in config['DEFAULT']:
    raise ValueError(f'Missing StatisticsTemplate under the [DEFAULT] section in "player.ini"')
if 'StatisticsFolder' not in config['DEFAULT']:
    raise ValueError(f'Missing StatisticsFolder under the [DEFAULT] section in "player.ini"')

def default_config() -> configparser.SectionProxy:
    """
    Returns the default configuration for a Player.
    """
    return config['DEFAULT']