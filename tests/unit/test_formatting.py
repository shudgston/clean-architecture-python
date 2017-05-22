from datetime import datetime
from unittest import TestCase
from links.formatting import display_date, iso_date, host_from_url, slugify


class FormatDisplayDateTest(TestCase):

    def test_display_date(self):
        formatted = display_date(datetime(year=2017, month=1, day=1))
        self.assertEqual(formatted, 'Jan 1, 2017')

    def test_display_date_with_invalid_datetime(self):
        with self.assertRaises(AssertionError):
            display_date(None)


class FormatISODateTest(TestCase):

    def test_format_iso_date(self):
        formatted = iso_date(datetime(year=2017, month=1, day=1))
        self.assertEqual(formatted, '2017-01-01T00:00:00')

    def test_format_iso_date_with_invalid_datetime(self):
        with self.assertRaises(AssertionError):
            iso_date(None)


class HostFromURLTest(TestCase):

    def test_host_is_extracted_from_url(self):
        self.assertEqual('www.test.com', host_from_url('http://www.test.com'))
        self.assertEqual('test.com', host_from_url('http://test.com'))

    def test_invalid_url(self):
        self.assertEqual('', host_from_url(''))
        # urlparse behavior
        self.assertEqual(b'', host_from_url(None))


class SlugifyTest(TestCase):

    def test_slugify(self):
        self.assertEqual('hello-world', slugify('HELLO world!'))
        self.assertEqual('hello-world', slugify('       HELLO   world!'))
        self.assertEqual('ok', slugify(' o*@#*$%@#$%*k'))
        self.assertEqual('δ', slugify('\u0394'))
        self.assertEqual('helloworld', slugify('&&HELLO@WORLD!'))
        self.assertEqual(200, len(slugify('longer than 200' * 200)))
