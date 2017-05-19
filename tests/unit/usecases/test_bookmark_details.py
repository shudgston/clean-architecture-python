import datetime
from unittest import TestCase, mock

from links.context import context
from links.entities import User, Bookmark
from links.exceptions import BookmarkNotFound
from links.usecases.bookmark_details import BookmarkDetailsUseCase, BookmarkDetailsPresenter, \
    BookmarkDetails, BookmarkDetailsController
from .base import UseCaseTest


class BookmarkDetailsUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = User('user')
        self.otheruser = User('otheruser')
        self.unknownuser = User('unknownuser')
        context.user_repo.save(self.user)
        context.user_repo.save(self.otheruser)
        self.uc = BookmarkDetailsUseCase()

    def test_user_with_bookmark_can_see_details(self):
        now = datetime.datetime.utcnow()
        context.bookmark_repo.save(
            Bookmark('id1', self.user.id, 'test', 'http://test.com', date_created=now))

        rv = self.uc.get_bookmark_details(self.user.id, 'id1')
        self.assertEqual(rv.bookmark_id, 'id1')
        self.assertEqual(rv.name, 'test')
        self.assertEqual(rv.url, 'http://test.com')
        self.assertEqual(rv.date_created, now)

    def test_user_with_none_cannot_see_details(self):
        with self.assertRaises(BookmarkNotFound):
            self.uc.get_bookmark_details(self.user.id, 'id1')

    def test_user_cannot_see_other_users_details(self):
        context.bookmark_repo.save(
            Bookmark('id1', self.user.id, 'test', 'http://test.com'))

        with self.assertRaises(Exception):
            self.uc.get_bookmark_details(self.otheruser.id, 'id1')

    def test_unknown_user_cannot_see_details(self):
        context.bookmark_repo.save(
            Bookmark('id1', self.user.id, 'test', 'http://test.com'))

        with self.assertRaises(BookmarkNotFound):
            self.uc.get_bookmark_details(self.unknownuser.id, 'id1')


class BookmarkDetailsPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
        now = datetime.datetime(year=2017, month=1, day=1)
        response = BookmarkDetails('id', 'name', 'http://test.com', now)
        presenter = BookmarkDetailsPresenter()
        presenter.present(response)
        view_model = {
            'bookmark_id': 'id',
            'name': 'name',
            'url': 'http://test.com',
            'date_created': 'Jan 1, 2017',
            'date_created_iso': '2017-01-01T00:00:00',
            'host': 'test.com'
        }
        self.assertEqual(view_model, presenter.get_view_model())


class BookmarkDetailsControllerTest(TestCase):

    def setUp(self):
        self.usecase = mock.Mock()
        self.presenter = mock.Mock()
        self.view = mock.Mock()
        self.controller = BookmarkDetailsController(self.usecase, self.presenter, self.view)
        self.request = {'user_id': 'user_id', 'bookmark_id': 'bookmark_id'}

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.get_bookmark_details.assert_called_with('user_id', 'bookmark_id')

    def test_controller_passes_response_model_to_presenter(self):
        response = BookmarkDetails('id', 'name', 'url', datetime.datetime.utcnow())
        self.usecase.get_bookmark_details.return_value = response
        self.controller.handle(self.request)
        self.presenter.present.assert_called_with(response)

    def test_controller_passes_view_model_to_view(self):
        view_model = {'fake_view_model': True}
        self.presenter.get_view_model.return_value = view_model
        self.controller.handle(self.request)
        self.view.generate_view.assert_called_with(view_model)

