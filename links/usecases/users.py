import abc
from links.context import context
from links.logger import get_logger
from links.security import check_password

LOGGER = get_logger(__name__)


class InputBoundary(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def authenticate_user(self, user_id, password, presenter):
        pass


class AuthenticateUserUseCase(InputBoundary):

    def __init__(self):
        self._auth_success_callback = None

    def authenticate_user(self, user_id, password, presenter):
        password_hash = context.user_repo.get_password_hash(user_id)
        verified = check_password(password, password_hash)
        LOGGER.info("Auth succeeded? %s", verified)
        presenter.present(verified)
