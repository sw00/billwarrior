import configparser
import os

INI_FILE_PATH = os.path.join(
    os.getenv("HOME"), ".config", "billwarrior", "billwarrior.ini"
)


class BillWarriorConfig(object):
    def __init__(self):
        parser = configparser.ConfigParser()

        with open(INI_FILE_PATH, 'r') as f:
            parser.read_string(f.read())

        categories = []

        for option in parser.options('categories'):
            categories.append(option.split('.')[0])

        self.__categories = set(categories)


    @property
    def categories(self):
        return self.__categories
