from abc import ABCMeta, abstractmethod

from links import formatting
from links.context import context
from links.exceptions import BookmarkNotFound
from links.logger import get_logger
from links.usecases.interfaces import Controller, OutputBoundary

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
    }


class BookmarkDetailsInputBoundary(metaclass=ABCMeta):

    @abstractmethod
    def get_bookmark_details(self, user_id, bookmark_id, presenter):
        pass


class BookmarkDetailsUseCase(BookmarkDetailsInputBoundary):
    """Fetch a bookmarks details"""

    def get_bookmark_details(self, user_id, bookmark_id, presenter):
        """

        :param user_id:
        :param bookmark_id:
        :return:
        """
        bookmark = context.bookmark_repo.get(bookmark_id)

        if bookmark.belongs_to(user_id):
            # return bookmark.as_dict()
            presenter.present(bookmark.as_dict())
        else:
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
        self.usecase.get_bookmark_details(
            request['user_id'],
            request['bookmark_id'],
            self.presenter
        )
        return self.view.generate_view(self.presenter.get_view_model())
