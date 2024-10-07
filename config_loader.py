import os
import configparser

CONFIG_PATH = './configs/'

def list_configs():
    """Lists all config files in the config directory."""
    configs = [f for f in os.listdir(CONFIG_PATH) if f.endswith('.ini')]
    configs.insert(0, "Exit")  # Add option to exit
    return configs

def load_config(config_name):
    """Loads the configuration settings from a .ini file."""
    config = configparser.ConfigParser()
    config.read(os.path.join(CONFIG_PATH, config_name))
    return config
