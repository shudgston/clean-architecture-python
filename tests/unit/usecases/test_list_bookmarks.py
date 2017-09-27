from datetime import datetime
from unittest import TestCase, mock

from links import entities
from links import exceptions
from links.context import context
from links.usecases import bookmarks
from .base import UseCaseTest, PresenterSpy, UseCaseSpy, ViewSpy, ViewModelDouble


class ListBookmarksUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = entities.User('user')
        self.otheruser = entities.User('otheruser')
        self.unknownuser = entities.User('unknownuser')
        context.user_repo.save(self.user)
        context.user_repo.save(self.otheruser)

        self.presenter_spy = PresenterSpy()
        self.usecase = bookmarks.ListBookmarksUseCase(user_id=self.user.id)

    def test_user_with_one_bookmarks_sees_one(self):
        bookmark = entities.Bookmark('test-id', self.user.id, 'name', 'http://test.com')
        context.bookmark_repo.save(bookmark)
        self.usecase.execute(self.presenter_spy)
        self.assertEqual(1, len(self.presenter_spy.response_model))

        bm = self.presenter_spy.response_model[0]
        self.assertEqual(bm.id, 'test-id')
        self.assertEqual(bm.name, 'name')
        self.assertEqual(bm.url, 'http://test.com')

    def test_user_without_bookmarks_sees_none(self):
        self.usecase.execute(self.presenter_spy)
        self.assertEqual(0, len(self.presenter_spy.response_model))

    def test_unknown_user_raises_exception(self):
        self.usecase.user_id = self.unknownuser.id
        with self.assertRaises(exceptions.UserNotFound):
            self.usecase.execute(self.presenter_spy)

    @mock.patch('links.usecases.bookmarks.context')
    def test_repo_error_raises_exception(self, ctx):
        ctx.bookmark_repo.get_by_user.side_effect = Exception("Mocked Database Error")
        with self.assertRaises(exceptions.RepositoryError):
            self.usecase.execute(self.presenter_spy)


class ListBookmarksPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
        dt = datetime(year=2017, month=1, day=1)

        response = [
            bookmarks.Bookmark(
                id='id1',
                name='test1',
                url='http://test.com',
                date_created=dt
            ),
            bookmarks.Bookmark(
                id='id2',
                name='test2',
                url='http://test.com',
                date_created=dt
            )
        ]

        presenter = bookmarks.ListBookmarksPresenter()
        presenter.present(response)
        view_model = presenter.get_view_model()

        first = view_model[0]
        self.assertEqual(first.id, 'id1')
        self.assertEqual(first.name, 'test1')
        self.assertEqual(first.url, 'http://test.com')
        self.assertEqual(first.date_created, dt.isoformat())

        second = view_model[1]
        self.assertEqual(second.id, 'id2')
        self.assertEqual(second.name, 'test2')
        self.assertEqual(second.url, 'http://test.com')
        self.assertEqual(second.date_created, dt.isoformat())


class ListBookmarksControllerTest(TestCase):

    def setUp(self):
        self.usecase_spy = UseCaseSpy()
        self.presenter_spy = PresenterSpy()
        self.view_spy = ViewSpy()
        self.controller = bookmarks.ListBookmarksController(
            self.usecase_spy,
            self.presenter_spy,
            self.view_spy
        )

    def test_usecase_invocation(self):
        req = {'user_id': 'test-user'}
        self.controller.handle(req)
        self.assertEqual(self.usecase_spy.user_id, 'test-user')

    def test_view_receives_view_model(self):
        req = {'user_id': 'test-user'}
        self.presenter_spy.view_model = ViewModelDouble
        self.controller.handle(req)
        self.assertTrue(self.view_spy.generate_view_was_called)
        self.assertIs(self.view_spy.view_model, self.presenter_spy.view_model)
