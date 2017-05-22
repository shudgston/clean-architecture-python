import abc

# TODO: make create and update distinct functions. Don't have save() do both.


class BookmarkRepo(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save(self, bookmark):
        pass

    @abc.abstractmethod
    def get(self, bookmark_id):
        pass

    @abc.abstractmethod
    def get_by_user(self, user_id, limit=100):
        pass


class UserRepo(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save(self, user):
        pass

    @abc.abstractmethod
    def get(self, user_id):
        pass

    @abc.abstractmethod
    def exists(self, user_id):
        pass

    @abc.abstractmethod
    def get_password_hash(self, user_id):
        pass
