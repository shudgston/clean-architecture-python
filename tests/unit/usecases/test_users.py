from unittest import TestCase, mock

from links.context import context
from links.entities import User
from links.security import create_password_hash
from links.usecases.users import AuthenticateUserUseCase
from tests.unit.helpers import setup_testing_context
from tests.unit.usecases.spies import PresenterSpy


class AuthenticateUserUseCaseTest(TestCase):

    def setUp(self):
        setup_testing_context()
        self.uc = AuthenticateUserUseCase()
        self.spy = PresenterSpy()
        self.user = User('user')
        self.user.password_hash = create_password_hash('password')
        context.user_repo.save(self.user)

    def test_user_with_correct_password_can_auth(self):
        self.uc.authenticate_user('user', 'password', self.spy)
        self.assertTrue(self.spy.present_called)
        self.assertTrue(self.spy.response_model)

    def test_user_with_wrong_password_cannot_auth(self):
        self.uc.authenticate_user('user', 'wrong', self.spy)
        self.assertTrue(self.spy.present_called)
        self.assertFalse(self.spy.response_model)
