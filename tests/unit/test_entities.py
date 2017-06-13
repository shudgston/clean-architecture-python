import datetime
import unittest

from links.entities import Bookmark, User, NullBookmark, NullUser


class UserEntityTest(unittest.TestCase):

    def test_constructor(self):
        user = User('user')
        self.assertEqual(user.id, 'user')

    def test_null_user_constructor(self):
        user = NullUser()
        self.assertIs(user.id, None)
        self.assertIs(user.password_hash, None)


class BookmarkEntityTest(unittest.TestCase):

    def test_constructor(self):
        bm = Bookmark('id123', 'user', 'this is a test', 'http://example.com')
        self.assertEqual(bm.id, 'id123')
        self.assertEqual(bm.user_id, 'user')
        self.assertEqual(bm.name, 'this is a test')
        self.assertEqual(bm.url, 'http://example.com')
        self.assertTrue(isinstance(bm.date_created, datetime.datetime))

    def test_belongs_to(self):
        bm = Bookmark('id123', 'user', 'name', 'http://example.com')
        self.assertTrue(bm.belongs_to('user'))
        self.assertFalse(bm.belongs_to('another user'))
        self.assertFalse(bm.belongs_to(1))
        self.assertFalse(bm.belongs_to(None))


class NullBookmarkTest(unittest.TestCase):

    def test_null_bookmark_constructor(self):
        bm = NullBookmark()
        self.assertIs(bm.id, None)
        self.assertIs(bm.user_id, None)
        self.assertIs(bm.name, '')
        self.assertIs(bm.url, '')
        self.assertIs(bm.date_created, None)

    def test_belongs_to(self):
        bm = NullBookmark()
        self.assertFalse(bm.belongs_to('user'))
        self.assertFalse(bm.belongs_to('another user'))
        self.assertFalse(bm.belongs_to(1))
        self.assertFalse(bm.belongs_to(None))
