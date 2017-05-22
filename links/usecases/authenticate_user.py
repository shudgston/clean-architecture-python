from abc import ABCMeta, abstractmethod

from links.context import context
from links.logger import get_logger
from links.security import check_password
from links.usecases.interfaces import OutputBoundary, Controller

LOGGER = get_logger(__name__)


class AuthenticateUseInputBoundary(metaclass=ABCMeta):

    @abstractmethod
    def authenticate_user(self, user_id, password):
        pass


class AuthenticateUserUseCase(AuthenticateUseInputBoundary):

    def authenticate_user(self, user_id, password):
        """
        :param user_id:
        :param password:
        :return:
        """
        response = {'is_authenticated': False, 'user_id': user_id}
        password_hash = context.user_repo.get_password_hash(user_id)

        if context.user_repo.exists(user_id):
            if check_password(password, password_hash):
                response['is_authenticated'] = True
                return response

        response['is_authenticated'] = False
        return response


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
        resp = self.usecase.authenticate_user(request['username'], request['password'])
        self.presenter.present(resp)
        vm = self.presenter.get_view_model()
        return self.view.generate_view(vm)
