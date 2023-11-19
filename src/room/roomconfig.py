import config as cfg

config = cfg.has_required_items(
    path = cfg.path,
    file = 'room.ini',
    settings = {
        'DEFAULT': [
            'Private',
            'Invitable',
            'AutoArchiveDuration',
            'SlowmodeDelay'
        ]
    }
)
'The configuration for a room.'

default_config = config['DEFAULT']
'The default configuration for a room.'

class Config:
    @staticmethod
    def private() -> bool:
        """
        Returns the 'Private' key value.
        """
        return default_config.getboolean('Private')
    
    @staticmethod
    def invitable() -> bool:
        """
        Returns the 'Invitable' key value.
        """
        return default_config.getboolean('Invitable')
    
    @staticmethod
    def auto_archive_duration() -> int:
        """
        Returns the 'AutoArchiveDuration' key value.
        """
        return default_config.getint('AutoArchiveDuration')
    
    @staticmethod
    def slowmode_delay() -> int:
        """
        Returns the 'SlowmodeDelay' key value.
        """
        return default_config.getint('SlowmodeDelay')