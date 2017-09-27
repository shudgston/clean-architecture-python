from unittest import TestCase, mock

from links.context import context
from links.entities import User
from links.security import create_password_hash
from links.usecases.authenticate_user import (
    AuthenticateUserUseCase,
    AuthenticateUserPresenter,
    AuthenticateUserController,
    Response
)
from .base import UseCaseTest, PresenterSpy, ControllerTestMixin


class AuthenticateUserUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = User('user')
        self.user.password_hash = create_password_hash('password')
        context.user_repo.save(self.user)

        self.uc = AuthenticateUserUseCase()
        self.uc.user_id = self.user.id
        self.uc.password = 'password'

        self.presenter_spy = PresenterSpy()

    def test_user_with_correct_password_can_auth(self):
        self.uc.execute(self.presenter_spy)
        self.assertTrue(self.presenter_spy.response_model.is_authenticated)
        self.assertEqual(self.presenter_spy.response_model.user_id, self.uc.user_id)

    def test_user_with_wrong_password_cannot_auth(self):
        self.uc.password = 'wrong'
        self.uc.execute(self.presenter_spy)
        self.assertFalse(self.presenter_spy.response_model.is_authenticated)
        self.assertEqual(self.presenter_spy.response_model.user_id, self.uc.user_id)


class AuthenticateUserPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = Response()
        response.is_authenticated = True
        response.user_id = 'testuser'

        presenter = AuthenticateUserPresenter()
        presenter.present(response)

        self.assertDictEqual(
            {
                'is_authenticated': True,
                'user_id': 'testuser'
            },
            presenter.get_view_model()
        )


class AuthenticateUserControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        self.mixin_setup()
        self.controller = AuthenticateUserController(
            self.usecase,
            self.presenter,
            self.view
        )
        self.request = {'user_id': 'testuser', 'password': 'password'}

    def test_usecase_invocation(self):
        self.controller.handle(self.request)
        self.usecase.execute.assert_called_with(self.presenter)
        self.assertEqual(self.usecase.user_id, self.request['user_id'])
        self.assertEqual(self.usecase.password, self.request['password'])