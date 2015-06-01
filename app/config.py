from __future__ import unicode_literals
import yaml


def config(key):
    with open('../config.yml', 'r') as config_file:
        file = yaml.load(config_file)
        result = file[key]
    return result
