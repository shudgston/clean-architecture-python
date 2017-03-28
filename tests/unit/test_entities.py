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
        bm = Bookmark('id123', 'user', 'name', 'web://example.com')
        self.assertEqual(bm.id, 'id123')
        self.assertEqual(bm.user_id, 'user')
        self.assertEqual(bm.name, 'name')
        self.assertEqual(bm.url, 'web://example.com')
        self.assertTrue(isinstance(bm.date_created, datetime.datetime))

    def test_null_bookmark_constructor(self):
        bm = NullBookmark()
        self.assertIs(bm.id, None)
        self.assertIs(bm.user_id, None)
        self.assertIs(bm.name, None)
        self.assertIs(bm.url, None)
        self.assertIs(bm.date_created, None)
