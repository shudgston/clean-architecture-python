from links.context import context
from links.logger import get_logger
from links.security import check_password
from links.usecases.interfaces import OutputBoundary, Controller, UseCase

LOGGER = get_logger(__name__)


class AuthenticateUserUseCase(UseCase):

    def __init__(self):
        self.user_id = ''
        self.password = ''

    def execute(self, presenter: OutputBoundary):
        response = Response()
        response.user_id = self.user_id
        response.is_authenticated = False

        # user = context.user_repo.exists(self.username)
        password_hash = context.user_repo.get_password_hash(self.user_id)

        if check_password(self.password, password_hash):
            response.is_authenticated = True


        presenter.present(response)


class Response:

    def __init__(self):
        self.is_authenticated = False
        self.user_id = ''


class AuthenticateUserPresenter(OutputBoundary):

    def __init__(self):
        self._view_model = {
            'is_authenticated':  False,
            'user_id': '',
        }

    def present(self, response_model: Response):
        self._view_model['is_authenticated'] = response_model.is_authenticated
        self._view_model['user_id'] = response_model.user_id

    def get_view_model(self):
        return self._view_model


class AuthenticateUserController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        self.usecase.user_id = request['user_id']
        self.usecase.password = request['password']
        self.usecase.execute(self.presenter)
        return self.view.generate_view(self.presenter.get_view_model())
