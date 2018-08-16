from datetime import datetime, timedelta


class Tag(object):
    def __init__(self, name, intervals):
        self.__name = name
        self.__record_collection = dict()
        self.__sort_into_day_entries(intervals)

    @property
    def name(self):
        return self.__name

    def records(self):
        return self.__record_collection

    def add(self, interval):
        interval.get_start().date()
        entry = self.__record_collection.get(interval.get_start().date(), [])
        entry.append(interval)

    def day_totals(self):
        return {day: sum((interval.get_duration() for interval in intervals), timedelta()) 
                for day, intervals in self.__record_collection.items()} 

    def __sort_into_day_entries(self, intervals):
        for interval in intervals:
            entry = self.__record_collection.get(interval.get_start().date(), [])
            entry.append(interval)
            self.__record_collection[interval.get_start().date()] = entry
