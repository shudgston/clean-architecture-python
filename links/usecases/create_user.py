import abc

from links.context import context
from links.entities import User
from links.logger import get_logger
from links.security import create_password_hash
from links.usecases.interfaces import OutputBoundary, Controller
from links import validation

LOGGER = get_logger(__name__)


class CreateUserInputBoundary(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_user(self, username, password, presenter):
        pass


class CreateUserUseCase(CreateUserInputBoundary):

    _validation_schema = {
        'username': validation.Schema(
            required=True,
            maxlength=20,
            custom=[(validation.is_valid_username, "Username is not allowed")],
        )
    }

    def create_user(self, username, password, presenter):
        """

        :param username:
        :param password:
        :return:
        """
        response = {'user_created': False, 'username': username, 'errors': {}}

        is_valid, errors = validation.validate(
            {'username': username},
            self._validation_schema
        )

        if errors:
            response['errors'] = errors
        elif context.user_repo.exists(username):
            LOGGER.info("create_user: user '{}' already exists".format(username))
            response['errors'] = {'username': ['That username is taken']}
        else:
            user = User(username)
            user.password_hash = create_password_hash(password)
            context.user_repo.save(user)
            response['user_created'] = True

        presenter.present(response)


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
        self.usecase.create_user(request['username'], request['password'], self.presenter)
        return self.view.generate_view(self.presenter.get_view_model())
