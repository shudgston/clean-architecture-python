from datetime import datetime
from unittest import TestCase, mock

from links.context import context
from links import exceptions
from links.entities import Bookmark, User
from links.usecases.list_bookmarks import ListBookmarksUseCase, ListBookmarksPresenter, ListBookmarksController
from .base import UseCaseTest


class ListBookmarksUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = User('user')
        self.otheruser = User('otheruser')
        self.unknownuser = User('unknownuser')
        context.user_repo.save(self.user)
        context.user_repo.save(self.otheruser)
        self.uc = ListBookmarksUseCase()

    def test_user_with_one_bookmarks_sees_one(self):
        bookmark = Bookmark('0', self.user.id, 'name', 'url')
        context.bookmark_repo.save(bookmark)
        rv = self.uc.list_bookmarks(self.user.id)
        self.assertEqual(len(rv), 1)

    def test_user_without_bookmarks_sees_none(self):
        rv = self.uc.list_bookmarks(self.otheruser.id)
        self.assertEqual(len(rv), 0)

    def test_unknown_user_raises_exception(self):
        with self.assertRaises(exceptions.UserNotFound):
            self.uc.list_bookmarks(self.unknownuser)

    @mock.patch('links.usecases.list_bookmarks.context')
    def test_repo_error_raises_exception(self, ctx):
        ctx.bookmark_repo.get_by_user.side_effect = Exception("Mocked Database Error")
        with self.assertRaises(exceptions.RepositoryError):
            self.uc.list_bookmarks(self.user)


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
                'slug': 'test1',
            }
            self.assertEqual(2, len(presenter.get_view_model()))
            self.assertDictEqual(expected, presenter.get_view_model()[0])


class ListBookmarksControllerTest(TestCase):

    def setUp(self):
        self.usecase = mock.Mock()
        self.presenter = mock.Mock()
        self.view = mock.Mock()
        self.controller = ListBookmarksController(self.usecase, self.presenter, self.view)
        self.request = dict(user_id='user_id', filterkey='all')

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.list_bookmarks.assert_called_with('user_id', filterkey='all')

    def test_controller_passes_response_model_to_presenter(self):
        response = {
            'id': 'id',
            'name': 'test1',
            'url': 'http://test.com',
            'date_created': datetime.utcnow(),
        }
        self.usecase.list_bookmarks.return_value = response
        self.controller.handle(self.request)
        self.presenter.present.assert_called_with(response)

    def test_controller_passes_view_model_to_view(self):
        view_model = {'fake_view_model': True}
        self.presenter.get_view_model.return_value = view_model
        self.controller.handle(self.request)
        self.view.generate_view.assert_called_with(view_model)
