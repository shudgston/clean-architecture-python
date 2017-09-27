from collections import namedtuple
from abc import abstractmethod

from links import exceptions
from links import formatting
from links.context import context
from links.exceptions import BookmarkNotFound
from links.logger import get_logger
from links.usecases.interfaces import Controller, IPresenter, UseCase
from links.usecases.interfaces import OutputBoundary

LOGGER = get_logger(__name__)

Bookmark = namedtuple('Bookmark', ['id', 'name', 'url', 'date_created'])
ViewableBookmark = namedtuple('Bookmark', ['id', 'name', 'url', 'date_created'])


class ViewBookmarksUseCase(UseCase):

    def execute(self, presenter):
        # Template method pattern of execution
        data = self._fetch_data()
        response_model = self._create_response_model(data)
        presenter.present(response_model)

    @abstractmethod
    def _fetch_data(self):
        """Steps to fetch data from a repo. Return data is passed to self._present"""
        pass

    @abstractmethod
    def _create_response_model(self, data):
        """Create a response model to pass to the presenter"""
        pass


class ListBookmarksUseCase(ViewBookmarksUseCase):
    """Constructs a list of all bookmarks owned by a user."""

    def __init__(self, user_id=None):
        self.user_id = user_id

    def _fetch_data(self):
        if not context.user_repo.exists(self.user_id):
            raise exceptions.UserNotFound(self.user_id)
        try:
            bookmarks = context.bookmark_repo.get_by_user(self.user_id, limit=1000)
        except Exception as ex:
            LOGGER.exception(ex)
            raise exceptions.RepositoryError("Data access error")

        return bookmarks

    def _create_response_model(self, data):
        return [self._make_presentable(bm) for bm in data]

    def _make_presentable(self, bm):
        return Bookmark(
            id=bm.id,
            name=bm.name,
            url=bm.url,
            date_created=bm.date_created
        )


class BookmarkDetailsUseCase(ViewBookmarksUseCase):
    """Fetch a bookmarks details"""

    def __init__(self, user_id=None, bookmark_id=None):
        self.user_id = user_id
        self.bookmark_id = bookmark_id

    def _fetch_data(self):
        bookmark = context.bookmark_repo.get(self.bookmark_id)
        if bookmark.belongs_to(self.user_id):
            return bookmark

        raise BookmarkNotFound

    def _create_response_model(self, data):
        return self._make_presentable(data)

    def _make_presentable(self, bookmark):
        """Transform entity into a response model for the presenter"""
        return Bookmark(
            id= bookmark.id,
            name=bookmark.name,
            url=bookmark.url,
            date_created=bookmark.date_created
        )


class ListBookmarksPresenter(OutputBoundary):

    def __init__(self):
        self._view_model = []

    def get_view_model(self):
        return self._view_model

    def present(self, response_model):
        self._view_model = [self._make_viewable(bm) for bm in response_model]

    def _make_viewable(self, bookmark):
        return ViewableBookmark(
            id=bookmark.id,
            name=bookmark.name,
            url=bookmark.url,
            date_created=formatting.iso_date(bookmark.date_created)
        )


class BookmarkDetailsPresenter(IPresenter):

    def __init__(self):
        self._view_model = None

    def present(self, response_model):
        self._make_viewable(response_model)

    def get_view_model(self):
        return self._view_model

    def _make_viewable(self, response_model):
        self._view_model = ViewableBookmark(
            id=response_model.id,
            name=response_model.name,
            url=response_model.url,
            date_created = formatting.iso_date(response_model.date_created)
        )


class ListBookmarksController(Controller):
    """A default controller"""

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        self.usecase.user_id = request['user_id']
        self.usecase.execute(self.presenter)
        return self.view.generate_view(self.presenter.get_view_model())


class BookmarkDetailsController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        self.usecase.user_id = request['user_id']
        self.usecase.bookmark_id = request['bookmark_id']
        self.usecase.execute(self.presenter)
        return self.view.generate_view(self.presenter.get_view_model())