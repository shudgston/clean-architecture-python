from abc import ABCMeta, abstractmethod
from links.usecases.interfaces import Controller, OutputBoundary
from links.context import context
from links.logger import get_logger
from links import formatting
from links.exceptions import BookmarkNotFound

LOGGER = get_logger(__name__)


def format_bookmark_details(bookmark):
    """

    :param bookmark: bookmark details dict
    :return: dict
    """
    return {
        'bookmark_id': bookmark['id'],
        'name': bookmark['name'],
        'url': bookmark['url'],
        'date_created': formatting.display_date(bookmark['date_created']),
        'date_created_iso': formatting.iso_date(bookmark['date_created']),
        'host': formatting.host_from_url(bookmark['url']),
        'slug': formatting.slugify(bookmark['name']),
    }


class InputBoundary(metaclass=ABCMeta):

    @abstractmethod
    def get_bookmark_details(self, user_id, bookmark_id):
        pass


class BookmarkDetailsUseCase(InputBoundary):
    """Fetch a bookmarks details"""

    def get_bookmark_details(self, user_id, bookmark_id):
        """

        :param user_id:
        :param bookmark_id:
        :return:
        """
        bookmark = context.bookmark_repo.get(bookmark_id)

        if bookmark.belongs_to(user_id):
            return bookmark.as_dict()

        raise BookmarkNotFound


class BookmarkDetailsPresenter(OutputBoundary):

    def __init__(self):
        self.view_model = {}

    def present(self, bookmark_details):
        self.view_model = format_bookmark_details(bookmark_details)

    def get_view_model(self):
        return self.view_model


class BookmarkDetailsController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        resp = self.usecase.get_bookmark_details(request['user_id'], request['bookmark_id'])
        self.presenter.present(resp)
        vm = self.presenter.get_view_model()
        return self.view.generate_view(vm)
