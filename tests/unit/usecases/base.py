from unittest import TestCase

from links.context import context
from links.repos.inmemory import MemoryBookmarkRepo, MemoryUserRepo


class UseCaseTest(TestCase):

    def setUp(self):
        # ensure a new/clean instance of context repositories
        context.bookmark_repo = MemoryBookmarkRepo()
        context.user_repo = MemoryUserRepo()
