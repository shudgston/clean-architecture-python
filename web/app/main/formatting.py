from datetime import datetime

DEFAULT_DATE_FORMAT = '%b %-d, %Y'


def format_iso_date(dt):
    assert isinstance(dt, datetime)
    return dt.isoformat()


def format_display_date(dt):
    assert isinstance(dt, datetime)
    return dt.strftime(DEFAULT_DATE_FORMAT)
