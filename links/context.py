"""
App-initializing code is responsible for settings context attributes.
"""

from links.repos import couchdb
from links.repos import inmemory
from links.settings import Settings
from links.logger import get_logger

LOGGER = get_logger(__name__)


class AppContext:

    def __init__(self):
        self.user_repo = None
        self.bookmark_repo = None


context = AppContext()


def init_context(settings):
    if settings.DATABASE_PLUGIN == 'couchdb':
        context.user_repo = couchdb.CouchDBUserRepo()
        context.bookmark_repo = couchdb.CouchDBBookmarkRepo()
    elif settings.DATABASE_PLUGIN == 'inmemory':
        context.user_repo = inmemory.MemoryUserRepo()
        context.bookmark_repo = inmemory.MemoryBookmarkRepo()
    else:
        raise RuntimeError(
            "Invalid value for Settings.DATABASE_PLUGIN: '{}'"
            .format(settings.DATABASE_PLUGIN)
        )

    LOGGER.info("*** Initialized database plugin '%s' *** ", settings.DATABASE_PLUGIN)