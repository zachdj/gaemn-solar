""" API for accessing user configuration settings in the `config.json` file """

import json

_config = dict()
config_file_read = False

try:
    with open('../config.json', 'r') as config_file:
        _config = json.load(config_file)
        config_file_read = True
except FileNotFoundError:
    print('WARNING: Could not read "config.json" file.')


def get(key):
    if key in _config:
        return _config[key]
    else:
        raise KeyNotFoundException('The item "%s" was not found in the configuration settings.  '
                                   'Please check the config.json file.' % key)


def to_dict():
    return _config.copy()


class KeyNotFoundException(Exception):
    pass
