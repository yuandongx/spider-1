import os
from pathlib import Path


def load_config():
    """
    Load configuration from environment variables.
    """
    config = {}
    _env = Path(__file__).parent.joinpath('.environment')
    if not _env.exists():
        raise FileNotFoundError(f"Configuration file '{_env}' not found.")
    with _env.open('r', encoding='utf-8') as file:
        lines = file.readline()
        for line in lines:
            key, value = line.strip().split('=', 1)
            config[key] = value
            os.environ[key] = value

    return config

if __name__ == '__main__':
    pass