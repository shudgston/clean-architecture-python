"""
Implementations of the repo interfaces using CouchDB as the storage mechanism
"""
import datetime
import json
import couchdb
import dateutil.parser

from links.entities import Bookmark, NullBookmark, User, NullUser
from links.logger import get_logger
from links.repos.interfaces import BookmarkRepo, UserRepo
from links.settings import CouchDBSettings

LOGGER = get_logger(__name__)


def json_decoder(json_str):
    """Decoder wrapper for couchdb.json.use"""
    return json.loads(json_str, cls=CouchDBDecoder)


def json_encoder(obj):
    """Encoding wrapper for couchdb.json.use"""
    return json.dumps(obj, cls=CouchDBEncoder)


class CouchDBDecoder(json.JSONDecoder):
    """Custom JSON decoder class for handlings couchdb data"""

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, **kwargs)

    def object_hook(self, json_dict):
        if 'date_created' in json_dict:
            json_dict['date_created'] = self.parsedate(
                json_dict['date_created'])

        return json_dict

    def parsedate(self, datestr):
        try:
            result = dateutil.parser.parse(datestr)
        except AttributeError:
            result = None
        return result


class CouchDBEncoder(json.JSONEncoder):
    """Custom JSON encoder class for handling special data types"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()


class CouchDBMixin:
    """A mixin class to share commonly used attributes amongst subclasses"""

    def __init__(self):
        LOGGER.debug(
            "%s -> %s/%s",
            self.__class__,
            CouchDBSettings.DATABASE_HOST,
            CouchDBSettings.DATABASE_NAME
        )
        couchdb.json.use(encode=json_encoder, decode=json_decoder)
        self.database = CouchDBSettings.DATABASE_NAME
        self.server = couchdb.Server(CouchDBSettings.DATABASE_HOST)
        self.server.resource.credentials = (
            CouchDBSettings.DATABASE_USER,
            CouchDBSettings.DATABASE_PASSWORD,
        )
        self.server.resource.session.disable_ssl_verification()
        self.db = self.server[self.database]


class CouchDBBookmarkRepo(CouchDBMixin, BookmarkRepo):

    _doc_type = 'bookmark'

    def to_entity(self, doc):
        return Bookmark(
            doc['_id'],
            doc['user_id'],
            doc['name'],
            doc['url'],
            date_created=doc['date_created']
        )

    def save(self, bookmark):
        """
        """
        try:
            doc = self.db[bookmark.id]
            doc['name'] = bookmark.name
            doc['url'] = bookmark.url
            LOGGER.debug("CouchDBBookmarkRepo: updating exising doc")
        except couchdb.http.ResourceNotFound:
            LOGGER.debug("CouchDBBookmarkRepo: creating new doc")
            # fill with entity data
            doc = {
                '_id': bookmark.id,
                'user_id': bookmark.user_id,
                'name': bookmark.name,
                'url': bookmark.url,
                'date_created': bookmark.date_created,
                'type': self._doc_type,
            }

        LOGGER.info("Saving to couchdb: %s", doc)
        self.db.save(doc)

    def delete(self, bookmark_id):
        """
        """
        LOGGER.debug('Delete doc %s', bookmark_id)
        doc = self.db[bookmark_id]
        self.db.delete(doc)

    def get(self, bookmark_id):
        try:
            doc = self.db[bookmark_id]
        except couchdb.ResourceNotFound:
            LOGGER.exception('Bookmark %s does not exist', bookmark_id)
            return NullBookmark()
        return self.to_entity(doc)

    def get_by_user(self, user_id, limit=None):
        """
        TODO: use a better view
        """
        url = '_design/bookmarks/_view/by_user'
        batch = 1000
        opts = dict(
            startkey=[user_id, {}],
            endkey=[user_id],
            descending=True,
            include_docs=True,
            limit=limit
        )
        gen = self.db.iterview(url, batch, **opts)
        return [
            self.to_entity(row.doc) for row in gen if row.doc.get('user_id') == user_id
        ]


class CouchDBUserRepo(CouchDBMixin, UserRepo):

    _doc_type = 'user'

    def to_entity(self, doc):
        user = User(doc['_id'])
        user.password_hash = doc['password_hash']
        return user

    def save(self, user):
        """
        """
        if self.exists(user.id):
            LOGGER.info("User %s already exists.")
            return

        doc = {
            '_id': user.id,
            'type': self._doc_type,
            'password_hash': user.password_hash,
        }
        self.db.save(doc)

    def get(self, user_id):
        """
        """
        LOGGER.debug("Find user by id: %s", user_id)
        try:
            doc = self.db[user_id]
        except couchdb.ResourceNotFound:
            LOGGER.exception("User id %s not found", user_id)
            return NullUser()

        return self.to_entity(doc)

    def get_password_hash(self, user_id):
        try:
            doc = self.db[user_id]
        except couchdb.ResourceNotFound:
            LOGGER.exception("User id %s not found", user_id)
            return ''
        return doc.get('password_hash', '')

    def exists(self, user_id):
        """
        """
        exists = True
        try:
            doc = self.db[user_id]
            # LOGGER.debug("User exists: %s", doc)
        except couchdb.http.ResourceNotFound:
            exists = False
        return exists
