import unittest
from datetime import datetime, timedelta
from random import randint
from unittest import mock

from timewreport.interval import TimeWarriorInterval

import tests.testsupport as tests
from billwarrior.config import BillWarriorConfig
from billwarrior.invoice import Invoice, ItemCategory, LineItem
from billwarrior.records import DayEntry


class BillWarriorConfigFake(BillWarriorConfig):
    def __init__(self):
        pass

    @classmethod
    def build(cls, tag_mapping={}, rate_mapping={}):
        def fake_category_of(tag):
            return tag_mapping.get(tag, None)

        def fake_rate_for(category):
            return rate_mapping.get(category, 0.0)

        billw_config = cls()
        billw_config.category_of = mock.MagicMock(side_effect=fake_category_of)
        billw_config.rate_for = mock.MagicMock(side_effect=fake_rate_for)

        return billw_config


class InvoiceTest(unittest.TestCase):
    def test_creates_categories_from_interval_tags_and_mapping(self):
        a, b = (
            tests.give_interval(tags=["videocall", "meeting"]),
            tests.give_interval(tags=["flight", "nyc"]),
        )

        billw_config = BillWarriorConfigFake.build(
            {"meeting": "Consulting & Research", "flight": "Travel"}
        )

        invoice = Invoice([a, b], billw_config)
        items = invoice.items()

        expected_a, expected_b = (
            ItemCategory("Consulting & Research", [DayEntry([a])], 0.0),
            ItemCategory("Travel", [DayEntry([b])], 0.0),
        )

        self.assertEqual(len(items), 2)
        self.assertIn(str(expected_a), [str(item) for item in items])
        self.assertIn(str(expected_b), [str(item) for item in items])

    def test_raises_exception_when_interval_sorts_into_more_than_one_category(self):
        a, b = (
            tests.give_interval(tags=["videocall", "meeting"]),
            tests.give_interval(tags=["flight", "videocall", "other tag"]),
        )

        a_category = "Consulting & Research"
        tag_mapping = {
            "meeting": a_category,
            "videocall": a_category,
            "flight": "Travel",
        }

        billw_config = BillWarriorConfigFake.build(tag_mapping)

        with self.assertRaises(ValueError) as e:
            Invoice([a, b], billw_config)

        self.assertEqual(
            str(e.exception),
            "Interval has tags belonging to different categories: {}".format(
                ["flight", "videocall"]
            ),
        )

    def test_raises_exception_when_an_interval_does_not_belong_to_any_category(self):
        a, b = (
            tests.give_interval(tags=["meeting"]),
            tests.give_interval(tags=["coding", "stories"]),
        )

        billw_config = BillWarriorConfigFake.build(
            {"flight": "Travel", "coding": "Software Development"}
        )

        with self.assertRaises(ValueError) as e:
            Invoice([a, b], billw_config)

        self.assertEqual(
            str(e.exception), "Interval doesn't belong to any category: {}".format(a)
        )

    @unittest.skip
    def test_sets_unit_price_for_item_category(self):
        a, b = (
            tests.give_interval(tags=["meeting"]),
            tests.give_interval(tags=["coding", "stories"]),
        )

        category_mapping = {
            "Consulting & Research": ["meeting"],
            "Software Development": ["coding"],
        }
        invoice = Invoice(
            [a, b],
            category_mapping,
            {"Consulting & Research": 9.34, "Software Development": 12.02},
        )
        items = invoice.items()

        expected_a, expected_b = (
            ItemCategory("Consulting & Research", [DayEntry([a])], 9.34),
            ItemCategory("Software Development", [DayEntry([b])], 12.02),
        )

        self.assertEqual(len(items), 2)
        self.assertIn(str(expected_a), [str(item) for item in items])
        self.assertIn(str(expected_b), [str(item) for item in items])

    @unittest.skip
    def test_prints_invoice_categories_and_items(self):
        a, b = (
            tests.give_interval(tags=["meeting"]),
            tests.give_interval(tags=["coding", "stories"]),
        )
        category_mapping = {
            "Consulting & Research": ["meeting"],
            "Software Development": ["coding"],
        }
        expected_a, expected_b = (
            ItemCategory("Consulting & Research", [DayEntry([a])], 9.34),
            ItemCategory("Software Development", [DayEntry([b])], 12.02),
        )

        invoice = Invoice(
            [a, b],
            category_mapping,
            {"Consulting & Research": 9.34, "Software Development": 12.02},
        )

        self.assertEqual(str(invoice), "\n".join([str(expected_a), str(expected_b)]))


