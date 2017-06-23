import datetime
from unittest import TestCase, mock

from links.context import context
from links.entities import User, Bookmark
from links.exceptions import BookmarkNotFound
from links.usecases.bookmark_details import BookmarkDetailsUseCase, BookmarkDetailsPresenter, \
    BookmarkDetailsController
from .base import UseCaseTest, PresenterSpy, ControllerTestMixin


class BookmarkDetailsUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = User('user')
        self.otheruser = User('otheruser')
        self.unknownuser = User('unknownuser')
        context.user_repo.save(self.user)
        context.user_repo.save(self.otheruser)
        self.uc = BookmarkDetailsUseCase()
        self.presenter_spy = PresenterSpy()

    def test_user_with_bookmark_can_see_details(self):
        now = datetime.datetime.utcnow()
        context.bookmark_repo.save(
            Bookmark('id1', self.user.id, 'test', 'http://test.com', date_created=now))

        self.uc.get_bookmark_details(self.user.id, 'id1', self.presenter_spy)

        self.assertTrue(self.presenter_spy.present_called)
        self.assertDictEqual(
            {
                'id': 'id1',
                'user_id': 'user',
                'name': 'test',
                'url': 'http://test.com',
                'date_created': now
            },
            self.presenter_spy.response_model
        )

    def test_user_with_none_cannot_see_details(self):
        with self.assertRaises(BookmarkNotFound):
            self.uc.get_bookmark_details(self.user.id, 'id1', self.presenter_spy)

    def test_user_cannot_see_other_users_details(self):
        context.bookmark_repo.save(
            Bookmark('id1', self.user.id, 'test', 'http://test.com'))

        with self.assertRaises(BookmarkNotFound):
            self.uc.get_bookmark_details(self.otheruser.id, 'id1', self.presenter_spy)

    def test_unknown_user_cannot_see_details(self):
        context.bookmark_repo.save(
            Bookmark('id1', self.user.id, 'test', 'http://test.com'))

        with self.assertRaises(BookmarkNotFound):
            self.uc.get_bookmark_details(self.unknownuser.id, 'id1', self.presenter_spy)


class BookmarkDetailsPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
        now = datetime.datetime(year=2017, month=1, day=1)
        response = {
            'id': 'id',
            'name': 'name',
            'url': 'http://test.com',
            'date_created': now
        }
        presenter = BookmarkDetailsPresenter()
        presenter.present(response)
        view_model = {
            'bookmark_id': 'id',
            'name': 'name',
            'url': 'http://test.com',
            'date_created': 'Jan 1, 2017',
            'date_created_iso': '2017-01-01T00:00:00',
            'host': 'test.com',
        }
        self.assertDictEqual(view_model, presenter.get_view_model())


class BookmarkDetailsControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        self.mixin_setup()
        self.controller = BookmarkDetailsController(self.usecase, self.presenter, self.view)
        self.request = {'user_id': 'user_id', 'bookmark_id': 'bookmark_id'}

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.get_bookmark_details.assert_called_with(
            'user_id', 'bookmark_id', self.presenter
        )

