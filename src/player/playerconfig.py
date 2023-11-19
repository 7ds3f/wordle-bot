import config as cfg

config = cfg.has_required_items(
    path = cfg.path,
    file = 'player.ini',
    settings = {
        'DEFAULT': [
            'Path',
            'Template'
        ]
    }
)
'The configuration for a player.'

default_config = config['DEFAULT']
'The default configuration for a Player.'

class Config:
    @staticmethod
    def path() -> str:
        """
        Returns the 'Path' key value.
        """
        return default_config['Path']
    
    @staticmethod
    def template() -> str:
        """
        Returns the 'Template' key value.
        """
        return default_config['Template']