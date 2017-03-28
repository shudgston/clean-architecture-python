import datetime
import unittest

from links.context import context
from links.entities import User, Bookmark
from links.usecases.bookmarks import BookmarkDetailsUseCase
from .spies import PresenterSpy
from ..helpers import setup_testing_context


class BookmarkDetailsUseCaseTest(unittest.TestCase):

    def setUp(self):
        self.user = User('user')
        self.otheruser = User('otheruser')
        self.unknownuser = User('unknownuser')
        setup_testing_context()
        context.user_repo.save(self.user)
        context.user_repo.save(self.otheruser)

        self.spy = PresenterSpy()
        self.uc = BookmarkDetailsUseCase()

    def test_user_with_bookmark_can_see_details(self):
        now = datetime.datetime.utcnow()
        context.bookmark_repo.save(
            Bookmark('id1', self.user.id, 'test', 'web://test.com', date_created=now))

        self.uc.bookmark_details(self.user.id, 'id1', self.spy)
        self.assertEqual(self.spy.response_model.bookmark_id, 'id1')
        self.assertEqual(self.spy.response_model.name, 'test')
        self.assertEqual(self.spy.response_model.url, 'web://test.com')
        self.assertEqual(self.spy.response_model.date_created, now)

    def test_user_with_none_cannot_see_details(self):
        request = {
            'user_id': self.user.id,
            'bookmark_id': 'id1',
        }

        with self.assertRaises(Exception):
            self.uc.execute(request, self.spy)

    def test_user_cannot_see_other_users_details(self):
        context.bookmark_repo.save(
            Bookmark('id1', self.user.id, 'test', 'web://test.com'))

        request = {
            'user_id': self.otheruser.id,
            'bookmark_id': 'id1',
        }

        with self.assertRaises(Exception):
            self.uc.execute(request, self.spy)

    def test_unknown_user_cannot_see_details(self):
        context.bookmark_repo.save(
            Bookmark('id1', self.user.id, 'test', 'web://test.com'))

        request = {
            'user_id': self.unknownuser.id,
            'bookmark_id': 'id1',
        }

        with self.assertRaises(Exception):
            self.uc.execute(request, self.spy)
