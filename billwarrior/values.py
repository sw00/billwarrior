from datetime import timedelta


class Day(object):
    def __init__(self, intervals):
        self.__intervals = intervals

    def total_duration(self):
        return sum([interval.get_duration() for interval in self.__intervals],
                timedelta())
