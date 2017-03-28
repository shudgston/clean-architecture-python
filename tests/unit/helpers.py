from nose.tools import nottest

from links.context import context
from links.entities import Bookmark, User
from tests.unit.doubles import MemoryBookmarkRepo, MemoryUserRepo


@nottest
def setup_testing_context():
    context.bookmark_repo = MemoryBookmarkRepo()
    context.user_repo = MemoryUserRepo()


@nottest
def setup_testing_data():
    setup_testing_context()

    users = [
        User('hodor'),
        User('fred'),
    ]

    for u in users:
        context.user_repo.save(u)

    bookmarks = [
        Bookmark('hodorID1', 'hodor', 'google', 'web://google.com'),
        Bookmark('hodorID2', 'hodor', 'reddit', 'web://reddit.com'),
        Bookmark('hodorID3', 'hodor', 'CNN', 'web://cnn.com'),
        Bookmark('fredID1', 'fred', 'altavista', 'web://altavista.com'),
    ]

    for b in bookmarks:
        context.bookmark_repo.save(b)
