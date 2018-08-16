import unittest
from datetime import datetime, timedelta

import tests.testsupport as tests
from billwarrior.values import DayEntry


class DayTest(unittest.TestCase):
    def test_total_should_sum_entries_together(self):
        same_day = datetime.today()
        intervals = [(tests.give_interval(same_day)), tests.give_interval(same_day)]
        day = DayEntry(intervals)

        self.assertEqual(
            day.total_duration(),
            sum([interval.get_duration() for interval in intervals], timedelta()),
        )

    def test_exception_raised_when_intervals_have_different_start_dates(self):
        a = tests.give_interval()
        b = tests.give_interval(a.get_date() + timedelta(days=7))

        with self.assertRaises(ValueError):
            DayEntry([a, b])

    def test_date_should_return_date_object_representing_day(self):
        interval = tests.give_interval()
        day_entry = DayEntry([interval])

        self.assertEqual(day_entry.date, interval.get_date().date())
