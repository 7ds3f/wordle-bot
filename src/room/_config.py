import configparser

# The configuration for a gaming room.
config = configparser.ConfigParser()
config.read('src/assets/.config/room.ini')

def default_config() -> configparser.SectionProxy:
    """
    Returns the default configuration of a room.
    """
    return config['DEFAULT']