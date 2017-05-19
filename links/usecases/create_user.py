import abc
from links.context import context
from links.logger import get_logger
from links.security import check_password, create_password_hash
from links.entities import User
from links.usecases.interfaces import OutputBoundary, Controller

LOGGER = get_logger(__name__)


class CreateUserInputBoundary(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_user(self, username, password):
        pass


class CreateUserUseCase(CreateUserInputBoundary):

    def create_user(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        response = {'user_created': False, 'username': username}

        if context.user_repo.exists(username):
            return response
        else:
            user = User(username)
            user.password_hash = create_password_hash(password)
            context.user_repo.save(user)
            response['user_created'] = True
            return response


class CreateUserPresenter(OutputBoundary):

    def __init__(self):
        self.view_model = False

    def present(self, response_model):
        """This presenter doesn't need to do much"""
        self.view_model = response_model

    def get_view_model(self):
        return self.view_model


class CreateUserController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        resp = self.usecase.create_user(request['username'], request['password'])
        self.presenter.present(resp)
        vm = self.presenter.get_view_model()
        return self.view.generate_view(vm)
