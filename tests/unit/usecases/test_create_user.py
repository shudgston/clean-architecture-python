from unittest import TestCase, mock

from links.context import context
from links.entities import User
from links.security import create_password_hash
from links.usecases.create_user import CreateUserUseCase, CreateUserPresenter, CreateUserController
from tests.unit.usecases.base import UseCaseTest, PresenterSpy, ControllerTestMixin


class CreateUserUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.uc = CreateUserUseCase()
        self.presenter_spy = PresenterSpy()
        self.user = User('user')
        self.user.password_hash = create_password_hash('password')
        context.user_repo.save(self.user)

        self.request = {
            'username': 'user',
            'password': 'password'
        }

    def test_user_not_created_when_user_already_exists(self):
        self.uc.execute(self.request, self.presenter_spy)
        self.assertDictEqual(
            {
                'user_created': False,
                'username': 'user',
                'errors': {'username': ['That username is taken']}
            },
            self.presenter_spy.response_model
        )

    def test_invalid_username_is_rejected(self):
        self.request['username'] = 'user!@#$'
        self.uc.execute(self.request, self.presenter_spy)
        self.assertDictEqual(
            {
                'user_created': False,
                'username': 'user!@#$',
                'errors': {'username': ['Username is not allowed']}
            },
            self.presenter_spy.response_model
        )

    def test_user_is_created(self):
        self.request['username'] = 'newuser'
        self.uc.execute(self.request, self.presenter_spy)
        self.assertDictEqual(
            {
                'user_created': True,
                'username': 'newuser',
                'errors': {}
            },
            self.presenter_spy.response_model
        )
        user = context.user_repo.get('newuser')
        self.assertEqual('newuser', user.id)


class CreateUserPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = {'user_created': True, 'username': 'user'}
        presenter = CreateUserPresenter()
        presenter.present(response)
        self.assertDictEqual(response, presenter.get_view_model())

    def test_presenter_shows_error_on_failure(self):
        response = {'user_created': True, 'username': 'user'}
        presenter = CreateUserPresenter()
        presenter.present(response)
        self.assertDictEqual(response, presenter.get_view_model())


class CreateUserControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        self.mixin_setup()
        self.controller = CreateUserController(self.usecase, self.presenter, self.view)
        self.request = {'username': 'user', 'password': 'password'}

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.execute.assert_called_with(
            {
                'username': 'user',
                'password': 'password',
            },
            self.presenter
        )
