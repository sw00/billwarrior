import unittest
from datetime import date, datetime, timedelta
from random import randint

from timewreport.interval import TimeWarriorInterval

import billable

DT_FORMAT = "%Y%m%dT%H%M%SZ"


class BillableTest(unittest.TestCase):
    def test_totals_by_days_should_sum_multiple_intervals_on_same_day(self):
        any_day = datetime.today().replace(day=randint(1, 28), month=randint(1, 12))

        start_a = any_day.replace(hour=12)
        end_a = start_a + timedelta(0, 60)

        start_b = end_a + timedelta(0, 60)
        end_b = start_b + timedelta(0, 60)

        interval_a = TimeWarriorInterval(
            start_a.strftime(DT_FORMAT),
            end_a.strftime(DT_FORMAT),
            ["A long, descriptive tag", "single-word-tag", "tag123"],
        )
        interval_b = TimeWarriorInterval(
            start_b.strftime(DT_FORMAT),
            end_b.strftime(DT_FORMAT),
            ["A long, descriptive tag", "single-word-tag", "tag123"],
        )

        intervals = billable.Intervals([interval_a, interval_b])
        days = intervals.totals_by_days()
        self.assertIn(any_day.date(), days)
        self.assertEqual(
            days.get(any_day.date()),
            (interval_a.get_duration() + interval_b.get_duration()),
        )


if __name__ == "__main__":
    unittest.main()
