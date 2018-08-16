import unittest

from timewreport.interval import TimeWarriorInterval

import tests.testsupport as tests
from billwarrior.invoice import Invoice


class InvoiceTest(unittest.TestCase):
    def test_categories_should_return_list_of_tags(self):
        a, b, c = (
                tests.give_interval(tags=['meeting']),
                tests.give_interval(tags=['pingpong']),
                tests.give_interval(tags=['coding']),
                )

        invoice = Invoice([a,b,c])
        categories = invoice.categories()

        self.assertCountEqual(['meeting', 'pingpong', 'coding'], categories)


class LineItemTest(unittest.TestCase):
    pass


