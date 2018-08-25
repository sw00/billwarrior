import configparser
import os

INI_FILE_PATH = os.path.join(
    os.getenv("HOME"), ".config", "billwarrior", "billwarrior.ini"
)


class BillWarriorConfig(object):
    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read(INI_FILE_PATH)

        with open(INI_FILE_PATH, "r") as f:
            parser.read_string(f.read())

        self.__categories = set(
            [option.split(".")[0] for option in parser.options("categories")]
        )

    @property
    def categories(self):
        return self.__categories
