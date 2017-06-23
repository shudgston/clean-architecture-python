from datetime import datetime
from unittest import TestCase, mock

from links import exceptions
from links.context import context
from links.entities import Bookmark, User
from links.usecases.list_bookmarks import (
    ListBookmarksUseCase,
    ListBookmarksPresenter,
    ListBookmarksController
)
from .base import UseCaseTest, PresenterSpy, ControllerTestMixin


class ListBookmarksUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = User('user')
        self.otheruser = User('otheruser')
        self.unknownuser = User('unknownuser')
        context.user_repo.save(self.user)
        context.user_repo.save(self.otheruser)
        self.uc = ListBookmarksUseCase()
        self.presenter_spy = PresenterSpy()

    def test_user_with_one_bookmarks_sees_one(self):
        bookmark = Bookmark('0', self.user.id, 'name', 'url')
        context.bookmark_repo.save(bookmark)
        self.uc.list_bookmarks(self.user.id, self.presenter_spy)
        self.assertEqual(1, len(self.presenter_spy.response_model))

    def test_user_without_bookmarks_sees_none(self):
        self.uc.list_bookmarks(self.otheruser.id, self.presenter_spy)
        self.assertEqual(0, len(self.presenter_spy.response_model))

    def test_unknown_user_raises_exception(self):
        with self.assertRaises(exceptions.UserNotFound):
            self.uc.list_bookmarks(self.unknownuser, self.presenter_spy)

    @mock.patch('links.usecases.list_bookmarks.context')
    def test_repo_error_raises_exception(self, ctx):
        ctx.bookmark_repo.get_by_user.side_effect = Exception("Mocked Database Error")
        with self.assertRaises(exceptions.RepositoryError):
            self.uc.list_bookmarks(self.user, self.presenter_spy)


class ListBookmarksPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
            dt = datetime(year=2017, month=1, day=1)
            response = [
                {
                    'id': 'id1',
                    'name': 'test1',
                    'url': 'http://test.com',
                    'date_created': dt
                },
                {
                    'id': 'id2',
                    'name': 'test2',
                    'url': 'http://test.com',
                    'date_created': dt
                },
            ]
            presenter = ListBookmarksPresenter()
            presenter.present(response)
            expected = {
                'bookmark_id': 'id1',
                'name': 'test1',
                'url': 'http://test.com',
                'date_created': 'Jan 1, 2017',
                'date_created_iso': '2017-01-01T00:00:00',
                'host': 'test.com',
            }
            self.assertEqual(2, len(presenter.get_view_model()))
            self.assertDictEqual(expected, presenter.get_view_model()[0])


class ListBookmarksControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        self.mixin_setup()
        self.controller = ListBookmarksController(self.usecase, self.presenter, self.view)
        self.request = dict(user_id='user_id')

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.list_bookmarks.assert_called_with('user_id', self.presenter)
