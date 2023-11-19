import configparser
import enchant

from wordle import WordleConfig

class GameConfig:
    NAME_KEY = 'Name'
    'The name key.'
    DICT_KEY = 'Dictionary'
    'The dictionary key.'
    ATTEMPT_KEY = 'MaxAttempts'
    'The max attempts key.'
    VALID_KEY = 'ValidWordsOnly'
    'The valid words only key.'
    LANG_KEY = 'Language'
    'The language key.'
    
    def __init__(self, mode: str) -> None:
        self.mode = mode
        self.config = self.get_config()
        self.dictionary = self.get_dictionary()
        self.attempts = self.get_attempts()
        self.valid_only = self.get_validity()
        self.language = self.get_language()
    
    def get_config(self) -> configparser.SectionProxy:
        """
        Gets the default configuration for this gamemode.
        """
        return WordleConfig.config[f'Gamemode.{self.mode}']
    
    def get_dictionary(self) -> list[str]:
        """
        Gets the default dictionary for this gamemode.
        """
        dict_config = WordleConfig.dictionary_config
        dict_path = self.config[GameConfig.DICT_KEY]
        
        with open(dict_config[dict_path], 'r', encoding='utf-8') as file:
            word_pool = file.readlines()
            file.close()
            return word_pool
    
    def get_attempts(self) -> int:
        """
        Gets the default maximum attempts for this gamemode.
        """
        return self.config.getint(GameConfig.ATTEMPT_KEY)
    
    def get_validity(self) -> bool:
        """
        Gets whether only valid words are allowed for this gamemode.
        """
        return self.config.getboolean(GameConfig.VALID_KEY)
    
    def get_language(self) -> enchant.Dict:
        """
        Gets the default language for this gamemode.
        """
        return enchant.Dict(self.config[GameConfig.LANG_KEY])
        