from unittest import TestCase, mock

from web.app.main import presentation
from web.app.auth.presentation import AuthenticateUserController, AuthenticateUserPresenter


class ControllerTestMixin:

    def setUp(self):
        self.uc = mock.Mock()
        self.presenter = mock.Mock()
        self.view = mock.Mock()
        self.presenter.get_view_model.return_value = {'view_model': True}

    def test_presenter_calls_get_view_model(self):
        self.presenter.get_view_model.assert_called_once_with()

    def test_controller_calls_generate_view(self):
        self.view.generate_view.assert_called_once_with({'view_model': True})


class BookmarkListControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        super(BookmarkListControllerTest, self).setUp()
        self.controller = presentation.BookmarkListController(
            self.uc,
            self.presenter,
            self.view
        )
        request = {'user_id': 'user'}
        self.controller.handle(request)

    def test_usecase_is_called(self):
        self.uc.list_bookmarks.assert_called_once_with('user', self.presenter)


class BookmarkDetailsControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        super(BookmarkDetailsControllerTest, self).setUp()
        self.controller = presentation.BookmarkDetailsController(
            self.uc,
            self.presenter,
            self.view
        )

        request = {'user_id': 'user', 'bookmark_id': 'id'}
        self.controller.handle(request)

    def test_usecase_is_called(self):
        self.uc.bookmark_details.assert_called_once_with('user', 'id', self.presenter)


class CreateBookmarkControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        super(CreateBookmarkControllerTest, self).setUp()
        self.controller = presentation.CreateBookmarkController(
            self.uc,
            self.presenter,
            self.view
        )
        form = mock.Mock()
        form.name.data = 'name'
        form.url.data = 'url'

        request = {'user_id': 'user', 'form': form}
        self.controller.handle(request)

    def test_usecase_is_called(self):
        self.uc.create_bookmark.assert_called_once_with('user', 'name', 'url', self.presenter)


class AuthenticateUserControllerTest(ControllerTestMixin, TestCase):

    def setUp(self):
        self.uc = mock.Mock()
        self.presenter = mock.Mock()
        self.view = mock.Mock()
        self.presenter.get_view_model.return_value = {'view_model': True}

        # controller's handle() is not fired until form.validate_on_submit()
        # passes, so we can assume validated data at this point.
        form = mock.Mock()
        form.username.data = 'user'
        form.password.data = 'password'

        controller = AuthenticateUserController(
            self.uc,
            self.presenter,
            self.view
        )

        with mock.patch('web.app.auth.presentation.login_user') as m_login_user:
            controller.handle(form)

    def test_usecase_authenticate_user_is_called(self):
        self.uc.authenticate_user.assert_called_once_with('user', 'password', self.presenter)

    def test_presenter_calls_get_view_model(self):
        self.presenter.get_view_model.assert_called_once_with()

    def test_controller_calls_generate_view(self):
        self.view.generate_view.assert_called_once_with({'view_model': True})


class AuthenticateUserPresenterTest(TestCase):

    def test_presenter_gets_true_when_auth_succeeds(self):
        presenter = AuthenticateUserPresenter()
        presenter.present(True)
        vm = presenter.get_view_model()
        self.assertIs(vm, True)

    def test_presenter_gets_false_when_auth_succeeds(self):
        presenter = AuthenticateUserPresenter()
        presenter.present(False)
        vm = presenter.get_view_model()
        self.assertIs(vm, False)
