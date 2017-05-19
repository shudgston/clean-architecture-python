from unittest import TestCase, mock

from links.context import context
from links.entities import User
from links.security import create_password_hash
from links.usecases.authenticate_user import AuthenticateUserUseCase, AuthenticateUserPresenter, \
    AuthenticateUserController
from .base import UseCaseTest


class AuthenticateUserUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.uc = AuthenticateUserUseCase()
        self.user = User('user')
        self.user.password_hash = create_password_hash('password')
        context.user_repo.save(self.user)

    def test_user_with_correct_password_can_auth(self):
        rv = self.uc.authenticate_user('user', 'password')
        self.assertTrue(rv['is_authenticated'])
        self.assertEqual('user', rv['user_id'])

    def test_user_with_wrong_password_cannot_auth(self):
        rv = self.uc.authenticate_user('user', 'wrong')
        self.assertFalse(rv['is_authenticated'])
        self.assertEqual('user', rv['user_id'])


class AuthenticateUserPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = {'is_authenticated': True, 'user_id': 'id'}
        presenter = AuthenticateUserPresenter()
        presenter.present(response)
        self.assertEqual({'is_authenticated': True, 'user_id': 'id'}, presenter.get_view_model())


class AuthenticateUserControllerTest(TestCase):

    def setUp(self):
        self.usecase = mock.Mock()
        self.presenter = mock.Mock()
        self.view = mock.Mock()
        self.controller = AuthenticateUserController(self.usecase, self.presenter, self.view)
        self.request = {'username': 'user', 'password': 'password'}

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.authenticate_user.assert_called_with('user', 'password')

    def test_controller_passes_response_model_to_presenter(self):
        response = {'is_authenticated': True}
        self.usecase.authenticate_user.return_value = response
        self.controller.handle(self.request)
        self.presenter.present.assert_called_with(response)

    def test_controller_passes_view_model_to_view(self):
        view_model = {'fake_view_model': True}
        self.presenter.get_view_model.return_value = view_model
        self.controller.handle(self.request)
        self.view.generate_view.assert_called_with(view_model)
