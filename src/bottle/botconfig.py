import config as cfg
import os

from dotenv import load_dotenv

config = cfg.has_required_items(
    path = cfg.path,
    file = 'bot.ini',
    settings = {
        'DEFAULT': [
            'EnableCommandPrefix',
            'CommandPrefix'
        ],
        'TOKEN': [
            'Path',
            'File',
            'Name'
        ]
    }
)
'The configuration for BOTTLE.'

default_config = config['DEFAULT']
'The default configuration for BOTTLE.'

token_config = config['TOKEN']
'The token configuration for BOTTLE.'

__target_file = cfg.get_target_file(
    path = token_config['Path'],
    file = token_config['File']
)
load_dotenv(__target_file)
TOKEN = os.getenv(token_config['Name'])
'The token key for BOTTLE.'

class Config:
    @staticmethod
    def enable_command_prefix() -> bool:
        """
        Returns the 'EnableCommandPrefix' key value.
        """
        return default_config.getboolean('EnableCommandPrefix')
    
    @staticmethod
    def command_prefix() -> str:
        """
        Returns the 'CommandPrefix' key value.
        """
        return default_config['CommandPrefix']