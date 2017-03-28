import abc
from datetime import datetime
from urllib.parse import urlparse


class Entity(metaclass=abc.ABCMeta):

    _id = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value


class Bookmark:

    def __init__(self, id_, user_id, name, url, date_created=None):
        self.id = id_
        self.user_id = user_id
        self.name = name
        self.url = url

        if date_created is None:
            date_created = datetime.now()

        self.date_created = date_created

    def __repr__(self):
        output = self.__dict__.copy()
        output['date_created'] = repr(self.date_created)
        return (
            "Bookmark('{id}', '{user_id}', '{name}', '{url}', date_created={date_created})"
            .format(**output)
        )


class NullBookmark(Bookmark):
    """Return a null entity when nothing was found"""

    def __init__(self):
        # overloaded init
        super().__init__(None, None, None, None)
        self.date_created = None

    def __repr__(self):
        return "NullBookmark()"


class User:

    def __init__(self, id_):
        self.id = id_
        self.password_hash = None

    def __repr__(self):
        return "User('{}')".format(self.id)


class NullUser(User):
    """Representation of a 'user not found'"""

    def __init__(self):
        # overloaded init
        super().__init__(None)

    def __repr__(self):
        return 'NullUser()'
