#!/usr/bin/env python3
import datetime


class Intervals(object):
    def __init__(self, list_of_intervals):
        self._intervals = dict()

        for interval in list_of_intervals:
            records = self._intervals.get(interval.get_start().date(), [])
            records.append(interval.get_duration())
            self._intervals[interval.get_start().date()] = records

    def totals_by_days(self):
        """Returns total duration per day."""
        return {
            day: sum(records, datetime.timedelta())
            for day, records in self._intervals.items()
        }
