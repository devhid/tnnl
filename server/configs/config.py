"""Parser for loading config file
"""
import configparser
import os.path

from utils.consts import *

def load_configs(config_file, config_section, config_keys):
    """Loads configurations from config file based on given config section and values
    
    Arguments:
        config_file {string} -- configuration section to read
        config_keys {string[]} -- list of keys to read from the section
    
    Returns:
        dict<string, string> -- map containing configuration for given section
    """

    if not os.path.isfile(config_file):
        return None

    config = configparser.ConfigParser()
    config.read(config_file)

    if config_section not in config:
        return None

    for key in config_keys:
        if key not in config[config_section]:
            return None

    return config[config_section]