from datetime import timedelta


class Day(object):
    def __init__(self, intervals):
        if len(set([interval.get_date() for interval in intervals])) > 1:
            raise ValueError

        self.__intervals = intervals

    def total_duration(self):
        return sum([interval.get_duration() for interval in self.__intervals],
                timedelta())
