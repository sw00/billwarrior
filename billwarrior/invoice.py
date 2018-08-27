from datetime import timedelta


class Invoice(object):
    def __init__(self, intervals, config):
        self.__items = []

        intervals_by_category = {}
        for interval in intervals:
            tag_mapping = {tag: config.category_of(tag) for tag in interval.get_tags()}

            interval_categories = set(
                [category for category in tag_mapping.values() if category]
            )

            if len(interval_categories) == 0:
                raise ValueError(
                    "Interval doesn't belong to any category: {}".format(interval)
                )

            if len(interval_categories) > 1:
                raise ValueError(
                    "Interval has tags belonging to different categories: {}".format(
                        [
                            tag
                            for tag in tag_mapping.keys()
                            if tag_mapping.get(tag, None)
                        ]
                    )
                )

            this_category = interval_categories.pop()
            category_entry = intervals_by_category.get(this_category, [])
            category_entry.append(interval)
            intervals_by_category[this_category] = category_entry

        for category, intervals in intervals_by_category.items():
            intervals_by_day = {}

            for interval in intervals:
                day_entry = intervals_by_day.get(interval.get_date().date(), [])
                day_entry.append(interval)
                intervals_by_day[interval.get_date().date()] = day_entry

            self.__items.append(
                ItemCategory(category, intervals_by_day, config.rate_for(category))
            )

    def items(self):
        return self.__items

    def __str__(self):
        return "\n".join([str(item) for item in self.__items])


class ItemCategory(object):
    def __init__(self, tag_name, intervals_by_day, unit_price):
        self.header = (
            " ".join([x for x in tag_name.split() if not x == ""]).strip().capitalize()
        )
        self.line_items = []

        for day, intervals in sorted(intervals_by_day.items(), key=lambda x: x[0]):
            self.line_items.append(LineItem(day, sum([interval.get_duration() for interval
                in intervals], timedelta()), unit_price))

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
