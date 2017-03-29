from flask import render_template, redirect, url_for, flash
from flask_login import logout_user, login_user

from links.context import context
from links.logger import get_logger
from links.usecases.interfaces import Controller, OutputBoundary, View
from links.usecases.users import AuthenticateUserUseCase
from . import auth
from .forms import LoginForm
from .models import LoggedInUser, AnonymousUser
from .. import LOGIN_MANAGER

LOGGER = get_logger(__name__)


@LOGIN_MANAGER.user_loader
def flask_login_user_loader(user_id):
    user = context.user_repo.get(user_id)
    if user.id is not None:
        loggedin_user = LoggedInUser()
        loggedin_user.id = user.id
        return loggedin_user

    return AnonymousUser()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        controller = AuthenticateUserController(
            AuthenticateUserUseCase(),
            AuthenticateUserPresenter(),
            AuthenticateUserView())
        return controller.handle(form)

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


class AuthenticateUserController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, form):
        self.view.form = form
        self.usecase.authenticate_user(form.username.data, form.password.data, self.presenter)

        is_authenticated = self.presenter.get_view_model()
        if is_authenticated:
            user = LoggedInUser()
            user.id = form.username.data
            login_user(user)

        return self.view.generate_view(is_authenticated)


class AuthenticateUserPresenter(OutputBoundary):

    def __init__(self):
        self._view_model = False

    def present(self, response_model):
        self._view_model = response_model

    def get_view_model(self):
        return self._view_model


class AuthenticateUserView(View):

    form = None

    def generate_view(self, is_authenticated):
        if is_authenticated:
            return redirect(url_for('main.index'))

        flash('Login Failed', category='danger')
        return render_template('login.html', form=self.form)
