import os
import sys
import unittest
from unittest import mock
from io import StringIO


from timewreport.parser import TimeWarriorParser

from billwarrior.config import BillWarriorConfig
from billwarrior.invoice import Invoice

INI_FILE = """
[categories]
billable.tags = coding, research, meeting
billable.text = Software Engineering & Consulting
billable.rate = 43.50

expensed.tags = travel, flight, train
expensed.text = Discounted time & expenses
expensed.rate = 21.75

nonbillable.tags = pingpong, lunch
nonbillable.text = Miscelaneous activities
nonbillable.rate = 0.0
"""

TIMEW_REPORT = """
[
{"start":"20180601T075048Z","end":"20180601T083639Z","tags":["travel","train"]},
{"start":"20180601T090520Z","end":"20180601T103037Z","tags":["meeting","client-side"]},
{"start":"20180601T123440Z","end":"20180601T144223Z","tags":["lunch"]},
{"start":"20180602T072333Z","end":"20180602T111036Z","tags":["coding","off-site"]},
{"start":"20180603T083437Z","end":"20180603T121520Z","tags":["coding","off-site"]},
{"start":"20180604T071523Z","end":"20180604T150143Z","tags":["travel","flight"]},
{"start":"20180605T071238Z","end":"20180605T102833Z","tags":["pingpong","lunch"]},
{"start":"20180606T083017Z","end":"20180606T123452Z","tags":["coding","on-site"]}
]
"""

EXPECTED_OUTPUT = """
\feetype{Billable}
\hourrow{June 01, 2018}{1.42}{43.50}
\hourrow{June 02, 2018}{3.78}{43.50}
\hourrow{June 03, 2018}{3.67}{43.50}
\hourrow{June 06, 2018}{4.07}{43.50}
\subtotal
%------------------------------------------------
\feetype{Expensed}
\hourrow{June 01, 2018}{0.76}{21.75}
\hourrow{June 04, 2018}{7.77}{21.75}
\subtotal
%------------------------------------------------
\feetype{Nonbillable}
\hourrow{June 01, 2018}{2.12}{0.00}
\hourrow{June 05, 2018}{3.26}{0.00}
\subtotal
%------------------------------------------------
"""


class BillWarriorTest(unittest.TestCase):
    @unittest.skip
    def test_happy_path(self):
        with mock.patch("builtins.open", mock.mock_open(read_data=INI_FILE)):
            config = BillWarriorConfig()

        timewparser = TimeWarriorParser(StringIO(TIMEW_REPORT))

        invoice = Invoice(timewparser.get_intervals(), config)

        self.assertEqual(str(invoice), EXPECTED_OUTPUT)
