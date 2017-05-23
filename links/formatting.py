import re
import unicodedata
from datetime import datetime
from urllib.parse import urlparse

DEFAULT_DATE_FORMAT = '%b %-d, %Y'


def iso_date(dt):
    assert isinstance(dt, datetime)
    return dt.isoformat()


def display_date(dt):
    assert isinstance(dt, datetime)
    return dt.strftime(DEFAULT_DATE_FORMAT)


def host_from_url(url):
    try:
        host = urlparse(url).netloc
    except AssertionError:
        host = ''
    return host


def slugify(text):
    """
    """
    s = unicodedata.normalize('NFKC', text.strip())
    s = re.sub(r'[^\w\s-]', '', s)
    # limit final length
    return re.sub(r'[-\s]+', '-', s).lower()[:200]
