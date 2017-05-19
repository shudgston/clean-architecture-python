
class UserError(Exception):
    """
    An exception that can be raised to deliver generic error messages to a user
    on a front end.
    """
    pass


class LinksError(Exception):
    pass


class RepositoryError(LinksError):
    pass


class UserNotFound(LinksError):
    pass


class BookmarkNotFound(LinksError):
    pass
