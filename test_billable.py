import unittest
from datetime import date, datetime, timedelta
from random import randint

from timewreport.interval import TimeWarriorInterval

import billable

DT_FORMAT = "%Y%m%dT%H%M%SZ"


class BillableTest(unittest.TestCase):
    def test_totals_by_days_should_sum_multiple_intervals_on_same_day(self):
        interval_a = self._give_interval()
        interval_b = self._give_interval(interval_a.get_date())
        self.assertEqual(interval_a.get_date().date(), interval_b.get_date().date())
        same_day = interval_a.get_date().date()

        intervals = billable.Intervals([interval_a, interval_b])
        days = intervals.totals_by_days()

        self.assertIn(same_day, days.keys())
        self.assertEqual(
            days.get(same_day), (interval_a.get_duration() + interval_b.get_duration())
        )

    def _give_interval(self, day=None, tags=[]):
        if day:
            start = day.replace(hour=randint(0, 23))
        else:
            start = datetime.today().replace(day=randint(1, 28), month=randint(1, 12))

        end = start + timedelta(0, randint(60 * 5, 60 * 60 * 2))  # up to 2h

        return TimeWarriorInterval(
            start.strftime(DT_FORMAT), end.strftime(DT_FORMAT), tags
        )


if __name__ == "__main__":
    unittest.main()
