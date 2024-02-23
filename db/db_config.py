import os

from configparser import ConfigParser

from config import PATH_PROJECT


def config(filename="database.ini", section="postgresql") -> dict:
    config_path = os.path.join(PATH_PROJECT, "db", filename)
    parser = ConfigParser()
    parser.read(config_path)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
