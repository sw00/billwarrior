class Invoice(object):
    def __init__(self, intervals):
        self.__categories = [tag for interval in intervals for tag in
                interval.get_tags()]

    def categories(self):
        return self.__categories

class LineItem(object):
    pass


