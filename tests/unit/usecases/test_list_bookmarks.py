import unittest
from unittest import mock

from links.context import context
from links.entities import Bookmark, User
from links.usecases.bookmarks import ListBookmarksUseCase
from .spies import PresenterSpy
from ..helpers import setup_testing_context


class ListBookmarksUseCaseSpy:

    execute_called = False
    requested_user = None

    def execute(self, request, presenter):
        self.execute_called = True
        self.requested_user = request.get('user_id')


class ListBookmarksUseCaseTest(unittest.TestCase):

    def setUp(self):
        setup_testing_context()
        self.user = User('user')
        self.otheruser = User('otheruser')
        self.unknownuser = User('unknownuser')
        context.user_repo.save(self.user)
        context.user_repo.save(self.otheruser)
        self.uc = ListBookmarksUseCase()

    def test_user_with_one_bookmarks_sees_one(self):
        bookmark = Bookmark('0', self.user.id, 'name', 'url')
        context.bookmark_repo.save(bookmark)
        presenter_spy = PresenterSpy()
        self.uc.list_bookmarks(self.user.id, presenter_spy)
        self.assertEqual(len(presenter_spy.response_model), 1)

    def test_user_without_bookmarks_sees_none(self):
        presenter_spy = PresenterSpy()
        self.uc.list_bookmarks(self.otheruser.id, presenter_spy)
        self.assertEqual(len(presenter_spy.response_model), 0)

    def test_unknown_user_sees_none(self):
        presenter_spy = PresenterSpy()
        self.uc.list_bookmarks(self.unknownuser.id, presenter_spy)
        self.assertEqual(len(presenter_spy.response_model), 0)

    def test_exception_handling(self):
        context.bookmark_repo = mock.Mock()
        context.bookmark_repo.get_by_user.side_effect = Exception('Mocked Internal Error')

        bookmark = Bookmark('0', self.user.id, 'name', 'url')
        context.bookmark_repo.save(bookmark)
        presenter_spy = PresenterSpy()
        request = {'user_id': self.user.id}

        with self.assertRaises(Exception):
            self.uc.execute(request, presenter_spy)


# class ListBookmarksPresenterTest(unittest.TestCase):
#
#     def test_present_formats_viewmodel(self):
#         date_created = datetime.datetime(year=2017, month=1, day=1)
#         response_model = [
#             BookmarkDetails('id1', 'name1', 'url1', date_created),
#             BookmarkDetails('id2', 'name2', 'url2', date_created),
#             BookmarkDetails('id3', 'name3', 'url3', date_created),
#             ]
#
#         presenter = ListBookmarksPresenter()
#         presenter.present(response_model)
#         viewmodel = presenter.get_view_model()
#
#         print(viewmodel)
#
#         row1 = viewmodel[0]
#         print(row1)
#         self.assertEqual(row1.bookmark_id, 'id1')
#         self.assertEqual(row1.name, 'name1')
#         self.assertEqual(row1.url, 'url1')
#         self.assertEqual(row1.date_created, 'Jan 1, 2017')
#         self.assertEqual(row1.date_created_iso, '2017-01-01T00:00:00')


# class ListBookmarksControllerTest(unittest.TestCase):
#
#     def setUp(self):
#         setup_testing_context()
#         self.user = User('user')
#         context.user_repo.save(self.user)
#         self.presenter_spy = PresenterSpy()
#         self.view_spy = ViewSpy()
#         self.usecase_spy = ListBookmarksUseCaseSpy()
#
#     def test_usecase_invocation(self):
#         request = {'user_id': self.user.id}
#         controller = ListBookmarksController(
#             self.usecase_spy, self.presenter_spy, self.view_spy)
#
#         controller.handle(request)
#         self.assertTrue(self.usecase_spy.execute_called)
#         self.assertEqual(self.usecase_spy.requested_user, self.user.id)
#
#     def test_controller_sends_view_model_to_the_view(self):
#         # Init a fake value for the presenter's view model.
#         # This value should end up in the view.
#         self.presenter_spy._view_model = {'test_value': uuid.uuid4().hex}
#         controller = ListBookmarksController(
#             self.usecase_spy, self.presenter_spy, self.view_spy)
#
#         controller.handle({})
#         self.assertTrue(self.view_spy.generate_view_called)
#         self.assertEqual(self.presenter_spy.get_view_model(), self.view_spy.view_model)
