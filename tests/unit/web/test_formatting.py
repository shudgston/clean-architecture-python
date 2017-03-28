from datetime import datetime
from unittest import TestCase

from web.app.main.formatting import format_display_date, format_iso_date


class FormatDisplayDateTest(TestCase):

    def test_format_display_date(self):
        formatted = format_display_date(datetime(year=2017, month=1, day=1))
        self.assertEqual(formatted, 'Jan 1, 2017')

    def test_format_display_date_with_invalid_datetime(self):
        with self.assertRaises(AssertionError):
            format_display_date(None)


class FormatISODateTest(TestCase):

    def test_format_iso_date(self):
        formatted = format_iso_date(datetime(year=2017, month=1, day=1))
        self.assertEqual(formatted, '2017-01-01T00:00:00')

    def test_format_iso_date_with_invalid_datetime(self):
        with self.assertRaises(AssertionError):
            format_iso_date(None)
