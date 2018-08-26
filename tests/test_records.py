import unittest
from datetime import datetime, timedelta

import tests.testsupport as tests
from billwarrior.records import DayEntry


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

    def test_add_should_raise_exception_when_interval_has_different_day(self):
        interval = tests.give_interval()
        day_entry = DayEntry([interval])

        new_interval = tests.give_interval(interval.get_date() + timedelta(days=2))

        with self.assertRaises(ValueError) as e:
            day_entry.add(new_interval)

        self.assertEqual(
            str(e.exception),
            "Can't add interval with different date than DayEntry({}): {}".format(
                day_entry.date, new_interval.get_date().date()
            ),
        )

    def test_add_should_add_interval_when_interval_has_same_day(self):
        interval = tests.give_interval()
        day_entry = DayEntry([interval])

        duration_a = day_entry.total_duration()

        new_interval = tests.give_interval(interval.get_date())
        day_entry.add(new_interval)

        self.assertEqual(day_entry.total_duration(), duration_a + new_interval.get_duration())

