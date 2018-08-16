import unittest
from datetime import datetime

from timewreport.interval import TimeWarriorInterval

import tests.testsupport as tests
from billwarrior.invoice import Invoice, LineItem


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
    def test_date_should_display_month_day_year_correctly_in_latex(self):
        day = datetime.today()
        line_item = LineItem(day, 0, 0)

        self.assertEqual(line_item.date, day.strftime('%B %d, %Y'))

