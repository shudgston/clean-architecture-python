import datetime
from unittest import TestCase

from links import entities
from links.context import context
from links.exceptions import BookmarkNotFound
from links.usecases import bookmarks
from .base import UseCaseTest, PresenterSpy, UseCaseSpy, ViewSpy, ViewModelDouble


class BookmarkDetailsUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = entities.User('user')
        self.otheruser = entities.User('otheruser')
        self.unknownuser = entities.User('unknownuser')
        context.user_repo.save(self.user)
        context.user_repo.save(self.otheruser)

        self.usecase = bookmarks.BookmarkDetailsUseCase(self.user.id, 'id1')
        self.presenter_spy = PresenterSpy()

    def test_user_with_bookmark_can_see_details(self):
        now = datetime.datetime.utcnow()
        context.bookmark_repo.save(
            entities.Bookmark('id1', self.user.id, 'test', 'http://test.com', date_created=now))

        self.usecase.execute(self.presenter_spy)
        rm = self.presenter_spy.response_model
        self.assertEqual(rm.id, 'id1')
        self.assertEqual(rm.name, 'test')
        self.assertEqual(rm.url, 'http://test.com')
        self.assertEqual(rm.date_created, now)

    def test_user_with_none_cannot_see_details(self):
        with self.assertRaises(BookmarkNotFound):
            self.usecase.execute(self.presenter_spy)

    def test_user_cannot_see_other_users_details(self):
        context.bookmark_repo.save(
            entities.Bookmark('id1', self.user.id, 'test', 'http://test.com'))

        self.usecase.user_id = self.otheruser.id

        with self.assertRaises(BookmarkNotFound):
            self.usecase.execute(self.presenter_spy)

    def test_unknown_user_cannot_see_details(self):
        context.bookmark_repo.save(
            entities.Bookmark('id1', self.user.id, 'test', 'http://test.com'))

        self.usecase.user_id = self.unknownuser.id

        with self.assertRaises(BookmarkNotFound):
            self.usecase.execute(self.presenter_spy)


class BookmarkDetailsPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = bookmarks.Bookmark(
            id='id',
            name='name',
            url='http://test.com',
            date_created=datetime.datetime(year=2017, month=1, day=21)
        )

        presenter = bookmarks.BookmarkDetailsPresenter()
        presenter.present(response)

        view_model = presenter.get_view_model()
        self.assertEqual(view_model.id, 'id')
        self.assertEqual(view_model.name, 'name')
        self.assertEqual(view_model.url, 'http://test.com')
        self.assertEqual(view_model.date_created, '2017-01-21T00:00:00')

#
# class BookmarkDetailsControllerTest(ControllerTestMixin, TestCase):
#
#     def setUp(self):
#         self.mixin_setup()
#         self.controller = BookmarkDetailsController(
#             self.usecase,
#             self.presenter,
#             self.view
#         )
#         self.request = {
#             'user_id': 'test-user',
#             'bookmark_id': '123',
#         }
#
#     def test_usecase_is_called(self):
#         self.controller.handle(self.request)
#         self.usecase.execute.assert_called_with(self.presenter)
#         self.assertEqual(self.usecase.user_id, 'test-user')
#         self.assertEqual(self.usecase.bookmark_id, '123')


class BookmarkDetailsControllerTest(TestCase):

    def setUp(self):
        self.usecase_spy = UseCaseSpy()
        self.presenter_spy = PresenterSpy()
        self.view_spy = ViewSpy()
        self.controller = bookmarks.BookmarkDetailsController(
            self.usecase_spy,
            self.presenter_spy,
            self.view_spy
        )

    def test_usecase_invocation(self):
        req = {
            'user_id': 'test-user',
            'bookmark_id': '123',
        }
        self.controller.handle(req)
        print(self.usecase_spy.__dict__)
        self.assertEqual(self.usecase_spy.user_id, req['user_id'])
        self.assertEqual(self.usecase_spy.bookmark_id, req['bookmark_id'])

    def test_view_receives_view_model(self):
        req = {
            'user_id': 'test-user',
            'bookmark_id': '123',
        }
        self.presenter_spy.view_model = ViewModelDouble
        self.controller.handle(req)
        self.assertTrue(self.view_spy.generate_view_was_called)
        self.assertIs(self.view_spy.view_model, self.presenter_spy.view_model)
