class Invoice(object):
    def __init__(self, intervals):
        self.__categories = [
            tag for interval in intervals for tag in interval.get_tags()
        ]

    def categories(self):
        return self.__categories


class ItemCategory(object):
    def __init__(self, tag_name, set_of_day_entries, unit_price):
        self.header = ' '.join([x for x in tag_name.split() if not x =='']).strip().capitalize()
        self.__line_items = [
            LineItem(day_entry.date, day_entry.total_duration(), unit_price) for day_entry in
            set_of_day_entries
        ]

    def __str__(self):
        return "".join(
            [
                "\\feetype{%s}\n" % self.header,
                "".join(["%s\n" % item for item in self.line_items]),
                "\\subtotal\n",
                "%------------------------------------------------",
            ]
        )


class LineItem(object):
    def __init__(self, day, duration, unit_price):
        self.__day = day
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
