from unittest import TestCase
from links.security import create_password_hash, check_password, set_testing_ctx

# lowers the number of passes so tests are not so slow.
set_testing_ctx()


class CreatePasswordHasHTest(TestCase):

    def test_hash_is_created(self):
        hash = create_password_hash('password')
        self.assertTrue(isinstance(hash, str))
        self.assertTrue(hash.startswith('$pbkdf2-sha256$'))


class CheckPasswordTest(TestCase):

    def test_password_matches_hash(self):
        hash = create_password_hash('password')
        self.assertTrue(check_password('password', hash))

    def test_password_does_not_match_hash(self):
        hash = create_password_hash('password')
        self.assertFalse(check_password('wrong', hash))
