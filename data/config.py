"""
Module for loading the app configuration
"""
import json


config = None


def get_config():
    """
    Gets the application configuration from the config.json file
    :return: dict with the config variables as string keys
    """
    global config
    if config is None:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

    return config
