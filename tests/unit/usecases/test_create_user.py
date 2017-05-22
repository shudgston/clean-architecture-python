from unittest import TestCase, mock

from links.context import context
from links.entities import User
from links.security import create_password_hash
from links.usecases.create_user import CreateUserUseCase, CreateUserPresenter, CreateUserController
from .base import UseCaseTest


class CreateUserUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.uc = CreateUserUseCase()
        self.user = User('user')
        self.user.password_hash = create_password_hash('password')
        context.user_repo.save(self.user)

    def test_user_not_created_when_user_already_exists(self):
        rv = self.uc.create_user('user', 'password')
        self.assertEqual({'user_created': False, 'username': 'user'}, rv)

    def test_user_is_created(self):
        rv = self.uc.create_user('newuser', 'password')
        self.assertEqual({'user_created': True, 'username': 'newuser'}, rv)
        user = context.user_repo.get('newuser')
        self.assertEqual('newuser', user.id)


class CreateUserPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
        presenter = CreateUserPresenter()
        response = True
        presenter.present(response)
        self.assertIs(True, presenter.get_view_model())

    def test_presenter_shows_error_on_failure(self):
        presenter = CreateUserPresenter()
        response = False
        presenter.present(response)
        self.assertIs(False, presenter.get_view_model())


class CreateUserControllerTest(TestCase):

    def setUp(self):
        self.usecase = mock.Mock()
        self.presenter = mock.Mock()
        self.view = mock.Mock()
        self.controller = CreateUserController(self.usecase, self.presenter, self.view)
        self.request = {'username': 'user', 'password': 'password'}

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.create_user.assert_called_with('user', 'password')

    def test_controller_passes_response_model_to_presenter(self):
        response = True
        self.usecase.create_user.return_value = response
        self.controller.handle(self.request)
        self.presenter.present.assert_called_with(response)

    def test_controller_passes_view_model_to_view(self):
        view_model = {'fake_view_model': True}
        self.presenter.get_view_model.return_value = view_model
        self.controller.handle(self.request)
        self.view.generate_view.assert_called_with(view_model)
