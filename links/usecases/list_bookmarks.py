from abc import ABCMeta, abstractmethod
from links.context import context
from links.logger import get_logger
from links.usecases.interfaces import OutputBoundary, Controller
from links.usecases.bookmark_details import BookmarkDetails, format_bookmark_details
from links.settings import Settings
from links import exceptions

LOGGER = get_logger(__name__)


class ListBookmarksInputBoundary(metaclass=ABCMeta):

    @abstractmethod
    def list_bookmarks(self, user_id):
        pass


class ListBookmarksUseCase(ListBookmarksInputBoundary):
    """Constructs a list of all bookmarks owned by a user."""

    def list_bookmarks(self, user_id, filterkey=None):
        """

        :param user_id:
        :return:
        """
        limit = Settings.BOOKMARK_LIST_FILTERS.get(
            filterkey,
            Settings.BOOKMARK_LIST_FILTERS['recent'])

        if not context.user_repo.exists(user_id):
            raise exceptions.UserNotFound(user_id)

        try:
            bookmarks = context.bookmark_repo.get_by_user(user_id, limit=limit)
        except Exception as ex:
            LOGGER.exception(ex)
            raise exceptions.RepositoryError("Data access error")

        response = [
            BookmarkDetails(bm.id, bm.name, bm.url, bm.date_created)
            for bm in bookmarks
            if bm.user_id == user_id
        ]
        return response


class ListBookmarksPresenter(OutputBoundary):

    def __init__(self):
        self.view_model = {}

    def get_view_model(self):
        return self.view_model

    def present(self, bookmarks):
        self.view_model = [format_bookmark_details(bm) for bm in bookmarks]


class ListBookmarksController(Controller):
    """A default controller"""

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        resp = self.usecase.list_bookmarks(
            request['user_id'],
            filterkey=request.get('filterkey')
        )
        self.presenter.present(resp)
        vm = self.presenter.get_view_model()
        return self.view.generate_view(vm)
