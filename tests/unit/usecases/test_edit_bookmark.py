from unittest import TestCase

from links.exceptions import InvalidOperationError
from links.context import context
from links.entities import Bookmark, User
from links.usecases import edit_bookmark
from tests.unit.usecases.base import UseCaseTest, PresenterSpy, ControllerTestMixin


class EditBookmarkUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.presenter_spy = PresenterSpy()
        context.user_repo._data = []
        context.bookmark_repo._data = []

        self.user = User('user')
        context.user_repo.save(self.user)

        self.bookmark = Bookmark('id1', self.user.id, 'name', 'http://test.com')
        context.bookmark_repo.save(self.bookmark)

    def test_user_can_edit_bookmark(self):
        uc = edit_bookmark.EditBookmarkUseCase()
        uc.user_id = self.user.id
        uc.bookmark_id = self.bookmark.id
        uc.name = 'name changed failing test'
        uc.url = 'http://test.com'
        uc.execute(self.presenter_spy)

        self.assertEqual(uc.user_id, 'user')
        self.assertTrue(self.presenter_spy.present_called)
        self.assertEqual(self.presenter_spy.response_model.errors, {})

    def test_user_cannot_edit_another_users_bookmark(self):
        other_user = User('other_user')
        context.user_repo.save(other_user)

        uc = edit_bookmark.EditBookmarkUseCase()
        uc.user_id = other_user.id
        uc.bookmark_id = self.bookmark.id
        uc.name = 'name changed'
        uc.url = 'http://test.com'
        uc.execute(self.presenter_spy)

        self.assertTrue(self.presenter_spy.present_called)
        self.assertEqual(
            self.presenter_spy.response_model.errors['error'],
            'Forbidden'
        )

    def test_unknown_user_cannot_edit_bookmark(self):
        uc = edit_bookmark.EditBookmarkUseCase()
        uc.user_id = 'unknown_user'
        uc.bookmark_id = self.bookmark.id
        uc.name = 'test'
        uc.url = 'http://test.com'

        with self.assertRaises(InvalidOperationError):
           uc.execute(self.presenter_spy)

    def test_invalid_values_are_caught(self):
        uc = edit_bookmark.EditBookmarkUseCase()
        uc.user_id = self.user.id
        uc.bookmark_id = self.bookmark.id
        uc.name = 'test'
        uc.url = 'gobbledigook'
        uc.execute(self.presenter_spy)

        self.assertEqual(
            self.presenter_spy.response_model.errors['url'],
            'Invalid URL'
        )

    def test_validation_error_when_args_not_complete(self):
        uc = edit_bookmark.EditBookmarkUseCase()
        uc.bookmark_id = self.bookmark.id
        uc.user_id = self.user.id
        uc.execute(self.presenter_spy)

        self.assertTrue(self.presenter_spy.present_called)
        self.assertEqual(
            self.presenter_spy.response_model.errors['name'],
            'Name is too long'
        )
        self.assertEqual(
            self.presenter_spy.response_model.errors['url'],
            'Invalid URL'
        )

    def test_error_raised_when_bookmark_id_is_none(self):
        uc = edit_bookmark.EditBookmarkUseCase()
        uc.user_id = self.user.id
        uc.bookmark_id = None
        uc.name = 'name'
        uc.url = 'http://test.com'

        with self.assertRaises(InvalidOperationError):
            uc.execute(self.presenter_spy)

    def test_error_raised_when_user_id_is_none(self):
        uc = edit_bookmark.EditBookmarkUseCase()
        uc.user_id = None
        uc.bookmark_id = self.bookmark.id
        uc.name = 'name'
        uc.url = 'http://test.com'

        with self.assertRaises(InvalidOperationError):
            uc.execute(self.presenter_spy)


class EditBookmarkPresentationTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = edit_bookmark.Response()
        presenter = edit_bookmark.EditBookmarkPresenter()
        presenter.present(response)
        self.assertDictEqual(
            presenter.get_view_model(),
            {
                'success': True,
                'errors': {}
            }
        )


class EditBookmarkControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        self.mixin_setup()
        self.controller = edit_bookmark.EditBookmarkController(
            self.usecase,
            self.presenter,
            self.view
        )
        self.request = {
            'bookmark_id': 'bid',
            'user_id': 'uid',
            'name': 'name',
            'url': 'url'
        }

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.execute.assert_called_with(self.presenter)
