class Invoice(object):
    def __init__(self, intervals):
        self.__categories = [tag for interval in intervals for tag in
                interval.get_tags()]

    def categories(self):
        return self.__categories

class LineItem(object):
    def __init__(self, day, duration, rate):
        self.__day = day.date()

    @property
    def date(self):
        return self.__day.strftime('%B %d, %Y')
