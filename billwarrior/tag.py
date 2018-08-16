class Tag(object):
    def __init__(self, name, intervals):
        self._name = name
        self.__record_collection = dict()
        self.__sort_into_day_entries(intervals)

    def records(self):
        return self.__record_collection

    def add(self, interval):
        interval.get_start().date()
        entry = self.__record_collection.get(interval.get_start().date(), [])
        entry.append(interval)

    def __sort_into_day_entries(self, intervals):
        for interval in intervals:
            entry = self.__record_collection.get(interval.get_start().date(), [])
            entry.append(interval)
            self.__record_collection[interval.get_start().date()] = entry
