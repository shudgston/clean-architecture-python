import unittest

from links import validation


class IsURLTest(unittest.TestCase):

    def test_value_is_valid_url(self):
        self.assertTrue(validation.is_url('http://localhost'))
        self.assertTrue(validation.is_url('http://example.com'))
        self.assertTrue(validation.is_url('http://www.test.com'))

    def test_value_is_invalid_url(self):
        self.assertFalse(validation.is_url('localhost'))
        self.assertFalse(validation.is_url('foo'))
        self.assertFalse(validation.is_url('example.com'))


class IsValidUserNameTest(unittest.TestCase):

    def test_username_is_valid(self):
        self.assertTrue(validation.is_valid_username('s1'))
        self.assertTrue(validation.is_valid_username('h0d0r'))
        self.assertTrue(validation.is_valid_username('hodor_123'))
        self.assertTrue(validation.is_valid_username('hodor123_hodor_123'))

    def test_username_is_invalid(self):
        self.assertFalse(validation.is_valid_username('_hodor'))
        self.assertFalse(validation.is_valid_username('1hodor'))
        self.assertFalse(validation.is_valid_username('___'))
        self.assertFalse(validation.is_valid_username('hodor!'))
        self.assertFalse(validation.is_valid_username('h0d@r'))


class ValidationSchemaTest(unittest.TestCase):

    def test_required_value_present(self):
        request = {'foo': 'foo is here'}
        schema = {'foo': validation.Schema(required=True)}
        valid, errors = validation.validate(request, schema)
        self.assertTrue(valid)
        self.assertFalse(errors)

    def test_required_value_present_and_empty(self):
        request = {'foo': ''}
        schema = {'foo': validation.Schema(required=True)}
        is_valid, errors = validation.validate(request, schema)
        self.assertFalse(is_valid)
        self.assertEqual(errors['foo'], ['Value is required'])

    def test_required_value_present_and_none(self):
        request = {'foo': None}
        schema = {'foo': validation.Schema(required=True)}
        is_valid, errors = validation.validate(request, schema)
        self.assertFalse(is_valid)
        self.assertEqual(errors['foo'], ['Value is required'])

    def test_required_value_missing(self):
        request = {}
        schema = {'foo': validation.Schema(required=True)}
        is_valid, errors = validation.validate(request, schema)
        self.assertFalse(is_valid)
        self.assertEqual(errors['foo'], ['Value is required'])

    def test_value_exceeds_maxlength(self):
        request = {'foo': 'test'}
        schema = {'foo': validation.Schema(maxlength=2)}
        valid, errors = validation.validate(request, schema)
        self.assertFalse(valid)
        self.assertEqual(errors['foo'], ['Value exceeds maximum length 2'])

    def test_value_meets_maxlength(self):
        request = {'foo': 'test'}
        schema = {'foo': validation.Schema(maxlength=4)}
        valid, errors = validation.validate(request, schema)
        self.assertTrue(valid)
        self.assertFalse(errors)

    def test_custom_validator_func_fails(self):

        def nope(x):
            return False

        request = {'foo': 'test'}
        schema = {
            'foo': validation.Schema(
                custom=[(nope, "this function always fails")])
        }
        valid, errors = validation.validate(request, schema)
        self.assertFalse(valid)
        self.assertEqual(errors['foo'], ['this function always fails'])

    def test_given_schema_should_pass(self):
        request = {
            'name': 'url name',
            'url': 'http://www.example.com'
        }

        defaults = {
            'required': True,
            'maxlength': 100
        }

        schema = {
            'name': validation.Schema(**defaults),
            'url': validation.Schema(
                custom=[(validation.is_url, "must be a valid url")],
                **defaults)
        }

        valid, errors = validation.validate(request, schema)
        self.assertTrue(valid)
        self.assertFalse(errors)

    def test_given_schema_should_fail(self):
        request = {
            'name': 'url name',
            'url': 'gobbledigook'
        }
        defaults = {
            'required': True,
            'maxlength': 100
        }
        schema = {
            'name': validation.Schema(**defaults),
            'url': validation.Schema(
                custom=[(validation.is_url, "must be a valid URL")]),
        }

        valid, errors = validation.validate(request, schema)
        self.assertFalse(valid)
        self.assertEqual(errors['url'], ['must be a valid URL'])
