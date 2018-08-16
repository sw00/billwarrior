import unittest
from datetime import date, datetime, timedelta
from random import randint

from timewreport.interval import TimeWarriorInterval

from billwarrior import billable

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

    def test_group_by_tags_should_group_intervals_by_unique_tags(self):
        interval_a = self._give_interval(tags=['meeting'])
        interval_b = self._give_interval(tags=['r&d'])
        interval_c = self._give_interval(tags=['coding'])
        interval_d = self._give_interval(tags=['coding'])

        intervals = billable.Intervals([interval_a, interval_b, interval_c, interval_d])

        grouped_intervals = intervals.group_by_tags()

        self.assertCountEqual(['meeting', 'r&d', 'coding'], grouped_intervals.keys())
        self.assertIn(interval_c, grouped_intervals.get('coding'))
        self.assertIn(interval_d, grouped_intervals.get('coding'))
        self.assertEqual([interval_a], grouped_intervals.get('meeting'))
        self.assertEqual([interval_b], grouped_intervals.get('r&d'))

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
