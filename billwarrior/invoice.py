class Invoice(object):
    def __init__(self, intervals):
        self.__categories = [
            tag for interval in intervals for tag in interval.get_tags()
        ]

    def categories(self):
        return self.__categories


class LineItem(object):
    def __init__(self, day, duration, unit_price):
        self.__day = day.date()
        self.__duration = duration
        self.__unit_price = unit_price

    @property
    def date(self):
        return self.__day.strftime("%B %d, %Y")

    @property
    def duration(self):
        totsec = self.__duration.total_seconds()
        h = totsec // 3600
        m = (totsec % 3600) // 60
        s = (totsec % 3600) % 60

        total = h + (m / 60) + (s / 6000)

        return "{:.2f}".format(total)

    @property
    def unit_price(self):
        return "{:.2f}".format(self.__unit_price)

    def __str__(self):
        return "\\hourrow{%s}{%s}{%s}" % (self.date, self.duration, self.unit_price)
