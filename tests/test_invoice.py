import unittest
from datetime import datetime, timedelta, timezone
from random import randint
from unittest import mock

import pytest
from timewreport.interval import TimeWarriorInterval

import tests.testsupport as tests
from billwarrior.config import BillWarriorConfig
from billwarrior.invoice import Invoice, ItemCategory, LineItem


class BillWarriorConfigFake(BillWarriorConfig):
    def __init__(self):
        pass

    @classmethod
    def build(cls, tag_mapping={}, rate_mapping={}):
        def fake_text_for(category):
            return category

        def fake_category_of(tag):
            return tag_mapping.get(tag, None)

        def fake_rate_for(category):
            return rate_mapping.get(category, 0.0)

        billw_config = cls()
        billw_config.text_for = mock.MagicMock(side_effect=fake_text_for)
        billw_config.category_of = mock.MagicMock(side_effect=fake_category_of)
        billw_config.rate_for = mock.MagicMock(side_effect=fake_rate_for)

        return billw_config


class InvoiceTest(unittest.TestCase):
    def test_creates_different_categories_from_interval_tags_and_mapping(self):
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
            ItemCategory("Consulting & Research", {a.get_date().date(): [a]}, 0.0),
            ItemCategory("Travel", {b.get_date().date(): [b]}, 0.0),
        )

        self.assertEqual(len(items), 2)
        self.assertEqual(str(expected_a), str(items[0]))
        self.assertEqual(str(expected_b), str(items[1]))

    @pytest.mark.freeze_time(tz_offset=2)
    def test_groups_intervals_of_same_category(self):
        same_day = datetime.today()
        a, b, c = (
            tests.give_interval(same_day, tags=["on-site", "coding"]),
            tests.give_interval(same_day, tags=["coding", "off-site"]),
            tests.give_interval(tags=["coding", "cafe"]),
        )

        billw_config = BillWarriorConfigFake.build({"coding": "Consulting & Research"})

        invoice = Invoice([a, b, c], billw_config)
        items = invoice.items()

        expected = ItemCategory(
            "Consulting & Research",
            {same_day.date(): [a, b], c.get_date().date(): [c]},
            0.0,
        )

        self.assertEqual(len(items), 1)  # one category
        self.assertEqual(str(items[0]), str(expected))

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

        with self.assertRaisesRegex(
            ValueError,
            "Intervals with the following tags belongs to more than one category: .",
        ) as e:
            Invoice([a, b], billw_config)

    def test_raises_exception_when_an_interval_does_not_belong_to_any_category(self):
        a, b = (
            tests.give_interval(tags=["meeting"]),
            tests.give_interval(tags=["coding", "stories"]),
        )

        billw_config = BillWarriorConfigFake.build(
            {"flight": "Travel", "coding": "Software Development"}
        )

        with self.assertRaisesRegex(
            ValueError,
            "These intervals with the following tags don't belong to any category: .",
        ) as e:
            Invoice([a, b], billw_config)

    def test_sets_unit_price_for_item_category(self):
        a, b = (
            tests.give_interval(tags=["meeting"]),
            tests.give_interval(tags=["coding", "stories"]),
        )

        category_a = "Consulting & Research"
        category_b = "Software Development"

        billw_config = BillWarriorConfigFake.build(
            {"meeting": category_a, "coding": category_b},
            {category_a: 9.34, category_b: 12.02},
        )

        invoice = Invoice([a, b], billw_config)
        items = invoice.items()

        expected_a, expected_b = (
            ItemCategory(
                "Consulting & Research",
                {a.get_date().date(): [a]},
                billw_config.rate_for(category_a),
            ),
            ItemCategory(
                "Software Development",
                {b.get_date().date(): [b]},
                billw_config.rate_for(category_b),
            ),
        )

        self.assertEqual(len(items), 2)
        self.assertEqual(str(expected_a), str(items[0]))
        self.assertEqual(str(expected_b), str(items[1]))

    def test_alpha_orders_categories(self):
        a, b = (
            tests.give_interval(tags=["meeting"]),
            tests.give_interval(tags=["coding", "stories"]),
        )

        category_a = "Consulting & Research"
        category_b = "Software Development"

        billw_config = BillWarriorConfigFake.build(
            {"coding": category_b, "meeting": category_a},
            {category_a: 12.02, category_b: 9.34},
        )

        invoice = Invoice([b, a], billw_config)
        items = invoice.items()

        expected_a, expected_b = (
            ItemCategory(
                "Consulting & Research",
                {a.get_date().date(): [a]},
                billw_config.rate_for(category_a),
            ),
            ItemCategory(
                "Software Development",
                {b.get_date().date(): [b]},
                billw_config.rate_for(category_b),
            ),
        )

        self.assertEqual(len(items), 2)
        self.assertEqual(str(expected_a), str(items[0]))
        self.assertEqual(str(expected_b), str(items[1]))

    def test_prints_invoice_categories_and_items(self):
        a, b = (
            tests.give_interval(tags=["meeting"]),
            tests.give_interval(tags=["coding", "stories"]),
        )

        category_a = "Consulting & Research"
        category_b = "Software Development"

        billw_config = BillWarriorConfigFake.build(
            {"meeting": category_a, "coding": category_b},
            {category_a: 9.34, category_b: 12.02},
        )
        expected_a, expected_b = (
            ItemCategory(
                "Consulting & Research",
                {a.get_date().date(): [a]},
                billw_config.rate_for(category_a),
            ),
            ItemCategory(
                "Software Development",
                {b.get_date().date(): [b]},
                billw_config.rate_for(category_b),
            ),
        )

        invoice = Invoice([a, b], billw_config)
        printed_invoice = str(invoice)

        self.assertIn(str(expected_a), printed_invoice)
        self.assertIn(str(expected_b), printed_invoice)


class ItemCategoryTest(unittest.TestCase):
    def test_header_should_display_formatted_tag_name_as_category_string(self):
        category = ItemCategory(" unclean tag   name ", {}, 0.0)
        self.assertEqual(category.header, "Unclean tag name")

    def test_line_items_should_be_populated_with_entries_per_day(self):
        a_day = datetime.today()
        entries = [
            [tests.give_interval(a_day + timedelta(days=1))],
            [tests.give_interval(a_day + timedelta(days=2))],
            [tests.give_interval(a_day + timedelta(days=3))],
        ]
        intervals_by_day = {entry[0].get_date().date(): entry for entry in entries}

        category = ItemCategory("arbitray category", intervals_by_day, 0.0)

        self.assertEqual(len(category.line_items), len(entries))

    def test_line_items_should_be_sorted_by_date(self):
        entries = [
            [tests.give_interval()],
            [tests.give_interval()],
            [tests.give_interval()],
        ]
        dates = [entry[0].get_date().date() for entry in entries]

        category = ItemCategory("arbitray category", dict(zip(dates, entries)), 0.0)

        sorted_date_list = sorted([entry[0].get_date().date() for entry in entries])
        self.assertListEqual(
            [
                datetime.strptime(line_item.date, "%B %d, %Y").date()
                for line_item in category.line_items
            ],
            sorted_date_list,
        )

    def test_str_should_display_header_line_items_and_subtotal_as_latex_output(self):
        a, b = tests.give_interval(), tests.give_interval()
        entries = {a.get_date().date(): [a], b.get_date().date(): [b]}

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
            hours=8, minutes=51, seconds=59
        )
        line_item = LineItem(datetime.today(), duration, None)

        totsec = duration.total_seconds()
        total = totsec / 3600.0

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
