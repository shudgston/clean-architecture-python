import abc
import datetime
import re
import unicodedata
import uuid

from links import validation
from links.context import context
from links.entities import Bookmark
from links.exceptions import UserNotFound
from links.logger import get_logger
from links.usecases.interfaces import Controller, OutputBoundary

LOGGER = get_logger(__name__)


def create_bookmark_slug(text):
    """
    """
    assert isinstance(text, str)
    s = unicodedata.normalize('NFKC', text.strip())
    s = re.sub(r'[^\w\s-]', '', s)
    # limit final length
    s = re.sub(r'[-\s]+', '-', s).lower()[:200]
    return '{}-{}'.format(uuid.uuid4().hex[:8], s)


class CreateBookmarkInputBoundary(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_bookmark(self, user_id, name, url, presenter):
        pass


class CreateBookmarkUseCase(CreateBookmarkInputBoundary):
    """The 'create a new bookmark' use case"""

    _validation_schema = {
        'user_id': validation.Schema(required=True),
        'name': validation.Schema(required=True, maxlength=400),
        'url': validation.Schema(
            required=True,
            custom=[(validation.is_url, "Not a valid URL")])
    }

    def create_bookmark(self, user_id, name, url, presenter):
        """
        :param user_id:
        :param name:
        :param url:
        :param presenter:
        :return:
        """
        if not context.user_repo.exists(user_id):
            raise UserNotFound(user_id)

        response = {'bookmark_id': None, 'errors': {}}
        unclean_data = {'user_id': user_id, 'name': name, 'url': url}
        is_valid, errors = validation.validate(unclean_data, self._validation_schema)

        if errors:
            response['errors'] = errors
        elif context.user_repo.exists(user_id):
            bookmark_id = create_bookmark_slug(name)
            date_created = datetime.datetime.utcnow()
            bookmark = Bookmark(bookmark_id, user_id, name, url, date_created=date_created)
            context.bookmark_repo.save(bookmark)
            response['bookmark_id'] = bookmark_id

        presenter.present(response)


class CreateBookmarkPresenter(OutputBoundary):

    def __init__(self):
        self.view_model = {}

    def present(self, response_model):
        self.view_model['bookmark_id'] = response_model['bookmark_id']
        self.view_model['errors'] = {
            key: val for key, val in response_model['errors'].items()
        }

    def get_view_model(self):
        return self.view_model


class CreateBookmarkController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        self.usecase.create_bookmark(
            request['user_id'],
            request['name'],
            request['url'],
            self.presenter
        )
        return self.view.generate_view(self.presenter.get_view_model())
