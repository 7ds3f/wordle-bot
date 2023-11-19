import configparser

class WordleConfig:
    @staticmethod
    def __get_config() -> configparser.ConfigParser:
        file = 'wordle.ini'
        config = configparser.ConfigParser()
        config.read(f'src/assets/.config/{file}')

        if 'DICTIONARY' not in config:
            raise ValueError(f'Missing [DICTIONARY] section in {file}')
        if 'FiveLetter' not in config['DICTIONARY']:
            return ValueError(f'Missing "FiveLetter" under the [DICTIONARY] section in {file}')
        if 'Feudle' not in config['DICTIONARY']:
            return ValueError(f'Missing "Feudle" under the [DICTIONARY] section in {file}')

        if 'EMOJI' not in config:
            raise ValueError(f'Missing [DICTIONARY] section in {file}')
        if 'SquareLetters' not in config['EMOJI']:
            return ValueError(f'Missing "SquareLetters" under the [EMOJI] section in {file}')
        return config
    
    config = __get_config()
    'The configuration for a Wordle game'

    dictionary_config = config['DICTIONARY']
    'The dictionary configuration for a Wordle game.'

    emoji_config = config['EMOJI']
    'The emoji configuration for a Wordle game.'

    def five_letter_words() -> str:
        return WordleConfig.dictionary_config['FiveLetter']
    
    def feudle_words() -> str:
        return WordleConfig.dictionary_config['Feudle']
    
    def square_letter_emojis() -> str:
        return WordleConfig.emoji_config['SquareLetters']