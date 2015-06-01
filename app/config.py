from __future__ import unicode_literals
from os import path
import yaml


def config(key):
    filename = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'config.yml')
    with open(filename, 'r') as config_file:
        file = yaml.load(config_file)
        result = file[key]
    return result
