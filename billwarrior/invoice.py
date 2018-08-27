from datetime import timedelta

from timewreport.interval import TimeWarriorInterval


class Invoice(object):
    def __init__(self, intervals, config):
        self.config = config
        self.__items = []

        sorted_intervals = self._sort_by_category(intervals)

        for category, intervals in sorted_intervals.items():
            days = set([interval.get_date().date() for interval in intervals])
            intervals_by_day = {
                day: [i for i in intervals if i.get_date().date() == day]
                for day in days
            }

            self.__items.append(
                ItemCategory(category, intervals_by_day, config.rate_for(category))
            )

    def _sort_by_category(self, list_of_intervals):
        tags = set(
            [tag for interval in list_of_intervals for tag in interval.get_tags()]
        )
        tag_mapping = {t: self.config.category_of(t) for t in tags}
        all_categories = set([c for c in tag_mapping.values()])

        interval_categories = {
            IntervalContainer(i): set(
                [tag_mapping[t] for t in i.get_tags() if tag_mapping.get(t, None)]
            )
            for i in list_of_intervals
        }

        no_category_list = [i for i, c in interval_categories.items() if len(c) == 0]
        ambiguous_list = [i for i, c in interval_categories.items() if len(c) > 1]

        if len(no_category_list) > 0:
            raise ValueError(
                "These intervals with the following tags don't belong to any category: {}".format(
                    [i.get_tags() for i in no_category_list]
                )
            )

        if len(ambiguous_list) > 0:
            raise ValueError(
                "Intervals with the following tags belongs to more than one category: {}".format(
                    [i.get_tags() for i in ambiguous_list]
                )
            )

        return {
            c: [i for i in list_of_intervals if c in interval_categories[i]]
            for c in all_categories
            if c
        }

    def items(self):
        return self.__items

    def __str__(self):
        return "\n".join([str(item) for item in self.__items])


class IntervalContainer(TimeWarriorInterval):
    def __new__(cls, interval):
        interval.__class__ = cls
        return interval

    def __init__(self, interval):
        pass

    def __hash__(self):
        return hash(repr(self))


class ItemCategory(object):
    def __init__(self, tag_name, intervals_by_day, unit_price):
        self.header = (
            " ".join([x for x in tag_name.split() if not x == ""]).strip().capitalize()
        )
        self.line_items = []

        for day, intervals in sorted(intervals_by_day.items(), key=lambda x: x[0]):
            self.line_items.append(
                LineItem(
                    day,
                    sum(
                        [interval.get_duration() for interval in intervals], timedelta()
                    ),
                    unit_price,
                )
            )

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
