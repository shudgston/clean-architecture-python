from flask import render_template, redirect, url_for, flash
from flask_login import current_user, logout_user, login_user

from links.context import context
from links.logger import get_logger
from links.usecases.authenticate_user import AuthenticateUserController, AuthenticateUserUseCase, AuthenticateUserPresenter
from links.usecases.interfaces import View

from . import auth
from .forms import LoginForm
from .models import LoggedInUser, AnonymousUser
from .. import LOGIN_MANAGER

LOGGER = get_logger(__name__)


@LOGIN_MANAGER.user_loader
def flask_login_user_loader(user_id):
    LOGGER.info("USER LOADER: %s", user_id)
    user = context.user_repo.get(user_id)
    if user.id is not None:
        loggedin_user = LoggedInUser()
        loggedin_user.id = user.id
        return loggedin_user

    LOGGER.info("RETURN ANONYMOUS USER")
    return AnonymousUser()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    LOGGER.info("CURRENT_USER: %s", current_user)
    LOGGER.info("CURRENT_USER is authenticated?: %s", current_user.is_authenticated)
    form = LoginForm()

    if form.validate_on_submit():
        controller = AuthenticateUserController(
            AuthenticateUserUseCase(),
            AuthenticateUserPresenter(),
            AuthenticateUserView())

        controller.view.form = form

        request = {
            'username': form.username.data,
            'password': form.password.data,
        }

        return controller.handle(request)

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# class AuthenticateUserController(Controller):
#
#     def __init__(self, usecase, presenter, view):
#         self.usecase = usecase
#         self.presenter = presenter
#         self.view = view
#
#     def handle(self, form):
#         self.view.form = form
#         self.usecase.authenticate_user(form.username.data, form.password.data, self.presenter)
#
#         is_authenticated = self.presenter.get_view_model()
#         if is_authenticated:
#             user = LoggedInUser()
#             user.id = form.username.data
#             login_user(user)
#
#         return self.view.generate_view(is_authenticated)
#
#
# class AuthenticateUserPresenter(OutputBoundary):
#
#     def __init__(self):
#         self._view_model = False
#
#     def present(self, response_model):
#         self._view_model = response_model
#
#     def get_view_model(self):
#         return self._view_model
#
#
class AuthenticateUserView(View):

    def __init__(self):
        self.form = None

    def generate_view(self, view_model):
        if view_model.get('is_authenticated', False):
            user = LoggedInUser()
            user.id = view_model.get('user_id')
            login_user(user)
            return redirect(url_for('main.index'))

        flash('Login Failed', category='danger')
        return render_template('login.html', form=self.form)
