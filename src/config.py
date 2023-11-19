import configparser

path = 'src/assets/.config'

def has_required_items(
    *,
    path: str,
    file: str,
    settings: dict[str, list[str]]
) -> configparser.ConfigParser:
    target_file = get_target_file(path=path, file=file)
    config = configparser.ConfigParser()
    config.read(target_file)

    for section in settings:
        if section not in config:
            raise ValueError(f'Missing [{section}] in {file}')
        for key in settings[section]:
            if key not in config[section]:
                raise ValueError(f"Missing '{key}' under [{section}] in {file}")
    
    return config

def get_target_file(
    *,
    path: str,
    file: str
) -> str:
    return f'{path}{file}' if path[-1] == '/' else f'{path}/{file}'