class Tag(object):
    def __init__(self, name, intervals):
        self._name = name
        self._intervals = intervals

    def records(self):
        record_collection = dict()
        for interval in self._intervals:
            entry = record_collection.get(interval.get_start().date(), [])
            entry.append(interval)
            record_collection[interval.get_start().date()] = entry

        return record_collection
        

