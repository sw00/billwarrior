from billwarrior.records import DayEntry


class Invoice(object):
    def __init__(self, intervals, config):
        self.__items = []

        for interval in intervals:
            mapped_tag = [
                interval_tag
                for interval_tag in interval.get_tags()
                if config.category_of(interval_tag)
            ]

            categories = set([config.category_of(tag) for tag in mapped_tag])
            if len(categories) > 1:
                raise ValueError(
                    "Interval has tags belonging to different categories: {}".format(
                        mapped_tag
                    )
                )

            if len(categories) == 0:
                raise ValueError(
                    "Interval doesn't belong to any category: {}".format(interval)
                )

            entries = [DayEntry([interval])]
            current_category = config.category_of(mapped_tag.pop())
            self.__items.append(
                ItemCategory(
                    current_category,
                    entries,
                    config.rate_for(current_category),
                )
            )

    def items(self):
        return self.__items
    
    def __str__(self):
        return '\n'.join([str(item) for item in self.__items])


class ItemCategory(object):
    def __init__(self, tag_name, list_of_day_entries, unit_price):
        self.header = (
            " ".join([x for x in tag_name.split() if not x == ""]).strip().capitalize()
        )
        self.line_items = [
            LineItem(day_entry.date, day_entry.total_duration(), unit_price)
            for day_entry in sorted(list_of_day_entries, key=lambda x: x.date)
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
