from unittest import TestCase, mock

from links.context import context
from links.entities import User
from links.exceptions import UserNotFound
from links.usecases import create_bookmark
from .base import UseCaseTest, PresenterSpy, ControllerTestMixin


class CreateBookmarkSlugTest(TestCase):

    def test_slug_format(self):
        slug = create_bookmark.create_bookmark_slug('test title')
        parts = slug.split('-')
        self.assertEqual(8, len(parts[0]))
        self.assertEqual('test', parts[1])
        self.assertEqual('title', parts[2])


class CreateBookmarkUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = User('user')
        context.user_repo.save(self.user)
        self.uc = create_bookmark.CreateBookmarkUseCase()
        self.presenter_spy = PresenterSpy()

    def test_unknown_user_cannot_create_bookmark(self):
        with self.assertRaises(UserNotFound):
            self.uc.create_bookmark('unknown', 'test', 'http://test.com', self.presenter_spy)

    def test_user_can_create_bookmark(self):
        self.uc.create_bookmark(self.user.id, 'test name', 'http://test.com', self.presenter_spy)
        self.assertIn('bookmark_id', self.presenter_spy.response_model)
        self.assertIn('errors', self.presenter_spy.response_model)
        self.assertIn('test-name', self.presenter_spy.response_model['bookmark_id'])
        self.assertDictEqual({}, self.presenter_spy.response_model['errors'])

        saved = context.bookmark_repo.get(
            self.presenter_spy.response_model['bookmark_id']
        )
        self.assertIn('test-name', saved.id)
        self.assertEqual(self.user.id, saved.user_id)
        self.assertEqual('test name', saved.name)
        self.assertEqual('http://test.com', saved.url)

    def test_invalid_values_are_caught(self):
        self.uc.create_bookmark(self.user.id, 'test', 'gobbledigook', self.presenter_spy)
        self.assertDictEqual(
            {'url': ['Not a valid URL']},
            self.presenter_spy.response_model['errors']
        )


class CreateBookmarkPresentationTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = {'bookmark_id': 'id1', 'errors': {}}
        presenter = create_bookmark.CreateBookmarkPresenter()
        presenter.present(response)
        expected = {'bookmark_id': 'id1', 'errors': {}}
        self.assertDictEqual(expected, presenter.get_view_model())


class CreateBookmarkControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        self.mixin_setup()
        self.controller = create_bookmark.CreateBookmarkController(
            self.usecase,
            self.presenter,
            self.view
        )
        self.request = {'user_id': 'id', 'name': 'name', 'url': 'url'}

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.create_bookmark.assert_called_with(
            'id', 'name', 'url', self.presenter
        )
