from links.context import context
from links.logger import get_logger
from links.security import check_password

LOGGER = get_logger(__name__)


class AuthenticateUserUseCase:

    def authenticate_user(self, user_id, password, presenter):
        """
        :param user_id:
        :param password:
        :param presenter:
        :return:
        """
        password_hash = context.user_repo.get_password_hash(user_id)
        verified = check_password(password, password_hash)
        LOGGER.info("Auth succeeded? %s", verified)
        presenter.present(verified)
