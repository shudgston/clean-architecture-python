"""
In-memory implementations of repository interfaces.
These should only be used for testing or demonstration purposes.
"""

from links.repos.interfaces import BookmarkRepo, UserRepo
from links.entities import Bookmark, User, NullUser, NullBookmark


class MemoryBookmarkRepo(BookmarkRepo):

    def __init__(self):
        self._data = []

    def save(self, bookmark):
        if bookmark.id is None:
            return
        data = {
            'id': bookmark.id,
            'user_id': bookmark.user_id,
            'name': bookmark.name,
            'url': bookmark.url,
            'date_created': bookmark.date_created,
        }
        self._data.append(data)

    def get(self, bookmark_id):
        docs = [x for x in self._data if x['id'] == bookmark_id]

        if docs:
            doc = docs[0]
            return Bookmark(
                doc['id'],
                doc['user_id'],
                doc['name'],
                doc['url'],
                date_created=doc['date_created']
            )
        return NullBookmark()

    def get_by_user(self, user_id, limit=None):
        docs = [doc for doc in self._data if doc['user_id'] == user_id]
        entities = [
            Bookmark(
                doc['id'],
                doc['user_id'],
                doc['name'],
                doc['url']
            ) for doc in docs
        ]

        return sorted(entities, key=lambda x: x.date_created)


class MemoryUserRepo(UserRepo):

    def __init__(self):
        self._data = []

    def save(self, user):
        self._data.append({
            'id': user.id,
            'password_hash': user.password_hash
        })

    def get(self, user_id):
        docs = [doc for doc in self._data if doc['id'] == user_id]
        if docs:
            user = User(docs[0]['id'])
            user.password_hash = docs[0]['password_hash']
            return user

        return NullUser()

    def exists(self, user_id):
        user = self.get(user_id)
        return user.id is not None

    def get_password_hash(self, user_id):
        user = self.get(user_id)
        return user.password_hash
