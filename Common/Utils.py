import json
import logging
import os

CURRENT_DIR, CURRENT_FILENAME = os.path.split(__file__)
logging.getLogger().setLevel(logging.INFO)

def string_to_float(value):
    logging.info('string_to_float', value)
    if type(value) == type('str'):
        return float(''.join(
            e for e in unicode(value, 'utf-8') if e.isalnum()))
    else:
        return float(value)


def get_config():
    logging.info('get_config')
    config_path = os.path.join(CURRENT_DIR, '.credentials', 'config.json')
    config = {}
    with open(config_path) as data_file:
        config = json.load(data_file)
    return config