class ItemCategoryTest(unittest.TestCase):
    def test_header_should_display_formatted_tag_name_as_category_string(self):
        category = ItemCategory(" unclean tag   name ", set(), 0.0)
        self.assertEqual(category.header, "Unclean tag name")

    def test_line_items_should_be_populated_with_day_entries(self):
        entries = [
            DayEntry([tests.give_interval()]),
            DayEntry([tests.give_interval()]),
            DayEntry([tests.give_interval()]),
        ]

        category = ItemCategory("arbitray category", entries, 0.0)

        self.assertEqual(len(category.line_items), len(entries))

    def test_line_items_should_be_sorted_by_date(self):
        entries = [
            DayEntry([tests.give_interval()]),
            DayEntry([tests.give_interval()]),
            DayEntry([tests.give_interval()]),
        ]
        category = ItemCategory("arbitray category", entries, 0.0)

        sorted_date_list = sorted([entry.date for entry in entries])
        print(sorted_date_list)
        self.assertListEqual(
            [
                datetime.strptime(line_item.date, "%B %d, %Y").date()
                for line_item in category.line_items
            ],
            sorted_date_list,
        )

    def test_str_should_display_header_line_items_and_subtotal_as_latex_output(self):
        a, b = tests.give_interval(), tests.give_interval()
        entries = [DayEntry([a]), DayEntry([b])]

        category = ItemCategory("arbitrary category", entries, 0.0)

        expected = "".join(
            [
                "\\feetype{%s}\n" % category.header,
                "".join(
                    [
                        "%s\n" % LineItem(i.get_date(), i.get_duration(), 0.0)
                        for i in sorted([a, b], key=lambda x: x.get_date())
                    ]
                ),
                "\\subtotal\n",
                "%------------------------------------------------",
            ]
        )

        self.assertEqual(category.__str__(), expected)


class LineItemTest(unittest.TestCase):
    def test_date_should_display_month_day_year_correctly_in_latex(self):
        day = datetime.today()
        line_item = LineItem(day, None, None)

        self.assertEqual(line_item.date, day.strftime("%B %d, %Y"))

    def test_duration_should_display_decimal_value_of_hours_worked(self):
        duration = timedelta(
            hours=randint(0, 8), minutes=randint(0, 59), seconds=randint(0, 59)
        )
        line_item = LineItem(datetime.today(), duration, None)

        totsec = duration.total_seconds()
        total = (
            totsec // 3600
            + (((totsec % 3600) // 60) / 60)
            + (((totsec % 3600) % 60) / 6000)
        )

        self.assertEqual(line_item.duration, "{:.2f}".format(total))

    def test_unit_price_should_be_displayed_as_is(self):
        unit_price = randint(0, 200) + randint(0, 99) * 0.1
        line_item = LineItem(datetime.today(), timedelta(), unit_price)

        self.assertEqual(line_item.unit_price, "{:.2f}".format(unit_price))

    def test_str_should_display_full_line_item_as_latex_output(self):
        line_item = LineItem(
            datetime.today(),
            timedelta(0, randint(0, 8) * 3600),
            randint(0, 200) + randint(0, 99) * 0.1,
        )

        self.assertEqual(
            line_item.__str__(),
            "\\hourrow{%s}{%s}{%s}"
            % (line_item.date, line_item.duration, line_item.unit_price),
        )
