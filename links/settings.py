"""
"""

import os


class Settings:
    BOOKMARK_LIST_FILTERS = {'everything': 1000, 'recent': 25}
    DATABASE_PLUGIN = os.environ.get('LINKS_DATABASE_PLUGIN')
    LOGGING_LEVEL = int(os.environ.get('LINKS_LOGGING_LEVEL', 20))  # info


class CouchDBSettings(Settings):
    DATABASE_NAME = os.environ.get('LINKS_DATABASE_NAME', 'NOTSET')
    DATABASE_USER = os.environ.get('LINKS_DATABASE_USER', 'NOTSET')
    DATABASE_PASSWORD = os.environ.get('LINKS_DATABASE_PASSWORD', 'NOTSET')
    DATABASE_HOST = os.environ.get('LINKS_DATABASE_HOST', 'NOTSET')
