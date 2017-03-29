import datetime
import uuid
from collections import namedtuple

from links import validation
from links.context import context
from links.entities import Bookmark
from links.exceptions import UserError
from links.logger import get_logger

LOGGER = get_logger(__name__)

BookmarkDetails = namedtuple(
    'BookmarkDetails',
    ['bookmark_id', 'name', 'url', 'date_created']
)

CreateBookmarkResponse = namedtuple(
    'CreateBookmarkResponse',
    ['bookmark_id',  'errors']
)


class BookmarkDetailsUseCase:
    """Fetch a bookmarks details"""

    def bookmark_details(self, user_id, bookmark_id, presenter):
        """

        :param user_id:
        :param bookmark_id:
        :param presenter:
        :return:
        """
        bookmark = context.bookmark_repo.get(bookmark_id)

        if bookmark.user_id == user_id:
            response = BookmarkDetails(
                bookmark.id,
                bookmark.name,
                bookmark.url,
                bookmark.date_created)
            presenter.present(response)
        else:
            LOGGER.info(
                "bookmark user '%s' did not match requesting user '%s'",
                bookmark.user_id,
                user_id
            )
            raise Exception("No Data")


class CreateBookmarkUseCase:
    """Creates a new bookmark"""

    _validation_schema = {
        'user_id': validation.Schema(required=True),
        'name': validation.Schema(required=True, maxlength=400),
        'url': validation.Schema(
            required=True,
            custom=[(validation.is_url, "Not a valid URL")])
    }

    def create_bookmark(self, user_id, name, url, presenter):
        """

        :param user_id:
        :param name:
        :param url:
        :param presenter:
        :return:
        """
        bookmark_id = uuid.uuid4().hex
        unclean_data = {'user_id': user_id, 'name': name, 'url': url}

        is_valid, errors = validation.validate(unclean_data, self._validation_schema)

        if errors:
            response = CreateBookmarkResponse(bookmark_id=None, errors=errors)
            presenter.present(response)
            return

        if context.user_repo.exists(user_id):
            bookmark = Bookmark(
                bookmark_id,
                user_id,
                name,
                url,
                date_created=datetime.datetime.now())

            context.bookmark_repo.save(bookmark)
            response = CreateBookmarkResponse(bookmark_id=bookmark_id, errors=errors)
            presenter.present(response)
        else:
            msg = "No such user '{}'".format(user_id)
            LOGGER.error(msg)
            raise UserError(msg)


class ListBookmarksUseCase:
    """Constructs a list of all bookmarks owned by a user."""

    def list_bookmarks(self, user_id, presenter):
        """

        :param user_id:
        :param presenter:
        :return:
        """
        try:
            bookmarks = context.bookmark_repo.get_by_user(user_id)
            response = [
                BookmarkDetails(bm.id, bm.name, bm.url, bm.date_created)
                for bm in bookmarks
                if bm.user_id == user_id
            ]
        except Exception as ex:
            LOGGER.exception(ex)
            raise UserError("Not found")

        presenter.present(response)
