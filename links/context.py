"""
App-initializg code is responsible for settings context attributes.
"""

from links.repos import couchdb
from links.settings import Settings
from links.logger import get_logger

LOGGER = get_logger(__name__)


class AppContext:

    def __init__(self):
        self.user_repo = None
        self.bookmark_repo = None


context = AppContext()


def init_context():
    if Settings.DATABASE_PLUGIN == 'couchdb':
        context.user_repo = couchdb.CouchDBUserRepo()
        context.bookmark_repo = couchdb.CouchDBBookmarkRepo()
    else:
        raise RuntimeError(
            "Invalid value for Settings.DATABASE_PLUGIN: '{}'"
            .format(Settings.DATABASE_PLUGIN)
        )

    LOGGER.debug("*** Initialized database plugin '%s' *** ", Settings.DATABASE_PLUGIN)
