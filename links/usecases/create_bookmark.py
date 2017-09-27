import datetime
import re
import unicodedata
import uuid

from links import validation
from links.context import context
from links.entities import Bookmark
from links.exceptions import UserNotFound, ValidationError, InvalidOperationError
from links.logger import get_logger
from links.usecases.interfaces import Controller, IPresenter, UseCase

LOGGER = get_logger(__name__)

NAME_LENGTH_LIMIT = 400


def create_bookmark_slug(text):
    """
    """
    assert isinstance(text, str)
    s = unicodedata.normalize('NFKC', text.strip())
    s = re.sub(r'[^\w\s-]', '', s)
    # limit final length
    s = re.sub(r'[-\s]+', '-', s).lower()[:200]
    return '{}-{}'.format(uuid.uuid4().hex[:8], s)


class CreateBookmarkUseCase(UseCase):
    """The 'create a new bookmark' use case"""

    def __init__(self):
        self.user_id = None
        self.name = None
        self.url = None

    def execute(self, presenter):

        if not context.user_repo.exists(self.user_id):
            LOGGER.error("Unknown user '%s'", self.user_id)
            raise InvalidOperationError("No such user")

        errors = self._validate()
        if errors:
            presenter.present(Response(errors=errors))
        else:
            bookmark_id = create_bookmark_slug(self.name)
            bookmark = Bookmark(
                bookmark_id,
                self.user_id,
                self.name,
                self.url,
                date_created=datetime.datetime.utcnow()
            )
            context.bookmark_repo.save(bookmark)
            presenter.present(Response())

    def _validate(self):
        errors = {}
        if self.name is None or len(self.name) > NAME_LENGTH_LIMIT:
            errors['name'] = 'Name is too long'

        if not validation.is_url(self.url):
            errors['url'] = 'Invalid URL'

        return errors


class CreateBookmarkPresenter(IPresenter):

    def __init__(self):
        self.view_model = {
            'success': False,
            'errors': {},
        }

    def present(self, response):
        self.view_model['errors'] = response.errors
        self.view_model['success'] = response.errors == {}

    def get_view_model(self):
        return self.view_model


class Response:

    def __init__(self, errors=None):
        if errors is None:
            errors = {}
        self.errors = errors



class CreateBookmarkController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        self.usecase.user_id = request['user_id']
        self.usecase.name = request['name']
        self.usecase.url = request['url']
        self.usecase.execute(self.presenter)
        return self.view.generate_view(self.presenter.get_view_model())
