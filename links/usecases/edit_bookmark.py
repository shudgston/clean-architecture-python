import abc

from links import validation
from links.context import context
from links.logger import get_logger
from links.usecases.interfaces import Controller, OutputBoundary

LOGGER = get_logger(__name__)


class EditBookmarkInputBoundary(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def edit_bookmark(self, user_id, name, url, presenter):
        pass


class EditBookmarkUseCase(EditBookmarkInputBoundary):
    """Creates a new bookmark"""

    _validation_schema = {
        # 'user_id': validation.Schema(required=True),
        'name': validation.Schema(required=True, maxlength=400),
        'url': validation.Schema(
            required=True,
            custom=[(validation.is_url, "Not a valid URL")])
    }

    def edit_bookmark(self, user_id, bookmark_id, name, url, presenter):
        unclean_data = {'name': name, 'url': url}
        is_valid, errors = validation.validate(unclean_data, self._validation_schema)
        bookmark = context.bookmark_repo.get(bookmark_id)

        response = {'bookmark_id': bookmark_id, 'errors': None}

        if errors:
            response['errors'] = errors
        elif bookmark.belongs_to(user_id):
            bookmark.name = name
            bookmark.url = url
            context.bookmark_repo.save(bookmark)
        else:
            response['errors'] = {'message': 'Insufficient Permissions'}

        presenter.present(response)


class EditBookmarkPresenter(OutputBoundary):

    def __init__(self):
        self.view_model = {}

    def present(self, response_model):
        self.view_model['bookmark_id'] = response_model['bookmark_id']
        self.view_model['errors'] = {
            key: val for key, val in response_model['errors'].items()
        }

    def get_view_model(self):
        return self.view_model


class EditBookmarkController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        self.usecase.edit_bookmark(
            request['user_id'],
            request['name'],
            request['url'],
            self.presenter
        )
        return self.view.generate_view(self.presenter.get_view_model())
