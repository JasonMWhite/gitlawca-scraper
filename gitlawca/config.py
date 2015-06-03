from __future__ import unicode_literals
from os import path
import yaml


def config(key):
    filename = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'config.yml')
    with open(filename, 'r') as config_file:
        yaml_file = yaml.load(config_file)
        result = yaml_file[key]
    return result
