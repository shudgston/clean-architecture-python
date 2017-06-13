import abc
from datetime import datetime


class Entity(metaclass=abc.ABCMeta):

    _id = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value


class BookmarkEntity(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def belongs_to(self):
        pass

    @abc.abstractmethod
    def as_dict(self):
        pass


class Bookmark(BookmarkEntity):

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

    def belongs_to(self, user_id):
        return self.user_id == user_id

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'url': self.url,
            'date_created': self.date_created,
        }


class NullBookmark(BookmarkEntity):
    """Return a null entity when nothing was found"""

    def __init__(self):
        self.id = None
        self.user_id = None
        self.date_created = None
        self.name = ''
        self.url = ''

    def __repr__(self):
        return "NullBookmark()"

    def belongs_to(self, user_id):
        return False

    def as_dict(self):
        return {}


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
