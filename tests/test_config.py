import os
import unittest
from unittest.mock import mock_open, patch

from billwarrior.config import BillWarriorConfig


class BillWarriorConfigTest(unittest.TestCase):
    def setUp(self):
        self.raw_file_data = (
            "[categories]"
            "\nbillable.tags = coding, research, meeting"
            "\nbillable.text = Software Engineering & Consulting"
            "\nbillable.rate = 43.50"
            "\nexpensed.tags = travel, flight, train"
            "\nexpensed.text = Discounted Travel Time"
            "\nexpensed.rate = 21.75"
            "\nnonbillable.tags = pingpong, lunch"
            "\nnonbillable.text = Miscellaneous activities"
            "\nnonbillable.rate = 0.0"
        )

    def test_categories_should_parse_list_of_categories_from_ini_file(self):
        file_path = os.path.join(
            os.getenv("HOME"), ".config", "billwarrior", "billwarrior.ini"
        )
        expected_categories = ["billable", "expensed", "nonbillable"]

        with patch(
            "builtins.open", mock_open(read_data=self.raw_file_data)
        ) as mocked_open:
            config = BillWarriorConfig()

        mocked_open.assert_called_once_with(file_path, "r")
        self.assertCountEqual(expected_categories, config.categories)

    def test_text_should_return_configured_text_for_category(self):
        with patch(
            "builtins.open", mock_open(read_data=self.raw_file_data)
        ) as mocked_open:
            config = BillWarriorConfig()

        expected = {
            "billable": "Software Engineering & Consulting",
            "expensed": "Discounted Travel Time",
            "nonbillable": "Miscellaneous activities",
        }

        for category_name, category_text in expected.items():
            self.assertEqual(config.text_for(category_name), category_text)

    def test_rate_should_return_configured_rate_for_category(self):
        with patch(
            "builtins.open", mock_open(read_data=self.raw_file_data)
        ) as mocked_open:
            config = BillWarriorConfig()

        expected = {"billable": 43.50, "expensed": 21.75, "nonbillable": 0.0}

        for category_name, category_rate in expected.items():
            self.assertEqual(config.rate_for(category_name), category_rate)

    def test_category_of_should_return_category_that_tag_belongs_to(self):
        with patch(
            "builtins.open", mock_open(read_data=self.raw_file_data)
        ) as mocked_open:
            config = BillWarriorConfig()

        expected = {
            "billable": ["coding", "research", "meeting"],
            "expensed": ["travel", "flight", "train"],
            "nonbillable": ["pingpong", "lunch"],
        }

        for category_name, tags in expected.items():
            for tag in tags:
                self.assertEqual(config.category_of(tag), category_name)
