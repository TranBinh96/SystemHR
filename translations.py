import configparser
import os

def get_translation(lang='vi'):
    config = configparser.ConfigParser()
    ini_path = os.path.join(os.path.dirname(__file__), 'translations.ini')
    config.read(ini_path, encoding='utf-8')
    if lang in config:
        return dict(config[lang])
    return dict(config['vi'])