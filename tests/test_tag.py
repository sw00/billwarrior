import unittest
from datetime import datetime

import tests.testsupport as tests
from billwarrior import tag


class TagTest(unittest.TestCase):
    def test_records_should_return_records_grouped_by_day_for_tag(self):
        a, b = (
            tests.give_interval(tags=['coding']),
            tests.give_interval(tags=['coding']),
        )

        coding_tag = tag.Tag('coding', [a, b])
        records = coding_tag.records()

        self.assertIn(a.get_date().date(), records.keys())
        self.assertIn(b.get_date().date(), records.keys())
        self.assertIn(a, records.get(a.get_date().date()))
        self.assertIn(b, records.get(b.get_date().date()))
        
    def test_add_should_add_record_to_day_under_tag(self):
        a, b = (
            tests.give_interval(tags=['coding']),
            tests.give_interval(tags=['coding']),
        )

        c = tests.give_interval(a.get_date(), tags=['coding'])

        coding_tag = tag.Tag('coding', [a, b])
        coding_tag.add(c)
        records = coding_tag.records()

        self.assertIn(c, records.get(a.get_date().date()))

    def test_day_totals_should_sum_interval_durations_by_day(self):
        same_day = datetime.today()
        a, b = (
            tests.give_interval(same_day, tags=['coding']),
            tests.give_interval(same_day, tags=['coding']),
        )

        coding_tag = tag.Tag('coding', [a, b])
        records = coding_tag.day_totals()

        self.assertIn(same_day.date(), records.keys())
        self.assertEqual((a.get_duration() + b.get_duration()),
                records.get(same_day.date()))


