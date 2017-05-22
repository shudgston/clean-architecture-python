from abc import ABCMeta, abstractmethod
from collections import namedtuple
from links.usecases.interfaces import Controller, OutputBoundary
from links.context import context
from links.logger import get_logger
from links import formatting
from links.exceptions import BookmarkNotFound

LOGGER = get_logger(__name__)


BookmarkDetails = namedtuple(
    'BookmarkDetails',
    ['bookmark_id', 'name', 'url', 'date_created']
)


def format_bookmark_details(bookmark):
    """

    :param bookmark: bookmark details namedtuple
    :return: dict
    """
    return {
        'bookmark_id': bookmark.bookmark_id,
        'name': bookmark.name,
        'url': bookmark.url,
        'date_created': formatting.display_date(bookmark.date_created),
        'date_created_iso': formatting.iso_date(bookmark.date_created),
        'host': formatting.host_from_url(bookmark.url)
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

        # if bookmark.user_id == user_id:
        if bookmark.belongs_to(user_id):
            response = BookmarkDetails(
                bookmark.id,
                bookmark.name,
                bookmark.url,
                bookmark.date_created
            )
            return response

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
