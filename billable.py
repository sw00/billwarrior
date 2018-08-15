#!/usr/bin/env python3
import datetime


class Intervals(object):
    def __init__(self, list_of_intervals):
        # TODO reconcile tags vs days
        self._raw_intervals = list_of_intervals
        self._intervals = dict()

        for interval in list_of_intervals:
            records = self._intervals.get(interval.get_start().date(), [])
            records.append(interval.get_duration())
            self._intervals[interval.get_start().date()] = records

    def group_by_tags(self):
        tagged_collection = dict()
        for interval in self._raw_intervals:
            for tag in interval.get_tags():
                records = tagged_collection.get(tag, [])
                records.append(interval)
                tagged_collection[tag] = records

        return tagged_collection

    def totals_by_days(self):
        """Returns total duration per day."""
        return {
            day: sum(records, datetime.timedelta())
            for day, records in self._intervals.items()
        }
