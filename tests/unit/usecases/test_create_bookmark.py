from unittest import TestCase, mock

from links.context import context
from links.entities import User
from links.exceptions import UserNotFound, InvalidOperationError
from links.usecases import create_bookmark
from tests.unit.usecases.base import UseCaseTest, PresenterSpy, ControllerTestMixin


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
        self.presenter_spy = PresenterSpy()
        self.user = User('user')
        context.user_repo.save(self.user)

        self.usecase = create_bookmark.CreateBookmarkUseCase()
        self.usecase.user_id = self.user.id
        self.usecase.name = 'test name'
        self.usecase.url = 'http://test.com'

    def test_unknown_user_cannot_create_bookmark(self):
        self.usecase.user_id = 'unknown01234'
        with self.assertRaises(InvalidOperationError):
            self.usecase.execute(self.presenter_spy)

    def test_user_can_create_bookmark(self):
        self.usecase.execute(self.presenter_spy)
        self.assertDictEqual(self.presenter_spy.response_model.errors, {})

        created = context.bookmark_repo.get_by_user(self.user.id)[0]
        self.assertEqual(created.name, self.usecase.name)
        self.assertEqual(created.url, self.usecase.url)
        self.assertEqual(created.user_id, self.usecase.user_id)

    def test_invalid_url_is_caught(self):
        self.usecase.url = 'goobledigook'
        self.usecase.execute(self.presenter_spy)
        self.assertDictEqual(
            self.presenter_spy.response_model.errors,
            {'url': 'Invalid URL'}
        )

    def test_invalid_name_is_caught(self):
        self.usecase.name = 'too long ' * 400
        self.usecase.execute(self.presenter_spy)
        self.assertDictEqual(
            self.presenter_spy.response_model.errors,
            {'name': 'Name is too long'}
        )


class CreateBookmarkPresentationTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = create_bookmark.Response()
        # response.bookmark_id = 'id1'
        # response.errors = None
        presenter = create_bookmark.CreateBookmarkPresenter()
        presenter.present(response)
        viewmodel = presenter.get_view_model()
        # self.assertEqual('id1', viewmodel['bookmark_id'])
        self.assertTrue(viewmodel['success'])

    def test_view_model_has_errors(self):
        response = create_bookmark.Response(errors={'url': 'Invalid URL'})
        # response.bookmark_id = None
        presenter = create_bookmark.CreateBookmarkPresenter()
        presenter.present(response)
        viewmodel = presenter.get_view_model()
        # self.fail('Using presenter.present_errors')
        self.assertEqual(viewmodel['errors'], {'url': 'Invalid URL'})
        self.assertEqual(viewmodel['success'], False)

class CreateBookmarkControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        self.mixin_setup()
        self.controller = create_bookmark.CreateBookmarkController(
            self.usecase,
            self.presenter,
            self.view
        )
        self.request = {
            'user_id': 'test-user',
            'name': 'name',
            'url': 'http://test.com'
        }

    def test_usecase_is_called(self):
        self.controller.handle(self.request)
        self.usecase.execute.assert_called_with(self.presenter)
        self.assertEqual(self.usecase.user_id, 'test-user')
        self.assertEqual(self.usecase.name, 'name')
        self.assertEqual(self.usecase.url, 'http://test.com')
