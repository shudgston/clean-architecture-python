from unittest import TestCase, mock

from links.context import context
from links.entities import Bookmark, User
from links.usecases.edit_bookmark import EditBookmarkUseCase, EditBookmarkPresenter, \
    EditBookmarkController
from tests.unit.usecases.base import UseCaseTest, PresenterSpy, ControllerTestMixin


class EditBookmarkUseCaseTest(UseCaseTest):

    def setUp(self):
        super().setUp()
        self.user = User('user')
        context.user_repo.save(self.user)

        self.bookmark = Bookmark('id1', self.user.id, 'name', 'http://test.com')
        context.bookmark_repo.save(self.bookmark)

        self.uc = EditBookmarkUseCase()
        self.presenter_spy = PresenterSpy()

    def test_user_can_edit_bookmark(self):
        self.uc.edit_bookmark(
            self.user.id,
            self.bookmark.id,
            'name changed',
            'http://test.com',
            self.presenter_spy
        )
        self.assertEqual(
            {
                'bookmark_id': self.bookmark.id,
                'errors': None
            },
            self.presenter_spy.response_model
        )

    def test_user_cannot_edit_another_users_bookmark(self):
        self.uc.edit_bookmark(
            'other_user',
            self.bookmark.id,
            'name changed',
            'http://test.com',
            self.presenter_spy
        )
        self.assertEqual(
            {
                'bookmark_id': self.bookmark.id,
                'errors': {'message': 'Insufficient Permissions'}
            },
            self.presenter_spy.response_model
        )

    def test_unknown_user_cannot_edit_bookmark(self):
        self.uc.edit_bookmark(
            'unknown',
            'id1',
            'test',
            'http://test.com',
            self.presenter_spy
        )
        self.assertEqual(
            {
                'bookmark_id': 'id1',
                'errors': {'message': 'Insufficient Permissions'}
            },
            self.presenter_spy.response_model
        )

    def test_invalid_values_are_caught(self):
        self.uc.edit_bookmark(
            self.user.id,
            self.bookmark.id,
            'test',
            'gobbledigook',
            self.presenter_spy)
        self.assertDictEqual(
            {
                'bookmark_id': self.bookmark.id,
                'errors': {'url': ['Not a valid URL']}
            },
            self.presenter_spy.response_model
        )


class EditBookmarkPresentationTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = {'bookmark_id': '1', 'errors': {}}
        presenter = EditBookmarkPresenter()
        presenter.present(response)
        self.assertDictEqual(response, presenter.get_view_model())


class EditBookmarkControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        self.mixin_setup()
        self.controller = EditBookmarkController(self.usecase, self.presenter, self.view)
        self.request = {'user_id': 'id', 'name': 'name', 'url': 'url'}

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.edit_bookmark.assert_called_with('id', 'name', 'url', self.presenter)
