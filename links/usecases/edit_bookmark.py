from links import validation
from links.context import context
from links.logger import get_logger
from links.usecases.interfaces import Controller, OutputBoundary, UseCase
from links.exceptions import InvalidOperationError

LOGGER = get_logger(__name__)

NAME_LENGTH_LIMIT = 400



class EditBookmarkUseCase(UseCase):

    def __init__(self):
        self.user_id = None
        self.bookmark_id = None
        self.name = None
        self.url = None
        self._validation_errors = {}

    def execute(self, presenter):
        bookmark = context.bookmark_repo.get(self.bookmark_id)
        self._validate_bookmark(bookmark)
        self._validate_user(context.user_repo.get(self.user_id))
        response = Response()

        if bookmark.belongs_to(self.user_id):
            errors = self._validate()
            if errors:
                response.errors = errors
            else:
                self._save_bookmark(bookmark)
        else:
            response.errors = {'error': 'Forbidden'}
            LOGGER.warning(
                "'%s' does not belong to user '%s' ",
                self.bookmark_id,
                self.user_id,
            )
        presenter.present(response)

    def _validate_bookmark(self, bookmark):
        if bookmark.id is None:
            raise InvalidOperationError("No such bookmark")

    def _validate_user(self, user):
        if user.id is None:
            raise InvalidOperationError("No such user")

    def _validate(self):
        errors = {}
        if self.name is None or len(self.name) > NAME_LENGTH_LIMIT:
            errors['name'] = 'Name is too long'

        if not validation.is_url(self.url):
            errors['url'] = 'Invalid URL'

        return errors

    def _save_bookmark(self, bookmark):
        bookmark.name = self.name
        bookmark.url = self.url
        context.bookmark_repo.save(bookmark)


class EditBookmarkPresenter(OutputBoundary):

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


class EditBookmarkController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        self.usecase.user_id = request['user_id']
        self.usecase.bookmark_id = request['bookmark_id']
        self.usecase.name = request['name']
        self.usecase.url = request['url']
        self.usecase.execute(self.presenter)
        return self.view.generate_view(self.presenter.get_view_model())
