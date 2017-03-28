from unittest import TestCase

from links.context import context
from links.entities import User
from links.usecases.bookmarks import CreateBookmarkUseCase
from .spies import PresenterSpy
from ..helpers import setup_testing_context


class CreateBookmarkUseCaseTest(TestCase):

    def setUp(self):
        setup_testing_context()
        self.user = User('user')
        context.user_repo.save(self.user)
        self.uc = CreateBookmarkUseCase()
        self.spy = PresenterSpy()

    def test_unknown_user_cannot_create_bookmark(self):
        with self.assertRaises(Exception):
            self.uc.create_bookmark('unknown', 'test', 'web://test.com', self.spy)

    def test_user_can_create_bookmark(self):
        self.uc.create_bookmark(self.user.id, 'test', 'web://test.com', self.spy)
        self.assertTrue(isinstance(self.spy.response_model.bookmark_id, str))

    def test_invalid_values_are_caught(self):
        self.uc.create_bookmark(self.user.id, 'test', 'gobbledigook', self.spy)
        self.assertEqual(
            self.spy.response_model.errors,
            {'url': ['Not a valid URL']})
