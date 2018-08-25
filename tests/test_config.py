import os
import unittest
from unittest.mock import mock_open, patch

import pytest

from billwarrior.config import BillWarriorConfig


class BillWarriorConfigTest(unittest.TestCase):
    def setUp(self):
        self.raw_file_data = (
            "[categories]"
            "\nbillable.tags = coding, research, meeting"
            "\nbillable.text = Software Engineering & Consulting"
            "\nbillable.rate = 43.50"
            "\nexpensed.tags = travel, flight, train"
            "\nexpensed.text = Rebate"
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

        with patch("builtins.open", mock_open(read_data=self.raw_file_data)) as mocked_open:
            config = BillWarriorConfig()

        mocked_open.assert_called_once_with(file_path, "r")
        self.assertCountEqual(expected_categories, config.categories)
