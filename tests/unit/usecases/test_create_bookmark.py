from unittest import TestCase, mock
from datetime import datetime

from links.context import context
from links.entities import User
from links.exceptions import UserNotFound
from links.usecases.create_bookmark import CreateBookmarkUseCase, CreateBookmarkPresenter, \
    CreateBookmarkResponse, CreateBookmarkController
from .base import UseCaseTest


class CreateBookmarkUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = User('user')
        context.user_repo.save(self.user)
        self.uc = CreateBookmarkUseCase()

    def test_unknown_user_cannot_create_bookmark(self):
        with self.assertRaises(UserNotFound):
            self.uc.create_bookmark('unknown', 'test', 'http://test.com')

    def test_user_can_create_bookmark(self):
        rv = self.uc.create_bookmark(self.user.id, 'test', 'http://test.com')
        self.assertTrue(isinstance(rv.bookmark_id, str))

    def test_invalid_values_are_caught(self):
        rv = self.uc.create_bookmark(self.user.id, 'test', 'gobbledigook')
        self.assertEqual(rv.errors, {'url': ['Not a valid URL']})


class CreateBookmarkPresentationTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = CreateBookmarkResponse('id1', {})
        presenter = CreateBookmarkPresenter()
        presenter.present(response)
        expected = {'bookmark_id': 'id1', 'errors': {}}
        self.assertDictEqual(expected, presenter.get_view_model())


class CreateBookmarkControllerTest(TestCase):

    def setUp(self):
        self.usecase = mock.Mock()
        self.presenter = mock.Mock()
        self.view = mock.Mock()
        self.controller = CreateBookmarkController(self.usecase, self.presenter, self.view)
        self.request = {'user_id': 'id', 'name': 'name', 'url': 'url'}

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.create_bookmark.assert_called_with('id', 'name', 'url')

    def test_controller_passes_response_model_to_presenter(self):
        response = CreateBookmarkResponse('id', {})
        self.usecase.create_bookmark.return_value = response
        self.controller.handle(self.request)
        self.presenter.present.assert_called_with(response)

    def test_controller_passes_view_model_to_view(self):
        view_model = {'fake_view_model': True}
        self.presenter.get_view_model.return_value = view_model
        self.controller.handle(self.request)
        self.view.generate_view.assert_called_with(view_model)
