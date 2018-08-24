from billwarrior.values import DayEntry


class Invoice(object):
    def __init__(self, intervals, category_mapping=None, category_prices={}):
        if category_mapping:
            # inverts the mapping for many-to-one tag-category relation
            tag_categories = {
                tag: category
                for category, tags in category_mapping.items()
                for tag in tags
            }
        else:
            tags = [interval.get_tags()[0] for interval in intervals]
            tag_categories = dict(zip(tags, tags))

        self.__items = []

        for interval in intervals:
            mapped_tag = [
                interval_tag
                for interval_tag in interval.get_tags()
                if interval_tag in tag_categories.keys()
            ]

            categories = set([tag_categories.get(tag) for tag in mapped_tag])
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
            current_category = tag_categories[mapped_tag.pop()]
            self.__items.append(
                ItemCategory(
                    current_category,
                    entries,
                    category_prices.get(current_category, 0.0),
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
