from datetime import timedelta


class DayEntry(object):
    def __init__(self, intervals):
        interval_dates = set([interval.get_date() for interval in intervals])
        if len(interval_dates) > 1:
            raise ValueError

        self.__intervals = intervals

    @property
    def date(self):
        return self.__intervals[0].get_date().date()

    def add(self, interval):
        if not interval.get_date().date() == self.date:
            raise ValueError(
                    "Can't add interval with different date than DayEntry({}): {}".format(
                    self.date, interval.get_date().date()
                )
            )
        self.__intervals.append(interval)

    def total_duration(self):
        return sum(
            [interval.get_duration() for interval in self.__intervals], timedelta()
        )
