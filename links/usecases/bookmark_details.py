from links import formatting
from links.context import context
from links.exceptions import BookmarkNotFound
from links.logger import get_logger
from links.usecases.interfaces import Controller, IPresenter, UseCase

LOGGER = get_logger(__name__)


def format_bookmark_details(bookmark):
    # return {
    #     'bookmark_id': bookmark.id
    #     'name': bookmark.name
    #     'url': bookmark['url'],
    #     'date_created': formatting.display_date(bookmark['date_created']),
    #     'date_created_iso': formatting.iso_date(bookmark['date_created']),
    #     'host': formatting.host_from_url(bookmark['url']),
    # }
    view = BookmarkDetailsViewModel()
    view.id = bookmark.id
    view.name = bookmark.name
    view.url = bookmark.url
    view.date_created = formatting.display_date(bookmark.date_created)
    view.date_created_iso = formatting.iso_date(bookmark.date_created)
    view.host = formatting.host_from_url(bookmark.url)
    return view


class BookmarkDetailsUseCase(UseCase):
    """Fetch a bookmarks details"""

    def __init__(self):
        self.bookmark_id = None
        self.user_id = None

    def execute(self, presenter):
        bookmark = context.bookmark_repo.get(self.bookmark_id)

        if bookmark.belongs_to(self.user_id):
            response_model = self._make_presentable(bookmark)
            presenter.present(response_model)
        else:
            raise BookmarkNotFound

    def _make_presentable(self, bookmark):
        """Transform entity into a response model for the presenter"""
        response = BookmarkDetailsReponseModel()
        response.bookmark_id = bookmark.id
        response.name = bookmark.name
        response.url = bookmark.url
        response.date_created = bookmark.date_created
        response.host = formatting.host_from_url(bookmark.url)
        return response


class BookmarkDetailsPresenter(IPresenter):

    def __init__(self):
        self.view_model = BookmarkDetailsViewModel()

    def present(self, response_model):
        # self.view_model = format_bookmark_details(bookmark_details)
        self._make_viewable(response_model)

    def get_view_model(self):
        return self.view_model

    def _make_viewable(self, response_model):
        self.view_model.bookmark_id = response_model.bookmark_id
        self.view_model.name = response_model.name
        self.view_model.url = response_model.url
        self.view_model.host = response_model.host
        self.view_model.date_created = formatting.display_date(
            response_model.date_created
        )
        self.view_model.date_created_iso = formatting.iso_date(
            response_model.date_created
        )


class BookmarkDetailsController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        self.usecase.user_id = request['user_id']
        self.bookmark_id = request['bookmark_id']
        self.usecase.execute(self.presenter)
        return self.view.generate_view(self.presenter.get_view_model())


class BookmarkDetailsReponseModel:

    def __init__(self):
        self.bookmark_id = None
        self.name = None
        self.url = None
        self.host = None
        self.host = None
        self.date_created = None


class BookmarkDetailsViewModel:

    def __init__(self):
        self.bookmark_id = None
        self.name = None
        self.url = None
        self.host = None
        self.date_created = None
        self.date_created_iso = None