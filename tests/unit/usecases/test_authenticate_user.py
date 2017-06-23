from unittest import TestCase, mock

from links.context import context
from links.entities import User
from links.security import create_password_hash
from links.usecases.authenticate_user import (
    AuthenticateUserUseCase,
    AuthenticateUserPresenter,
    AuthenticateUserController
)
from .base import UseCaseTest, PresenterSpy, ControllerTestMixin


class AuthenticateUserUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.uc = AuthenticateUserUseCase()
        self.user = User('user')
        self.user.password_hash = create_password_hash('password')
        self.presenter_spy = PresenterSpy()
        context.user_repo.save(self.user)

    def test_user_with_correct_password_can_auth(self):
        self.uc.authenticate_user('user', 'password', self.presenter_spy)
        self.assertDictEqual(
            {
                'is_authenticated': True,
                'user_id': 'user'
            },
            self.presenter_spy.response_model
        )

    def test_user_with_wrong_password_cannot_auth(self):
        self.uc.authenticate_user('user', 'wrong', self.presenter_spy)
        self.assertDictEqual(
            {
                'is_authenticated': False,
                'user_id': 'user'
            },
            self.presenter_spy.response_model
        )


class AuthenticateUserPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = {'is_authenticated': True, 'user_id': 'id'}
        presenter = AuthenticateUserPresenter()
        presenter.present(response)
        self.assertDictEqual(
            {
                'is_authenticated': True,
                'user_id': 'id'
            },
            presenter.get_view_model()
        )


class AuthenticateUserControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        self.mixin_setup()
        self.controller = AuthenticateUserController(self.usecase, self.presenter, self.view)
        self.request = {'username': 'user', 'password': 'password'}

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.authenticate_user.assert_called_with('user', 'password', self.presenter)

