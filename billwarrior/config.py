import configparser
import os

INI_FILE_PATH = os.path.join(
    os.getenv("HOME"), ".config", "billwarrior", "billwarrior.ini"
)


class BillWarriorConfig(object):
    def __init__(self):
        self.parser = configparser.ConfigParser()

        with open(INI_FILE_PATH, "r") as f:
            self.parser.read_string(f.read())

        self.__categories = set(
            [option.split(".")[0] for option in self.parser.options("categories")]
        )

    @property
    def categories(self):
        return self.__categories

    def text_for(self, category_name):
        return self.parser["categories"].get("{}.text".format(category_name))

    def rate_for(self, category_name):
        return self.parser["categories"].getfloat("{}.rate".format(category_name))
