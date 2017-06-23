from abc import ABCMeta, abstractmethod

from links.context import context
from links.logger import get_logger
from links.security import check_password
from links.usecases.interfaces import OutputBoundary, Controller

LOGGER = get_logger(__name__)


class AuthenticateUserInputBoundary(metaclass=ABCMeta):

    @abstractmethod
    def authenticate_user(self, user_id, password, presenter):
        pass


class AuthenticateUserUseCase(AuthenticateUserInputBoundary):

    def authenticate_user(self, user_id, password, presenter):
        """
        :param user_id:
        :param password:
        :param presenter:
        :return:
        """
        response = {'is_authenticated': False, 'user_id': user_id}
        password_hash = context.user_repo.get_password_hash(user_id)

        if context.user_repo.exists(user_id):
            if check_password(password, password_hash):
                response['is_authenticated'] = True

        presenter.present(response)


class AuthenticateUserPresenter(OutputBoundary):

    def __init__(self):
        self.view_model = False

    def present(self, response_model):
        self.view_model = response_model

    def get_view_model(self):
        return self.view_model


class AuthenticateUserController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        self.usecase.authenticate_user(
            request['username'],
            request['password'],
            self.presenter
        )
        return self.view.generate_view(self.presenter.get_view_model())
