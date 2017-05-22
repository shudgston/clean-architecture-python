from unittest import TestCase, mock
from datetime import datetime

from links.context import context
from links.entities import Bookmark, User
from links.exceptions import UserNotFound
from links.usecases.edit_bookmark import EditBookmarkUseCase, EditBookmarkPresenter, \
    EditBookmarkController
from .base import UseCaseTest


class EditBookmarkUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = User('user')
        context.user_repo.save(self.user)

        self.bookmark = Bookmark('id1', self.user.id, 'name', 'http://test.com')
        context.bookmark_repo.save(self.bookmark)

        self.uc = EditBookmarkUseCase()

    def test_user_can_edit_bookmark(self):
        rv = self.uc.edit_bookmark(self.user.id, self.bookmark.id, 'name changed', 'http://test.com')
        self.assertTrue(isinstance(rv, dict))
        self.assertIn('bookmark_id', rv)

    def test_user_can_edit_another_users_bookmark(self):
        rv = self.uc.edit_bookmark('other_user', self.bookmark.id, 'name changed', 'http://test.com')
        self.assertTrue(isinstance(rv, dict))
        self.assertIn('error', rv)

    def test_unknown_user_cannot_edit_bookmark(self):
        rv = self.uc.edit_bookmark('unknown', 'id1', 'test', 'http://test.com')
        self.assertTrue(isinstance(rv, dict))
        self.assertIn('error', rv)

    def test_invalid_values_are_caught(self):
        rv = self.uc.edit_bookmark(self.user.id, self.bookmark.id, 'test', 'gobbledigook')
        self.assertEqual(rv['error'], {'url': ['Not a valid URL']})


# class EditBookmarkPresentationTest(TestCase):

#     def test_presenter_creates_view_model(self):
#         response = EditBookmarkResponse('id1', {})
#         presenter = EditBookmarkPresenter()
#         presenter.present(response)
#         expected = {'bookmark_id': 'id1', 'errors': {}}
#         self.assertDictEqual(expected, presenter.get_view_model())


# class EditBookmarkControllerTest(TestCase):

#     def setUp(self):
#         self.usecase = mock.Mock()
#         self.presenter = mock.Mock()
#         self.view = mock.Mock()
#         self.controller = EditBookmarkController(self.usecase, self.presenter, self.view)
#         self.request = {'user_id': 'id', 'name': 'name', 'url': 'url'}

#     def test_usecase_is_called(self):
#         self.controller.handle(self.request)
#         self.usecase.edit_bookmark.assert_called_with('id', 'name', 'url')

#     def test_controller_passes_response_model_to_presenter(self):
#         response = EditBookmarkResponse('id', {})
#         self.usecase.edit_bookmark.return_value = response
#         self.controller.handle(self.request)
#         self.presenter.present.assert_called_with(response)

#     def test_controller_passes_view_model_to_view(self):
#         view_model = {'fake_view_model': True}
#         self.presenter.get_view_model.return_value = view_model
#         self.controller.handle(self.request)
#         self.view.generate_view.assert_called_with(view_model)
