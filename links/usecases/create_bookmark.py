import abc
import datetime
import uuid
from collections import namedtuple

from links import validation
from links.context import context
from links.entities import Bookmark
from links.exceptions import UserNotFound
from links.logger import get_logger
from links.usecases.interfaces import Controller, OutputBoundary

LOGGER = get_logger(__name__)

CreateBookmarkResponse = namedtuple(
    'CreateBookmarkResponse',
    ['bookmark_id',  'errors']
)


class CreateBookmarkInputBoundary(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_bookmark(self, user_id, name, url, date_created=None):
        pass


class CreateBookmarkUseCase(CreateBookmarkInputBoundary):
    """Creates a new bookmark"""

    _validation_schema = {
        'user_id': validation.Schema(required=True),
        'name': validation.Schema(required=True, maxlength=400),
        'url': validation.Schema(
            required=True,
            custom=[(validation.is_url, "Not a valid URL")])
    }

    def create_bookmark(self, user_id, name, url, date_created=None):
        """

        :param user_id:
        :param name:
        :param url:
        :return:
        """
        if not context.user_repo.exists(user_id):
            raise UserNotFound(user_id)

        unclean_data = {'user_id': user_id, 'name': name, 'url': url}
        is_valid, errors = validation.validate(unclean_data, self._validation_schema)

        if date_created is None:
            date_created = datetime.datetime.utcnow()

        if errors:
            response = CreateBookmarkResponse(bookmark_id=None, errors=errors)
            return response

        if context.user_repo.exists(user_id):
            bookmark_id = uuid.uuid4().hex
            bookmark = Bookmark(bookmark_id, user_id, name, url, date_created=date_created)
            LOGGER.info("create_bookmark: %s", bookmark)
            context.bookmark_repo.save(bookmark)
            response = CreateBookmarkResponse(bookmark_id=bookmark_id, errors=errors)
            return response


class CreateBookmarkPresenter(OutputBoundary):

    def __init__(self):
        self.view_model = {}

    def present(self, response_model):
        self.view_model['bookmark_id'] = response_model.bookmark_id
        self.view_model['errors'] = {
            key: val for key, val in response_model.errors.items()
        }

    def get_view_model(self):
        return self.view_model


class CreateBookmarkController(Controller):
    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        resp = self.usecase.create_bookmark(request['user_id'], request['name'], request['url'])
        self.presenter.present(resp)
        vm = self.presenter.get_view_model()
        return self.view.generate_view(vm)