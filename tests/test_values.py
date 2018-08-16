import unittest
from datetime import datetime, timedelta

import tests.testsupport as tests
from billwarrior.values import Day


class DayTest(unittest.TestCase):
    def test_total_should_sum_entries_together(self):
        intervals = [(tests.give_interval()), tests.give_interval()]
        day = Day(intervals)

        self.assertEqual(
                day.total_duration(),
                sum([interval.get_duration() for interval in intervals],
                    timedelta())
                )
